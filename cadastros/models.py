from django.db import models

# Create your models here.
class Marcas (models.Model):
    nome = models.CharField(max_length=50)
    foto = models.FileField(upload_to="marca", null=True, blank=True)

    def __str__(self):
        return self.nome
    
class Categorias (models.Model):
    nome = models.CharField(max_length=50)
    foto = models.FileField(upload_to="categoria", null=True, blank=True)

    def __str__(self):
        return self.nome
    
class Clientes (models.Model):
    nome = models.CharField(max_length=70)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=14, null=True, blank=True)
    endereco = models.CharField(max_length=150)
    nascimento = models.DateField()

    def __str__(self):
        return self.nome
    
class Produtos (models.Model):
    nome = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    porcentagem = models.IntegerField()
    lucro = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Adiciona um valor padrão
    venda = models.DecimalField(max_digits=10, decimal_places=2)
    codigo = models.IntegerField(unique=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, related_name='categorias') 
    marca = models.ForeignKey(Marcas, on_delete=models.CASCADE, related_name='marcas')
    foto = models.FileField(upload_to="produto", null=True, blank=True)

    def __str__(self):
        return self.nome
    
class Estoque (models.Model):
    estoque = models.IntegerField()
    data = models.DateField()
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, related_name='protudo')
