from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm


@login_required
def document_list(request):
    docs = Document.objects.all()
    return render(request, 'gestio_documental/document_list.html', {'documents': docs})


@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.creat_per = request.user
            doc.save()
            return redirect('gestio_documental:document_list')
    else:
        form = DocumentForm()
    return render(request, 'gestio_documental/document_form.html', {'form': form})


@login_required
def document_detail(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    return render(request, 'gestio_documental/document_detail.html', {'document': doc})

