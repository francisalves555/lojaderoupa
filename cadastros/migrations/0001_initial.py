# Generated by Django 5.0.7 on 2024-07-27 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('foto', models.FileField(blank=True, null=True, upload_to='categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=70)),
                ('cpf', models.CharField(max_length=11)),
                ('telefone', models.CharField(blank=True, max_length=14, null=True)),
                ('endereco', models.CharField(max_length=100)),
                ('nascimento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Marcas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('foto', models.FileField(blank=True, null=True, upload_to='marca')),
            ],
        ),
    ]
