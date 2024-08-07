from django.urls import path
from . import views

urlpatterns = [
    path('produtos', views.lista_produtos, name='lista_produtos'),
    path('categorias', views.lista_categorias, name='lista_categorias'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('estoques/', views.lista_estoques, name='lista_estoques'),
    path('categorias/<int:id>/editar', views.editar_categorias, name='editar_categorias'),
    path('marcas/<int:id>/editar', views.editar_marcas, name='editar_marcas'),
    path('clientes/<int:id>/editar', views.editar_clientes, name='editar_clientes'),
    path('estoques/<int:id>/editar', views.editar_estoques, name='editar_estoques'),
    path('categorias/<int:id>/deletar', views.deletar_categorias, name='deletar_categorias'),
    path('marcas/<int:id>/deletar', views.deletar_marcas, name='deletar_marcas'),
    path('produtos/<int:id>/editar', views.editar_produtos, name='editar_produtos'),
]
