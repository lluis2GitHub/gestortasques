# tasques/calendar_views.py
from datetime import date, timedelta
from calendar import monthrange
from django.shortcuts import render
from schedule.models import Calendar, Event
from apps.tasques.models import Tasca, Estat

def _get_calendar():
    return Calendar.objects.get(slug="tasques")

def _month_days(year, month):
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    days = []

    # Comença el calendari en dilluns
    start = first_day - timedelta(days=(first_day.weekday()))
    end = last_day + timedelta(days=(6 - last_day.weekday()))

    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)

    return days, first_day, last_day

def calendar_month_view(request):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    cal = _get_calendar()

    tasques = Tasca.objects.filter(usuari=request.user)
    tasques_dict = {t.id: t for t in tasques}  
    
    days, first_day, last_day = _month_days(year, month)

    events = Event.objects.filter(
        calendar=cal,
        start__date__lte=last_day,
        end__date__gte=first_day,
    )

        # 🔥 assignar la tasca correctament
    for event in events:
        try:
            tasca_id = int(event.title.replace("Tasca-", ""))
            event.tasca = tasques_dict.get(tasca_id)
        except:
            event.tasca = None
    
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    weekdays = ["DL", "DM", "DC", "DJ", "DV", "DS", "DG"]

    return render(request, "tasques/calendar_month.html", {
        "year": year,
        "month": month,
        "days": days,
        "events": events,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "weekdays": weekdays,
        "estats": Estat.objects.all(),
        "tasques_dict": tasques_dict,

    })

def calendar_week_view(request):
    today = date.today()

    # Si ve de GET, agafem la setmana que demana
    start_str = request.GET.get("start")
    if start_str:
        start = date.fromisoformat(start_str)
    else:
        start = today - timedelta(days=today.weekday())

    end = start + timedelta(days=6)

    cal = _get_calendar()

    tasques = Tasca.objects.filter(usuari=request.user)
    tasques_dict = {t.id: t for t in tasques}

    days = [start + timedelta(days=i) for i in range(7)]

    events = Event.objects.filter(
        calendar=cal,
        start__date__lte=end,
        end__date__gte=start,
    )

    for event in events:
        try:
            tasca_id = int(event.title.replace("Tasca-", ""))
            event.tasca = tasques_dict.get(tasca_id)
        except:
            event.tasca = None

    # 🔥 Setmana anterior i següent
    prev_start = (start - timedelta(days=7)).isoformat()
    next_start = (start + timedelta(days=7)).isoformat()

    return render(request, "tasques/calendar_week.html", {
        "start": start,
        "end": end,
        "days": days,
        "events": events,
        "estats": Estat.objects.all(),
        "prev_start": prev_start,
        "next_start": next_start,
    })



def calendar_day_view(request):
    today = date.today()

    day_str = request.GET.get("day")
    if day_str:
        day = date.fromisoformat(day_str)
    else:
        day = today

    cal = _get_calendar()

    events = Event.objects.filter(
        calendar=cal,
        start__date__lte=day,
        end__date__gte=day,
    )

    # 🔥 Assignar la tasca a cada event
    for e in events:
        e.tasca = None

        # Exemple: "Tasca-47"
        if e.title.startswith("Tasca-"):
            try:
                tasca_id = int(e.title.split("-")[1])
                e.tasca = Tasca.objects.filter(id=tasca_id, usuari=request.user).first()
            except ValueError:
                pass

    # 🔥 Setmana anterior i següent
    prev_day = (day - timedelta(days=1)).isoformat()
    next_day = (day + timedelta(days=1)).isoformat()

    return render(request, "tasques/calendar_day.html", {
        "day": day,
        "events": events,
        "estats": Estat.objects.all(),
        "prev_day": prev_day,
        "next_day": next_day,
    })


def calendar_gantt_view(request):
    tasques = Tasca.objects.filter(usuari=request.user)

    events = []

    for tasca in tasques:
        if tasca.data_inici and tasca.data_fi_prevista:
            events.append({
                "id": tasca.id,
                "titol": tasca.titol,
                "start": tasca.data_inici.strftime("%Y-%m-%d"),
                "end": tasca.data_fi_prevista.strftime("%Y-%m-%d"),
                "estat": tasca.estat.id,
            })

    return render(request, "tasques/calendar_gantt.html", {
        "events": events,
        "estats": Estat.objects.all(),
    })

def view_gantt(request):
    tasques = Tasca.objects.filter(usuari=request.user)

    events = []
    for t in tasques:
        if t.data_inici and t.data_fi_prevista:
            events.append({
                "id": t.id,
                "name": t.titol,
                "start": t.data_inici.strftime("%Y-%m-%d"),
                "end": t.data_fi_prevista.strftime("%Y-%m-%d"),
                "estat": t.estat.id,
            })

    return render(request, "tasques/gantt.html", {"events": events})