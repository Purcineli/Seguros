from django.shortcuts import render, redirect  
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from apolicies.models import Apolice, TiposSeguros  
from companies.models import Companies 
from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import pandas as pd
from django.http import HttpResponse

 # ou de onde seu modelo está

@login_required
def home(request):
    return render(request, 'app/home.html')

@login_required
def lista_apolices(request):
    apolices = Apolice.objects.all().select_related('segurado', 'tipo_seguro')

    # Filtros
    numero_filter = request.GET.get('numero')
    if numero_filter:
        apolices = apolices.filter(numero__icontains=numero_filter)
    
    seguradora_filter = request.GET.get('seguradora')
    if seguradora_filter:
        apolices = apolices.filter(seguradora__icontains=seguradora_filter)
    
    tipo_seguro_filter = request.GET.get('tipo_seguro')
    if tipo_seguro_filter:
        apolices = apolices.filter(tipo_seguro_id=tipo_seguro_filter)
    
    status_filter = request.GET.get('status')
    if status_filter:
        apolices = apolices.filter(status=status_filter)
    
    segurado_filter = request.GET.get('segurado')
    if segurado_filter:
        apolices = apolices.filter(segurado_id=segurado_filter)
    
    data_inicio_filter = request.GET.get('data_inicio')
    if data_inicio_filter:
        apolices = apolices.filter(data_inicio__gte=data_inicio_filter)
    
    data_fim_filter = request.GET.get('data_fim')
    if data_fim_filter:
        apolices = apolices.filter(data_fim__lte=data_fim_filter)

    # EXPORT TO EXCEL - Use the FILTERED queryset
    if request.GET.get('export') == 'xlsx':
        # Create DataFrame with FILTERED data
        data = []
        for apolice in apolices:  # This uses the filtered queryset
            data.append({
                'Número': apolice.numero,
                'Seguradora': apolice.seguradora,
                'Tipo Seguro': apolice.tipo_seguro.nome if apolice.tipo_seguro else '',
                'Segurado': apolice.segurado.nome if apolice.segurado else '',
                'Status': apolice.get_status_display(),
                'Data Início': apolice.data_inicio.strftime('%d/%m/%Y') if apolice.data_inicio else '',
                'Data Fim': apolice.data_fim.strftime('%d/%m/%Y') if apolice.data_fim else '',
                'Valor Seguro': str(apolice.valor_seguro),
                'Valor Prêmio': str(apolice.valor_premio),
                'Moeda': apolice.moeda,
                'Observações': apolice.observacoes or '',
                'Criado em': apolice.criado_em.strftime('%d/%m/%Y %H:%M') if apolice.criado_em else '',
            })
        
        df = pd.DataFrame(data)
        
        # Create HTTP response with Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="apolices.xlsx"'
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Apólices', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Apólices']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return response

    # Continue with normal view processing for HTML display
    # Ordenação
    sort_column = request.GET.get('sort', 'criado_em')
    sort_order = request.GET.get('order', 'desc')
    
    # Mapear colunas do template para campos do modelo
    sort_mapping = {
        'numero': 'numero',
        'seguradora': 'seguradora',
        'tipo': 'tipo_seguro__nome',
        'segurado': 'segurado__nome',
        'status': 'status',
        'data_inicio': 'data_inicio',
        'data_fim': 'data_fim',
        'valor_seguro': 'valor_seguro',
        'valor_premio': 'valor_premio',
        'dias_vencimento': 'data_fim',
        'criado_em': 'criado_em'
    }
    
    order_field = sort_mapping.get(sort_column, 'criado_em')
    
    if sort_order == 'desc':
        order_field = f'-{order_field}'
    
    apolices = apolices.order_by(order_field)
    
    # Verificar se usuário pode adicionar apólices
    pode_adicionar = request.user.groups.filter(name='Equipe').exists() or request.user.is_staff
    
    # Estatísticas (após filtros)
    total_apolices = apolices.count()
    apolices_ativas = apolices.filter(status='ativa').count()
    
    total_valor_seguro = apolices.aggregate(Sum('valor_seguro'))['valor_seguro__sum'] or Decimal('0')
    total_valor_premio = apolices.aggregate(Sum('valor_premio'))['valor_premio__sum'] or Decimal('0')
    
    # Formatar valores para exibição
    total_valor_seguro_fmt = f"{total_valor_seguro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    total_valor_premio_fmt = f"{total_valor_premio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Formatar valores individuais para exibição
    apolices_formatadas = []
    for apolice in apolices:
        apolice.valor_seguro_fmt = f"{apolice.valor_seguro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        apolice.valor_premio_fmt = f"{apolice.valor_premio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        apolices_formatadas.append(apolice)
    
    context = {
        'apolices': apolices_formatadas,
        'status_choices': Apolice.STATUS_CHOICES,
        'tipos_seguros': TiposSeguros.objects.filter(ativo=True).order_by('nome'),
        'numero_filter': numero_filter,
        'seguradora_filter': seguradora_filter,
        'tipo_seguro_filter': tipo_seguro_filter,
        'status_filter': status_filter,
        'segurado_filter': segurado_filter,
        'data_inicio_filter': data_inicio_filter,
        'data_fim_filter': data_fim_filter,
        'segurados': Companies.objects.all().order_by('nome'),
        'companies': Companies.objects.all().order_by('nome'),
        'total_apolices': total_apolices,
        'apolices_ativas': apolices_ativas,
        'total_valor_seguro': total_valor_seguro_fmt,
        'total_valor_premio': total_valor_premio_fmt,
        'pode_adicionar': pode_adicionar,
        'current_sort': sort_column,
        'current_order': sort_order,
    }
    return render(request, 'app/lista_apolices.html', context)

@login_required
def nova_apolice(request):
    if request.method == 'POST':
        try:
            # Validações básicas - CORRIGIDO
            required_fields = ['numero', 'seguradora', 'tipo_seguro', 'segurado', 'status', 
                             'data_inicio', 'data_fim', 'valor_seguro', 'valor_premio']
            
            for field in required_fields:
                if not request.POST.get(field):
                    messages.error(request, f'O campo {field} é obrigatório!')
                    return redirect('lista_apolices')
            
            # Verifica se o número já existe
            if Apolice.objects.filter(numero=request.POST['numero']).exists():
                messages.error(request, 'Já existe uma apólice com este número!')
                return redirect('lista_apolices')
            
            # Cria a nova apólice - CORRIGIDO
            apolice = Apolice(
                numero=request.POST['numero'],
                seguradora=request.POST['seguradora'],
                tipo_seguro_id=request.POST['tipo_seguro'],  # CORREÇÃO: tipo -> tipo_seguro
                segurado_id=request.POST['segurado'],
                status=request.POST['status'],
                data_inicio=request.POST['data_inicio'],
                data_fim=request.POST['data_fim'],
                valor_seguro=request.POST['valor_seguro'],
                valor_premio=request.POST['valor_premio'],
                moeda=request.POST.get('moeda', 'BRL'),
                observacoes=request.POST.get('observacoes', '')
            )
            
            # Salva o arquivo PDF se existir
            if 'pdf' in request.FILES:
                pdf_file = request.FILES['pdf']
                if not pdf_file.name.endswith('.pdf'):
                    messages.error(request, 'Apenas arquivos PDF são permitidos!')
                    return redirect('lista_apolices')
                apolice.pdf = pdf_file
            
            apolice.save()
            
            messages.success(request, 'Apólice criada com sucesso!')
            return redirect('lista_apolices')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar apólice: {str(e)}')
            return redirect('lista_apolices')
    
    return redirect('lista_apolices')

@login_required
def apolice_dados(request, apolice_id):
    """Retorna dados de uma apólice em JSON para edição"""
    try:
        apolice = Apolice.objects.get(id=apolice_id)
        data = {
            'numero': apolice.numero,
            'seguradora': apolice.seguradora,
            'tipo_seguro_id': apolice.tipo_seguro.id,  # CORREÇÃO: tipo -> tipo_seguro.id
            'segurado_id': apolice.segurado.id,
            'status': apolice.status,
            'data_inicio': apolice.data_inicio.isoformat(),
            'data_fim': apolice.data_fim.isoformat(),
            'valor_seguro': str(apolice.valor_seguro),
            'valor_premio': str(apolice.valor_premio),
            'moeda': apolice.moeda,
            'observacoes': apolice.observacoes or '',
            'pdf': apolice.pdf.url if apolice.pdf else None,
        }
        return JsonResponse(data)
    except Apolice.DoesNotExist:
        return JsonResponse({'error': 'Apólice não encontrada'}, status=404)
    
@login_required
def editar_apolice(request):
    if request.method == 'POST':
        try:
            apolice_id = request.POST.get('apolice_id')
            apolice = Apolice.objects.get(id=apolice_id)
            
            # Atualizar campos - CORRIGIDO
            apolice.numero = request.POST['numero']
            apolice.seguradora = request.POST['seguradora']
            apolice.tipo_seguro_id = request.POST['tipo_seguro']  # CORREÇÃO: tipo -> tipo_seguro
            apolice.segurado_id = request.POST['segurado']
            apolice.status = request.POST['status']
            apolice.data_inicio = request.POST['data_inicio']
            apolice.data_fim = request.POST['data_fim']
            apolice.valor_seguro = request.POST['valor_seguro']
            apolice.valor_premio = request.POST['valor_premio']
            apolice.moeda = request.POST.get('moeda', 'BRL')
            apolice.observacoes = request.POST.get('observacoes', '')
            
            # Atualizar PDF se um novo foi enviado
            if 'pdf' in request.FILES:
                pdf_file = request.FILES['pdf']
                if not pdf_file.name.endswith('.pdf'):
                    messages.error(request, 'Apenas arquivos PDF são permitidos!')
                    return redirect('lista_apolices')
                apolice.pdf = pdf_file
            
            apolice.save()
            messages.success(request, 'Apólice atualizada com sucesso!')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar apólice: {str(e)}')
    
    return redirect('lista_apolices')

@require_http_methods(["DELETE"])
def deletar_apolice(request, apolice_id):
    try:
        apolice = Apolice.objects.get(id=apolice_id)
        apolice.delete()
        return JsonResponse({'success': True})
    except Apolice.DoesNotExist:
        return JsonResponse({'error': 'Apólice não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)