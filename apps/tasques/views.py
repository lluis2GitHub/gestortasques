from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404 
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Q

# Create your views here.
from .models import Tasca , Nota, Estat
from .forms import TascaForm, NotaForm
from apps.gestio_documental.forms import DocumentForm
from apps.gestio_documental.models import Document
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


class ForcedLogoutLoginView(LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        # Si hi ha un usuari autenticat, el desconnectem
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)
    
def afegir_document(request, nota_id):
    nota = get_object_or_404(Nota, pk=nota_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            nota.add_document(
                file=form.cleaned_data["fitxer"],
                title=form.cleaned_data.get("nom", ""),
                description=form.cleaned_data.get("descripcio", ""),
                user=request.user
            )
            return redirect("tasques:editar_tasca", pk=nota.tasca.id)
    else:
        form = DocumentForm()

    return render(request, "tasques/afegir_document.html", {
        "form": form,
        "nota": nota
    })

def documents_nota(request, nota_id):
    print(nota_id)
    nota = get_object_or_404(Nota, pk=nota_id, tasca__usuari=request.user)
    documents = nota.documents.all()
    return render(request, "tasques/documents_nota.html", {
        "nota": nota,
        "documents": documents
    })


def eliminar_document(request, pk):
    document = get_object_or_404(Document, pk=pk)

    # Trobar la nota que conté aquest document
    nota = Nota.objects.filter(documents=document).first()

    if request.method == "POST":
        document.delete()
        messages.success(request, "Document eliminat correctament!")
        return redirect("tasques:documents_nota", nota.id)

    return render(request, "tasques/eliminar_document.html", {
        "document": document,
        "nota": nota
    })


@login_required
def llista_tasques(request):
    sort = request.GET.get("sort", "titol")
    direction = request.GET.get("dir", "asc")
    query = request.GET.get("q", "")

    # Ordenació
    ordering = f"-{sort}" if direction == "desc" else sort

    # Base queryset
    tasques_list = Tasca.objects.filter(usuari=request.user)

    # 🔍 Filtre de cerca
    if query:
        tasques_list = tasques_list.filter(
            Q(titol__icontains=query) |
            Q(descripcio__icontains=query)
        )

    tasques_list = tasques_list.order_by(ordering)

    paginator = Paginator(tasques_list, 10)
    page_number = request.GET.get("page")
    tasques = paginator.get_page(page_number)

    columnes = [
    ("titol", "Títol"),
    ("prioritat", "Prioritat"),
    ("aplicacio", "Aplicació"),
    ("data_inici", "Data Inici"),
    ("data_fi_prevista", "Data Fi Prevista"),
    ("completada", "Completada"),
]
    return render(request, "tasques/llista.html", {
        "tasques": tasques,
        "sort": sort,
        "direction": direction,
        "query": query,
        "columnes": columnes,
        "estats": Estat.objects.all(), 
    })

@login_required
def crear_tasca(request):
    if request.method == 'POST':
        form = TascaForm(request.POST)
        if form.is_valid():
            tasca = form.save(commit=False)
            tasca.usuari = request.user
            tasca.save()
            messages.success(request, "Tasca creada correctament!")
            return redirect('tasques:llista_tasques')
    else:
        form = TascaForm()

    return render(request, 'tasques/formulari.html', {
        'form': form,
        'mode': 'crear'
    })

@login_required
def editar_tasca(request, pk):
    tasca = get_object_or_404(Tasca, pk=pk, usuari=request.user)
    form_document = DocumentForm()

    if request.method == "POST":

        # POST per afegir nota
        if "add_note" in request.POST:
            nota_form = NotaForm(request.POST,prefix="nota")
            form = TascaForm(instance=tasca)

            if nota_form.is_valid():
                nova = nota_form.save(commit=False)
                nova.tasca = tasca
                nova.save()
                messages.success(request, "Nota afegida correctament!")
                return redirect("tasques:editar_tasca", tasca.id)

        # POST per guardar la tasca
        else:
            form = TascaForm(request.POST, instance=tasca)
            nota_form = NotaForm(prefix="nota")

            if form.is_valid():
                print("----- POST DESPRÉS DE GUARDAR -----")
                print("POST data_inici:", request.POST.get("tasca-data_inici"))
                print("POST data_fi_prevista:", request.POST.get("tasca-data_fi_prevista"))
                print("------------------------------------")

                form.save()
                messages.success(request, "Tasca actualitzada correctament!")
                return redirect("tasques:editar_tasca", tasca.id)

    else:
        # GET → aquí sí que es carreguen les dates correctament
        print("TASCA GET:", tasca.data_inici, tasca.data_fi_prevista)
        form = TascaForm(instance=tasca)
        nota_form = NotaForm(prefix="nota")

    return render(request, "tasques/formulari.html", {
        "form": form,
        "nota_form": nota_form,
        "form_document": form_document,
        "tasca": tasca,
        "mode": "editar",
        "debug": False,
    })

@login_required
def eliminar_tasca(request, pk): 
    tasca = get_object_or_404(Tasca, pk=pk, usuari=request.user)
 
    if request.method == 'POST': 
        tasca.delete() 
        messages.success(request, "Tasca eliminada correctament!")
        return redirect('tasques:llista_tasques') 
        
    
    return render(request, 'tasques/eliminar.html', {'tasca': tasca}) 

@login_required
def editar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk, tasca__usuari=request.user)

    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, "Nota actualitzada correctament!")
            return redirect('editar_tasca', nota.tasca.id)
    else:
        form = NotaForm(instance=nota)

    return render(request, 'tasques/editar_nota.html', {
        'form': form,
        'nota': nota
    })

@login_required
def eliminar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk, tasca__usuari=request.user)

    if request.method == 'POST':
        tasca_id = nota.tasca.id
        nota.delete()
        messages.success(request, "Nota eliminada correctament!")
        return redirect('editar_tasca', tasca_id)

    return render(request, 'tasques/eliminar_nota.html', {
        'nota': nota
    })