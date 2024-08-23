from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from cadastros.models import Produtos
from .models import Pagamento, Venda, Produto_venda
from decimal import Decimal

selected_products = []

def venda_produtos(request):
    todos_prod = Produtos.objects.all()
    selected_products = request.session.get('selected_products', [])
    valor_total = Decimal(request.session.get('valor_total', '0.0'))

    produtos_selecionados = Produtos.objects.filter(id__in=selected_products)

    context = {
        'todos_prod': todos_prod,
        'tabela_produtos': produtos_selecionados,
        'tipo_pagamentos':Pagamento.tipo_pagamento_choices,
        'valor_total': valor_total
    }
    return render(request, 'venda_produtos.html', context)

def add_produto(request):
    if request.method == "POST":
        produto_id = request.POST.get('produto_id')
        if produto_id:
            try:
                int(produto_id)  # Verifica se o ID é um número
                selected_products = request.session.get('selected_products', [])
                valor_total = Decimal(request.session.get('valor_total', '0.0'))

                if produto_id not in selected_products:
                    produto = Produtos.objects.get(id=produto_id)
                    selected_products.append(produto_id)
                    valor_total += produto.venda
                    print(valor_total)

                    request.session['selected_products'] = selected_products
                    request.session['valor_total'] = str(valor_total)
            except ValueError:
                pass  # Ignora valores inválidos

    return JsonResponse({'status': 'success', 'products':selected_products, 'valor_total':str(valor_total)})

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
        valor_total = Decimal(request.session.get('valor_total', '0.0')
)
        if produto_id in selected_products:
            selected_products.remove(produto_id)
            produto = Produtos.objects.get(id=produto_id)
            valor_total -= produto.venda
            print(valor_total)

            request.session['selected_products'] = selected_products
            request.session['valor_total'] = str(valor_total)

    return JsonResponse({'status': 'success', 'products':selected_products, 'valor_total':str(valor_total)})

def clear_selected_products(request):
    if 'selected_products' in request.session:
        del request.session['selected_products']

    return render(request, 'venda_produtos.html')

def compra_produtos(request):
    if request.method == 'POST':
        produto_ids = request.POST.getlist('produto_id')
        quantidades = request.POST.getlist('quantidade')
        tipo_pagamento = request.POST.get('tipo_pagamento')
        valor_total_compra = request.POST.get('valor_total_compra')
        valor_total_pecas = request.POST.getlist('valor_total_peca')
        data = request.POST.get('data')
        valor_pago = request.POST.get('valor_pago')

        valor_total_compra = Decimal(valor_total_compra.replace('R$', '').replace('.', '').replace(',', '.').strip())  
        valor_pago = Decimal(valor_pago.replace('R$', '').replace('.', '').replace(',', '.').strip())

        valor_total_pecas = [
            Decimal(valor.replace('R$', '').replace('.', '').replace(',', '.').strip())
            for valor in valor_total_pecas
            ]

        id_venda = Venda(
            data = data,
            valor_total = valor_total_compra,
        )
        id_venda.save()

        id_pagamento = Pagamento(
            venda = id_venda,
            tipo_pagamento = tipo_pagamento,
            valor_pago = valor_pago,
        )
        id_pagamento.save()

        for produto_id, quantidade, valor_total_peca in zip(produto_ids, quantidades, valor_total_pecas):
            produto = Produtos.objects.get(id=produto_id)
            produto_valor = produto.valor

            id_produto = Produto_venda(
                produto = produto,
                venda = id_venda,
                quantidade = quantidade,
                valor_unitario = produto_valor,
                valor_total_peca = valor_total_peca,
            )
            id_produto.save()

        return redirect('clear_selected_products')

    return HttpResponse(status=405)