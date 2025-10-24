from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from apolicies.models import Apolice 
from companies.models import Companies 
from decimal import Decimal
 # ou de onde seu modelo está

@login_required
def home(request):
    return render(request, 'app/home.html')

@login_required
def lista_apolices(request):
    """Lista todas as apólices"""
    apolices = Apolice.objects.all().select_related('segurado').order_by('-criado_em')
    
    # Filtros
    status_filter = request.GET.get('status')
    if status_filter:
        apolices = apolices.filter(status=status_filter)
    
    seguradora_filter = request.GET.get('seguradora')
    if seguradora_filter:
        apolices = apolices.filter(seguradora__icontains=seguradora_filter)
    
    segurado_filter = request.GET.get('segurado')
    if segurado_filter:
        apolices = apolices.filter(segurado_id=segurado_filter)
    
    # DEBUG - Verifique os segurados
    segurados_list = Companies.objects.all().order_by('nome')
    print(f"Total de segurados encontrados: {segurados_list.count()}")
    for segurado in segurados_list:
        print(f"Segurado: {segurado.nome} (ID: {segurado.id})")
    
    # Estatísticas
    total_apolices = apolices.count()
    apolices_ativas = apolices.filter(status='ativa').count()
    
    total_valor_seguro = apolices.aggregate(Sum('valor_seguro'))['valor_seguro__sum'] or Decimal('0')
    total_valor_premio = apolices.aggregate(Sum('valor_premio'))['valor_premio__sum'] or Decimal('0')
    
    # Formatar valores para exibição
    total_valor_seguro_fmt = f"{total_valor_seguro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    total_valor_premio_fmt = f"{total_valor_premio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    context = {
        'apolices': apolices,
        'status_choices': Apolice.STATUS_CHOICES,
        'status_filter': status_filter,
        'seguradora_filter': seguradora_filter,
        'segurado_filter': segurado_filter,
        'segurados': segurados_list,  # Use a lista que foi debugada
        'total_apolices': total_apolices,
        'apolices_ativas': apolices_ativas,
        'total_valor_seguro': total_valor_seguro_fmt,
        'total_valor_premio': total_valor_premio_fmt,
    }
    return render(request, 'app/lista_apolices.html', context)