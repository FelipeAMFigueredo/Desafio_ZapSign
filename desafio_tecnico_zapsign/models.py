# models.py
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(auto_now=True)
    api_token = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Document(models.Model):
    open_id = models.IntegerField()
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Signer(models.Model):
    token = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    external_id = models.CharField(max_length=255, null=True, blank=True)
    document = models.ForeignKey(Document, related_name="signers", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
