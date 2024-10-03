from django.urls import path, include
from .views import CompanyListView, CompanyDetailView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView
from .views import DocumentListView, DocumentDetailView, DocumentCreateView, DocumentUpdateView, DocumentDeleteView
from .views import SignerListView, SignerDetailView, SignerCreateView, SignerUpdateView, SignerDeleteView
from .views import create_document_zapsign  # Importando a função da view
from django.conf.urls import handler404
from django.shortcuts import redirect
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404

urlpatterns = [
    # URL raiz que redireciona para 'companies/'
    path('', lambda request: redirect('company-list'), name='home'),  # Redireciona para a lista de empresas
    path('api/create-document-zapsign/', create_document_zapsign, name='create_document_zapsign'),  # URL para a função
    path('api/documents/', DocumentCreateView.as_view(), name='document-create'),
    
    # URLs para Company
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('company/new/', CompanyCreateView.as_view(), name='company-create'),
    path('company/edit/<int:pk>/', CompanyUpdateView.as_view(), name='company-edit'),
    path('company/delete/<int:pk>/', CompanyDeleteView.as_view(), name='company-delete'),

    # URLs para Document
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('document/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('document/new/', DocumentCreateView.as_view(), name='document-create'),
    path('document/edit/<int:pk>/', DocumentUpdateView.as_view(), name='document-edit'),
    path('document/delete/<int:pk>/', DocumentDeleteView.as_view(), name='document-delete'),

    # URLs para Signers
    path('signers/', SignerListView.as_view(), name='signer-list'),
    path('signer/<int:pk>/', SignerDetailView.as_view(), name='signer-detail'),
    path('signer/new/', SignerCreateView.as_view(), name='signer-create'),
    path('signer/edit/<int:pk>/', SignerUpdateView.as_view(), name='signer-edit'),
    path('signer/delete/<int:pk>/', SignerDeleteView.as_view(), name='signer-delete'),
]
