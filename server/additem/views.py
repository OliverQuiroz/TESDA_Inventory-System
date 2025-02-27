from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Item
from .serializers import ItemSerializer

@api_view(['GET', 'POST'])
def items_view(request):
    if request.method == 'GET':
        items = Item.objects.all().order_by('id')
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            qr_code_url = item.qr_code.url if item.qr_code else None
            return Response({
                "message": "Item added successfully",
                "qr_code": qr_code_url
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
