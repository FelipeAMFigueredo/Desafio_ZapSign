import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company, Document, Signer
from .forms import SignerForm 
from django import forms
from django.contrib.auth.decorators import login_required



class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'

class CompanyCreateView(CreateView):
    model = Company
    template_name = 'company_form.html'
    fields = ['name', 'api_token'] 
    success_url = reverse_lazy('company-list')

class CompanyUpdateView(UpdateView):
    model = Company
    template_name = 'company_form.html'
    fields = ['name', 'api_token']
    success_url = reverse_lazy('company-list')

class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'company_confirm_delete.html'
    success_url = reverse_lazy('company-list')

class DocumentListView(ListView):
    model = Document
    template_name = 'document_list.html'
    context_object_name = 'documents'

class DocumentDetailView(DetailView):
    model = Document
    template_name = 'document_detail.html'
    context_object_name = 'document'

class DocumentCreateView(CreateView):
    model = Document
    template_name = 'document_form.html'
    fields = ['open_id', 'token', 'name', 'status', 'created_by', 'company', 'external_id']
    success_url = reverse_lazy('document-list')

class DocumentUpdateView(UpdateView):
    model = Document
    template_name = 'document_form.html'
    fields = ['open_id', 'token', 'name', 'status', 'created_by', 'company', 'external_id']
    success_url = reverse_lazy('document-list')

class DocumentDeleteView(DeleteView):
    model = Document
    template_name = 'document_confirm_delete.html'
    success_url = reverse_lazy('document-list')

class SignerListView(ListView):
    model = Signer
    template_name = 'signer_list.html'
    context_object_name = 'signers'

class SignerDetailView(DetailView):
    model = Signer
    template_name = 'signer_detail.html'

class SignerCreateView(CreateView):
    model = Signer
    form_class = SignerForm
    template_name = 'signer_form.html'
    success_url = '/signers/'

class SignerUpdateView(UpdateView):
    model = Signer
    form_class = SignerForm
    template_name = 'signer_form.html'
    success_url = '/signers/'

class SignerDeleteView(DeleteView):
    model = Signer
    template_name = 'signer_confirm_delete.html'
    success_url = '/signers/'
    
class SignerForm(forms.ModelForm):
    class Meta:
        model = Signer
        fields = ['token', 'status', 'name', 'email', 'external_id', 'document']


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_document_zapsign(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Recupera o token da empresa (você pode ajustar conforme sua necessidade)
        company = Company.objects.first()  # Aqui está usando a primeira empresa, ajuste se necessário
        api_token = company.api_token
        
        # Prepara os dados para a API ZapSign
        zapsign_data = {
            "name": data['name'],
            "signers": [
                {
                    "name": data['signer']['name'],
                    "email": data['signer']['email']
                }
            ],
            "pdf_url": data['pdfUrl'],
        }

        # Envia os dados para a API ZapSign
        zapsign_response = requests.post(
            'https://sandbox.api.zapsign.com.br/api/v1/docs/',
            json=zapsign_data,
            headers={'Authorization': f'Bearer {api_token}'}
        )

        if zapsign_response.status_code == 201:
            zapsign_data = zapsign_response.json()

            # Cria o documento no banco de dados
            document = Document.objects.create(
                name=data['name'],
                token=zapsign_data['token'],
                open_id=zapsign_data['open_id'],
                status=zapsign_data['status'],
                company=company,
                external_id=data['external_id']  # Exemplo, ajuste conforme seu modelo
            )

            # Cria o signatário no banco de dados
            signer = Signer.objects.create(
                token=zapsign_data['signers'][0]['token'],
                name=data['signer']['name'],
                email=data['signer']['email'],
                document=document
            )

            return JsonResponse({'status': 'success', 'document': zapsign_data}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to create document'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)