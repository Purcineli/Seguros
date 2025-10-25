from django.db import models
from companies.models import Companies
from django.core.exceptions import ValidationError
import os
from datetime import date
from django.utils import timezone

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Apenas arquivos PDF são permitidos.')
    
class TiposSeguros(models.Model):
    """Tipos de seguros disponíveis"""
    id = models.AutoField(primary_key=True, editable=False)
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Tipo")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Seguro"
        verbose_name_plural = "Tipos de Seguros"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Apolice(models.Model):
    """Apólice de seguro"""
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
        ('vencida', 'Vencida'),
        ('pendente', 'Pendente'),
    ]

    id = models.AutoField(primary_key=True, editable=False)
    numero = models.CharField(max_length=50, unique=True)
    seguradora = models.CharField(max_length=255)
    tipo_seguro = models.ForeignKey(TiposSeguros, on_delete=models.PROTECT, related_name='apolices', verbose_name="Tipo de Seguro")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor_seguro = models.DecimalField(max_digits=15, decimal_places=2)
    valor_premio = models.DecimalField(max_digits=15, decimal_places=2)
    moeda = models.CharField(max_length=3, default='BRL')
    segurado = models.ForeignKey(Companies, on_delete=models.PROTECT, related_name='apolices')
    observacoes = models.TextField(max_length=255, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    pdf = models.FileField(upload_to='apolices_pdfs/', validators=[validate_pdf], blank=True, null=True)

    def __str__(self):
        return f"Apolice {self.numero} - {self.tipo_seguro} - {self.segurado}"
    
    def save(self, *args, **kwargs):
        # Para updates, verifica mudanças no campo pdf
        if self.pk:
            try:
                old_instance = Apolice.objects.get(pk=self.pk)
                old_pdf = old_instance.pdf
                
                # Se o PDF foi removido (campo limpo)
                if old_pdf and not self.pdf:
                    self._delete_file(old_pdf)
                    
                # Se o PDF foi alterado (novo upload)
                elif old_pdf and self.pdf and old_pdf != self.pdf:
                    self._delete_file(old_pdf)
                    
            except Apolice.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Deleta arquivo físico ao deletar a instância
        if self.pdf:
            self._delete_file(self.pdf)
        super().delete(*args, **kwargs)

    def _delete_file(self, file_field):
        """Método helper para deletar arquivos físicos"""
        if file_field and hasattr(file_field, 'path'):
            try:
                if os.path.isfile(file_field.path):
                    os.remove(file_field.path)
            except (ValueError, OSError):
                # Log do erro se necessário
                pass

    class Meta:
        verbose_name = "Apólice de Seguro"
        verbose_name_plural = "Apólices de Seguros"

    @property
    def dias_para_vencimento(self):
        """Calcula dias restantes para o vencimento"""
        if self.status in ['cancelada', 'vencida']:
            return None
        
        hoje = date.today()
        if self.data_fim < hoje:
            return -1  # Já venceu
        
        return (self.data_fim - hoje).days

    def check_and_update_status(self):
        """Check if apolice is expired and update status"""
        if self.data_fim and self.data_fim < timezone.now().date():
            if self.status in ['ativa', 'pendente']:
                self.status = 'vencida'
                self.save()
                return True
        return False
    
    @property
    def is_expired(self):
        """Check if apolice is expired without saving"""
        if self.data_fim and self.data_fim < timezone.now().date():
            return True
        return False
    
    def save(self, *args, **kwargs):
        """Auto-check expiration on save"""
        if self.data_fim and self.data_fim < timezone.now().date():
            if self.status in ['ativa', 'pendente']:
                self.status = 'vencida'
        super().save(*args, **kwargs)





