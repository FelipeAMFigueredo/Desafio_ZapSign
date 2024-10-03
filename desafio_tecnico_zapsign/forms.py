from django import forms
from .models import Signer

class SignerForm(forms.ModelForm):
    class Meta:
        model = Signer
        fields = ['token', 'status', 'name', 'email', 'external_id', 'document']
