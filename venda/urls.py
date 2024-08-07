from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.venda_produtos, name='venda_produtos'),
    path('add_product/', views.add_product, name='add_product'),
    path('get_selected_products/', views.get_selected_products, name='get_selected_products'),
    path('remove_product/', views.remove_product, name='remove_product'),
    path('clear_selected_products/', views.clear_selected_products, name='clear_selected_products'),
]
