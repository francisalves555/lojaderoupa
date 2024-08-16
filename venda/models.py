from django.db import models
from cadastros.models import Produtos, Clientes
# Create your models here.

class Venda (models.Model):
    cliente = models.ForeignKey(Clientes, related_name='cliente', on_delete=models.CASCADE, blank=True, null=True)
    data = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venda {self.id} - Cliente: {self.cliente.nome}"

class Produto_venda(models.Model):
    produto = models.ForeignKey(Produtos, related_name='produtos_vendidos', on_delete=models.CASCADE)
    venda = models.ForeignKey(Venda, related_name='itens_venda', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Produto: {self.produto.nome} - Quantidade: {self.quantidade}"
    
class Pagamento(models.Model):
    tipo_pagamento_choices = (
        ('DI', 'Dinheiro'),
        ('CD', 'Cartão de credito'),
    )
    venda = models.ForeignKey(Venda, related_name='pagamento_venda', on_delete=models.CASCADE)
    tipo_pagamento = models.CharField(max_length=2, choices=tipo_pagamento_choices)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pagamento {self.id} - Tipo: {self.get_tipo_pagamento_display()}"