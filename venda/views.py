from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from cadastros.models import Produtos

selected_products = []

def venda_produtos(request):
    todos_prod = Produtos.objects.all()
    selected_products = request.session.get('selected_products', [])

    produtos_selecionados = Produtos.objects.filter(id__in=selected_products)

    context = {
        'todos_prod': todos_prod,
        'selected_products': produtos_selecionados
    }
    return render(request, 'venda_produtos.html', context)

def add_product(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                int(product_id)  # Verifica se o ID é um número
                selected_products = request.session.get('selected_products', [])
                if product_id not in selected_products:
                    selected_products.append(product_id)
                    request.session['selected_products'] = selected_products
            except ValueError:
                pass  # Ignora valores inválidos

    return JsonResponse({'status': 'success', 'products': selected_products})

def get_selected_products(request):
    selected_products_ids = request.session.get('selected_products', [])
    produtos_selecionados = Produtos.objects.filter(id__in=selected_products_ids)
    produtos_data = [
        {
            'id': produto.id,
            'nome': produto.nome,
            'marca': produto.marca.nome,  # Certifique-se de que 'marca' está incluído
            'codigo': produto.codigo,
            'venda': produto.venda,
        } 
        for produto in produtos_selecionados
    ]
    return JsonResponse({'products': produtos_data})

def remove_product(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        selected_products = request.session.get('selected_products', [])
        if product_id in selected_products:
            selected_products.remove(product_id)
            request.session['selected_products'] = selected_products

    return JsonResponse({'status': 'success', 'products': selected_products})

def clear_selected_products(request):
    if 'selected_products' in request.session:
        del request.session['selected_products']
    return HttpResponse("Selected products cleared.")