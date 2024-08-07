from django.shortcuts import render, redirect
from django.db import models
from cadastros.models import Produtos, Categorias, Marcas, Estoque, Clientes
from django.contrib import messages
import os
from django.conf import settings

# Create your views here.
def lista_produtos(request):
    todos_prod = Produtos.objects.all()
    estoques = Estoque.objects.all()

    total_estoque = {}
    for estoque in todos_prod:
        total_estoque[estoque.id] = Estoque.objects.filter(produto=estoque).aggregate(total=models.Sum('estoque'))['total' or 0]

    return render(request, 'lista_produtos.html', {'todos_prod':todos_prod, 'estoques':estoques, 'total_estoque':total_estoque})

def lista_categorias(request):
    todos_cate = Categorias.objects.all()
    todos_marc = Marcas.objects.all()

    return render(request, 'lista_categorias.html', {'todos_cate':todos_cate, 'todos_marc':todos_marc})

def lista_clientes(request):
    todos_clientes = Clientes.objects.all()

    return render(request, 'lista_clientes.html', {'todos_clientes':todos_clientes})

def lista_estoques(request):
    todos_estoques = Estoque.objects.all()

    return render (request, 'lista_estoques.html', {'todos_estoques':todos_estoques})

def editar_categorias(request, id):
    if request. method == 'GET':
        categoria_info = Categorias.objects.get(id=id)

        return render(request, 'editar_categorias.html', {'categoria_info':categoria_info})
    if request.method == 'POST':
        categoria_info = Categorias.objects.get(id=id)
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto-c')

        if nome:
            categoria_info.nome = nome

        if foto:
            if categoria_info.foto and os.path.isfile(categoria_info.foto.path):
                os.remove(categoria_info.foto.path)

            categoria_info.foto = foto

        categoria_info.save()
        messages.success(request, 'Categoria atualizada com sucesso!')
    
        return redirect('lista_categorias')
    
def editar_marcas(request, id):
    marca_info = Marcas.objects.get(id=id)

    if request.method == 'POST':
        marca_info = Marcas.objects.get(id=id)
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto-c')

        if nome:
            marca_info.nome = nome

        if foto:
            if marca_info.foto and os.path.isfile(marca_info.foto.path):
                os.remove(marca_info.foto.path)

            marca_info.foto = foto    
        marca_info.save()
        messages.success(request, 'Marca atualizada com sucesso')
        
        return redirect('lista_categorias')

    return render(request, 'editar_categorias.html', {'marca_info':marca_info})

def editar_clientes(request, id):
    cliente_info = Clientes.objects.get(id=id)

    if request.method == 'POST':
        cliente = Clientes.objects.get(id=id)
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        nascimento = request.POST.get('nascimento')

        if nome:
            cliente.nome = nome
        if cpf:
            cliente.cpf = cpf
        if telefone:
            cliente.telefone = telefone
        if endereco:
            cliente.endereco = endereco
        if nascimento:
            cliente.nascimento = nascimento

        cliente.save()
        messages.success(request, 'Cliente editado com sucesso')
        return redirect('lista_clientes')
    
    return render(request, 'editar_clientes.html', {'cliente_info':cliente_info})

def editar_estoques(request, id):
    estoque = Estoque.objects.get(id=id)

    if request.method == 'POST':
        estoques = request.POST.get('estoque')
        data = request.POST.get('data')

        estoque_save = Estoque.objects.get(id=id)

        if estoques:
            estoque_save.estoque = estoques
        if data:
            estoque_save.data = data
        estoque_save.save()
        messages.success(request, 'Estoque editado com sucesso')
        return redirect ('lista_estoques')

    return render (request, 'editar_estoques.html', {'estoque':estoque})

def editar_produtos(request, id):
    prod_info = Produtos.objects.get(id=id)
    cat_info = Categorias.objects.all()
    mar_info = Marcas.objects.all()

    if request.method == 'POST':
        prod_info = Produtos.objects.get(id=id)

        nome = request.POST.get('nome')
        valor = request.POST.get('valor')
        porcentagem = request.POST.get('porcentagem')
        lucro = request.POST.get('lucro')
        venda = request.POST.get('venda')        
        codigo = request.POST.get('codigo')
        categoria = request.POST.get('categoria')
        marca = request.POST.get('marca')
        foto = request.FILES.get('foto')

        if nome:
            prod_info.nome = nome
        if valor:
            valor = valor.replace('.','').replace(',','.')
            valor = float(valor)
            prod_info.valor = valor
        if lucro:
            lucro = lucro.replace('.','').replace(',','.')
            lucro = float(lucro)
            prod_info.lucro = lucro
        if venda:
            venda = venda.replace('.','').replace(',','.')
            venda = float(venda)
            prod_info.venda = venda
        if porcentagem:
            porcentagem = int(porcentagem)
            prod_info.porcentagem = porcentagem
        if codigo:
            prod_info.codigo = codigo
        if categoria:
            prod_info.categoria = Categorias.objects.get(id=categoria)
        if marca:
            prod_info.marca = Marcas.objects.get(id=marca)
        if foto:
            if prod_info.foto and os.path.isfile(prod_info.foto.path):
                os.remove(prod_info.foto.path)
            prod_info.foto = foto

        prod_info.save()
        messages.success(request, 'Produto alterado com sucesso')
        return redirect('lista_produtos')

    return render(request, 'editar_protudos.html', {'prod_info':prod_info, 'cat_info':cat_info, 'mar_info':mar_info})

def deletar_marcas(request, id):
    try:
        del_marca = Marcas.objects.get(id=id)

        if del_marca.foto and os.path.isfile(del_marca.foto.path):
            os.remove(del_marca.foto.path)

        del_marca.delete()
        messages.success(request, 'Marca deleta com sucesso')
        return redirect('lista_categorias')
    
    except del_marca.DoesNotExist():
        messages.error(request, 'Marca não existe')
        return redirect('lista_categorias')
    
def deletar_categorias(request, id):
    try:
        del_categ = Categorias.objects.get(id=id)

        if del_categ.foto and os.path.isfile(del_categ.foto.path):
            os.remove(del_categ.foto.path)

        del_categ.delete()
        messages.success(request, 'Categoria deletada com sucesso')
        return redirect('lista_categorias')

    except del_categ.DoesNotExist():
        messages.error(request, 'Essa categoria não existe')
        return redirect('lista_categorias')

