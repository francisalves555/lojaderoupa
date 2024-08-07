from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import models
from .models import Categorias, Marcas, Produtos, Clientes, Estoque
from django.contrib import messages

def cadastro_produtos(request):
    if request.method == 'GET':
        categorias = Categorias.objects.all()
        marcas = Marcas.objects.all()
        return render(request, 'cadastro_produtos.html', {'categorias':categorias, 'marcas':marcas})
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        valor = request.POST.get('valor')
        porcentagem = request.POST.get('porcentagem')
        lucro = request.POST.get('lucro')
        venda = request.POST.get('venda')
        estoque = request.POST.get('estoque')
        data = request.POST.get('data')
        codigo = request.POST.get('codigo')
        categoria_id = request.POST.get('categoria')
        marca_id = request.POST.get('marca')
        foto = request.FILES.get('foto')

        # arruma os valores de lucro e venda para float removendo . e ,
        lucro = lucro.replace('.','').replace(',','.')
        lucro = float(lucro)
        venda = venda.replace('.','').replace(',','.')
        venda = float(venda)

        #verifica se tem algum campo faltando 
        erro = []
        if not nome:
            erro.append('Digite um nome para o produto')
        try:
            valor = valor.replace('.', '').replace(',','.')
            valor = float(valor)
        except ValueError:
            erro.append('Digite o valor do fornecedor')
        try:
            porcentagem = int(porcentagem)
        except ValueError:
            erro.append('Digite a % que deseja ganhar')
        try:
            estoque = int(estoque)    
        except ValueError:
            erro.append('Digite quantos produtos tem em estoque')
        try:
            codigo = int(codigo)
        except ValueError:
            erro.append('Digite o codigo do produto')
        if not categoria_id:
            erro.append('Escolha uma categoria para o produto')
        if not marca_id:
            erro.append('Escolha a marca para o produto')
        if not data:
            erro.append('Escolha a data de compra')

        if erro:
            for erros in erro:
                messages.error(request, erros)
            return render(request, 'cadastro_produtos.html', {'categorias':Categorias.objects.all(), 'marcas':Marcas.objects.all()})
            
        categoria = Categorias.objects.get(id=categoria_id)
        marca = Marcas.objects.get(id=marca_id)
        
        #salvando datos na model Produtos
        produto = Produtos(
            nome = nome,
            valor = valor,
            porcentagem = porcentagem,
            lucro = lucro,
            venda = venda,
            codigo = codigo,
            categoria = categoria,
            marca = marca,
            foto = foto,
        )
        produto.save()

        #salvando datos na model Estoque
        est = Estoque(
            estoque = estoque,
            data = data,
            produto = produto
        )
        est.save()

        messages.success(request, 'Cadastro realizado com sucesso!')

        return redirect('lista_produtos')

def cadastro_categorias(request):
    if request.method == 'GET':
        return render(request, 'cadastro_categorias.html')
    
    if request.method == 'POST':
        nome_c = request.POST.get('nome-c')
        foto_c = request.FILES.get('foto-c')

        nome_m = request.POST.get('nome-m')
        foto_m = request.FILES.get('foto-m')

        #variavel para saber se teve algum cadastro em categorias ou marca 
        messagem_conf = False

        #verifica se tem nome e foto e salva e salva em Categorias
        if nome_c and foto_c:
            categ = Categorias(
                nome = nome_c,
                foto = foto_c,
            )
            categ.save()
            messagem_conf = True

        #verifica se tem nome e foto e salva em Marcas
        if nome_m and foto_m:
            marc = Marcas(
                nome = nome_m,
                foto = foto_m,
            )
            marc.save()
            messagem_conf = True

        #verifica se salvou certo
        if messagem_conf:
            messages.success(request, 'Cadastrado com sucesso')
        else:
            messages.error(request, 'Erro no cadastro')

        return redirect('cadastro_categorias')

def cadastro_clientes(request):
    if request.method == 'GET':
        return render(request, 'cadastro_clientes.html')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        nascimento = request.POST.get('nascimento')

        #verifica se todos os campos foram preenchidos corretamente
        erro=[]
        if not nome:
            erro.append('Digite o nome do cliente')
        if not cpf  or len(cpf) < 11:
            erro.append('Digite o CPF corretamente')
        elif Clientes.objects.filter(cpf=cpf).exists():
            erro.append('CPF já cadastrado')
        if not endereco:
            erro.append('Digite o endereço')
        if not nascimento:
            erro.append('Coloque a data de nascimento')

        if erro:
            for erros in erro:
                messages.error(request, erros)
            return redirect('cadastro_clientes')
        
        #salva na models Cliente
        cliente = Clientes(
            nome = nome,
            cpf = cpf,
            telefone = telefone,
            endereco = endereco,
            nascimento = nascimento,
        )
        cliente.save()
        messages.success(request, 'Cadastro realizado com sucesso')

        return redirect ('cadastro_clientes')

def cadastro_estoques(request):
    todos_prod = Produtos.objects.all()
    todos_est = Estoque.objects.all()

    #calcula total de estoque
    estoque_total = {}
    for produto in todos_prod:
        estoque_total[produto.id] = Estoque.objects.filter(produto=produto).aggregate(total=models.Sum('estoque'))['total'] or 0
            

    if request.method == 'POST':
        todos_prod = Produtos.objects.all()
        todos_est = Estoque.objects.all()

        produto_id = request.POST.get('produto_id')
        estoque = request.POST.get('estoque')
        data = request.POST.get('data')

        #pega o id que foi escolhido pelo usuario e salva na models Estoque
        est_escol = Produtos.objects.get(id=produto_id)
        est = Estoque(
            estoque = estoque,
            produto = est_escol,
            data = data,
        )
        est.save()
        messages.success(request, 'Estoque cadastrado com sucesso')
        return render (request, 'cadastro_estoques.html', {'todos_prod': todos_prod, 'todos_est':todos_est, 'estoque_total':estoque_total})
    
    return render (request, 'cadastro_estoques.html', {'todos_prod': todos_prod, 'todos_est':todos_est, 'estoque_total':estoque_total})

# envia as informações de cada produto que o usuario clicou para o javascript
def get_estoque(request, prod_id):
    produto = get_object_or_404(Produtos, id=prod_id)
    estoques = Estoque.objects.filter(produto=produto)
    data = [{'data': estoque.data, 'estoque': estoque.estoque} for estoque in estoques]
    return JsonResponse(data, safe=False)