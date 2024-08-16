# Generated by Django 5.0.7 on 2024-08-15 23:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cadastros', '0007_produtos_lucro_produtos_porcentagem_produtos_venda_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='cadastros.clientes')),
            ],
        ),
        migrations.CreateModel(
            name='Produto_venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos_vendidos', to='cadastros.produtos')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_venda', to='venda.venda')),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pagamento', models.CharField(choices=[('DI', 'Dinheiro'), ('CD', 'Cartão de credito')], max_length=2)),
                ('valor_pago', models.DecimalField(decimal_places=2, max_digits=10)),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagamento_venda', to='venda.venda')),
            ],
        ),
    ]
