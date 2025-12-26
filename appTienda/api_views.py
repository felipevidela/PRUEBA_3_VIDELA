from rest_framework import viewsets 
from .models import Insumo, Pedido 
from .serializers import InsumoSerializer, PedidoSerializer  
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from django.shortcuts import get_object_or_404 
from datetime import datetime 

class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer 

class PedidoCreateUpdateAPIView(APIView): 
    #Para hacer POST /api/pedidos/ 
    def post (self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid(): 
            pedido = serializer.save()
            return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Para hacer PUT/PATCH/api/pedidos/<id>/ 
    def put(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        serializer = PedidoSerializer(pedido, data=request.data)
        if serializer.is_valid(): 
            pedido = serializer.save()
            return Response(PedidoSerializer(pedido).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        serializer = PedidoSerializer(pedido, data=request.data, partial=True)
        if serializer.is_valid():
            pedido = serializer.save()
            return Response(PedidoSerializer(pedido).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PedidoFiltrarAPIView(APIView):
    #Ejemplo GET /api/pedidos/filtrar/?desde=2025-01-01&hasta=2025-12-31&estados=pendiente,enviado&max=20
    def get(self, request):
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')
        estado = request.query_params.get('estados') #Puede ser pendiente o enviado 
        max_results = request.query_params.get('max', '50')

        #Validaciones 
        try: 
            max_results = int(max_results)
            if max_results < 1 or max_results > 200: 
                return Response ({"error": "max debe estar entre 1 y 200"}, status=status.HTTP_400_BAD_REQUEST)
        except: 
            return Response ({"error": "max debe ser entero"}, status=status.HTTP_400_BAD_REQUEST)

        try: 
            if desde:
                datetime.strptime(desde, "%Y-%m-%d")
            if hasta: 
                datetime.strptime(hasta, "%Y-%m-%d")
        except: 
            return Response ({"error": "Formato de fecha invalido. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = Pedido.objects.all() 

        if desde:
            qs = qs.filter(fecha_solicitada__gte=desde)
        if hasta:
            qs = qs.filter(fecha_solicitada__lte=hasta)

        if estado:
            lista_estados = [estado.strip() for estado in estado.split(",") if estado.strip()]
            qs = qs.filter(estado__in=lista_estados)

        qs = qs.order_by('-id')[:max_results]
        data = PedidoSerializer(qs, many=True).data

        return Response({
            "count": len(data),
            "results": data
        }, status=status.HTTP_200_OK)





            

    






