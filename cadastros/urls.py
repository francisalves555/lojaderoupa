from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.cadastro_produtos, name='cadastro_produtos'),
    path('categorias/', views.cadastro_categorias, name='cadastro_categorias'),
    path('clientes/', views.cadastro_clientes, name='cadastro_clientes'),
    path('estoques/', views.cadastro_estoques, name='cadastro_estoques'),
    path('get_estoque/<int:prod_id>/', views.get_estoque, name='get_estoque'),
]
