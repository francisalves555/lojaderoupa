from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from cadastros.models import Produtos
from .models import Pagamento

selected_products = []

def venda_produtos(request):
    todos_prod = Produtos.objects.all()
    selected_products = request.session.get('selected_products', [])

    produtos_selecionados = Produtos.objects.filter(id__in=selected_products)

    context = {
        'todos_prod': todos_prod,
        'tabela_produtos': produtos_selecionados,
        'tipo_pagamentos':Pagamento.tipo_pagamento_choices
    }
    return render(request, 'venda_produtos.html', context)

def add_produto(request):
    if request.method == "POST":
        produto_id = request.POST.get('produto_id')
        if produto_id:
            try:
                int(produto_id)  # Verifica se o ID é um número
                selected_products = request.session.get('selected_products', [])
                if produto_id not in selected_products:
                    selected_products.append(produto_id)
                    request.session['selected_products'] = selected_products
            except ValueError:
                pass  # Ignora valores inválidos

    return JsonResponse({'status': 'success', 'products': selected_products})

def produto_selecionado(request):
    selected_products_ids = request.session.get('selected_products', [])
    produtos_selecionados = Produtos.objects.filter(id__in=selected_products_ids)
    produtos_data = [
        {
            'id': produto.id,
            'nome': produto.nome,
            'marca': produto.marca.nome, 
            'codigo': produto.codigo,
            'venda': produto.venda,
        } 
        for produto in produtos_selecionados
    ]
    return JsonResponse({'products': produtos_data})

def remove_product(request):
    if request.method == "POST":
        produto_id = request.POST.get('produto_id')
        selected_products = request.session.get('selected_products', [])
        if produto_id in selected_products:
            selected_products.remove(produto_id)
            request.session['selected_products'] = selected_products

    return JsonResponse({'status': 'success', 'products': selected_products})

def clear_selected_products(request):
    if 'selected_products' in request.session:
        del request.session['selected_products']
    return HttpResponse("Selected products cleared.")

def compra_produtos(request):
    if request.method == 'POST':
        produto_ids = request.POST.getlist('produto_id')
        quantidades = request.POST.getlist('quantidade')
        tipo_pagamento = request.POST.get('tipo_pagamento')

        for produto_id, quantidade in zip(produto_ids, quantidades):
            produto = Produtos.objects.get(id=produto_id)

            print(produto)
        return HttpResponse(produto)

    return HttpResponse(status=405)