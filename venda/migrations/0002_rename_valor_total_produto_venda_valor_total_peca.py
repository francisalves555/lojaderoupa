# Generated by Django 5.0.7 on 2024-08-22 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto_venda',
            old_name='valor_total',
            new_name='valor_total_peca',
        ),
    ]
