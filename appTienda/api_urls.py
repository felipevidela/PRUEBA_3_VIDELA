from django.urls import path, include 
from rest_framework.routers import DefaultRouter 
from .api_views import InsumoViewSet, PedidoCreateUpdateAPIView, PedidoFiltrarAPIView

#Esto es para crear un router de DRF 
router = DefaultRouter()

#Aquí registramos el ViewSet de Insumo en el router 
router.register('insumos', InsumoViewSet, basename='insumos')

#Aquí incluimos las urls que crea el router 
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('pedidos/', PedidoCreateUpdateAPIView.as_view()),
    path('pedidos/<int:pk>/', PedidoCreateUpdateAPIView.as_view()),
    path('pedidos/filtrar/', PedidoFiltrarAPIView.as_view()),
]