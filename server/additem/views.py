from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


@api_view(['GET', 'POST'])
def items_view(request):
    if request.method == 'GET':
        prop_no = request.GET.get("property_number")
        items = Item.objects.filter(property_number=prop_no) if prop_no else Item.objects.all()
        return Response(ItemSerializer(items, many=True).data, status=status.HTTP_200_OK)

    # POST
    data = request.data
    prop_no = data.get("property_number")
    if Item.objects.filter(property_number=prop_no).exists():
        return Response({"error": "Duplicate Property Number!"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ItemSerializer(data=data)
    if serializer.is_valid():
        item = serializer.save()  # QR is auto-generated in model.save()
        return Response({"message": "Item added!", "qr_code": item.qr_code.url}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def item_detail_view(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ItemSerializer(item).data)

    if request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
