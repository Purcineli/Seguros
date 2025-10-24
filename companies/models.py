from django.db import models

class Companies(models.Model):
    """Empresas"""

    id = models.AutoField(primary_key=True, editable=False)
    codigo = models.CharField(max_length=4, unique=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


