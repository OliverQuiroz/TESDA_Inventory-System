from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Item
from .serializers import ItemSerializer

@api_view(['GET', 'POST'])
def items_view(request):
    """
    GET -> Returns a list of all Items
    POST -> Creates a new Item (Prevents duplicate inventory numbers only)
    """
    if request.method == 'GET':
        items = Item.objects.all().order_by('id')
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        inventory_number = data.get("inventory_number")

        # ✅ Check for duplicate inventory number (Product name can be the same)
        if Item.objects.filter(inventory_number=inventory_number).exists():
            return Response({"error": "Item with this inventory number already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        # If no duplicate inventory number, save the item
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            item = serializer.save()
            return Response({"message": "Item added successfully!", "qr_code": item.qr_code.url if item.qr_code else None}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def item_detail_view(request, pk):
    """
    GET -> Retrieve a single item
    PUT -> Update an existing item
    DELETE -> Delete the item
    """
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    # Handle each method
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(
            {"message": "Item deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
