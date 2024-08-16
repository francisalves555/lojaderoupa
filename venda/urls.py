from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.venda_produtos, name='venda_produtos'),
    path('add_produto/', views.add_produto, name='add_produto'),
    path('produto_selecionado/', views.produto_selecionado, name='produto_selecionado'),
    path('remove_product/', views.remove_product, name='remove_product'),
    path('clear_selected_products/', views.clear_selected_products, name='clear_selected_products'),
    path('compra_produtos/', views.compra_produtos, name='compra_produtos'),
]
