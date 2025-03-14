from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Item
from .serializers import ItemSerializer

@api_view(['GET', 'POST'])
def items_view(request):
    """
    GET -> Returns a list of all Items (or filter by ?inventory_number=...)
    POST -> Creates a new Item (Prevents duplicate inventory_number)
    """
    if request.method == 'GET':
        inv_num = request.GET.get('inventory_number')
        if inv_num:
            # Filter by inventory_number if provided
            items = Item.objects.filter(inventory_number=inv_num).order_by('id')
        else:
            items = Item.objects.all().order_by('id')

        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        inventory_number = data.get("inventory_number")

        # ✅ Check for duplicate inventory number
        if Item.objects.filter(inventory_number=inventory_number).exists():
            return Response(
                {"error": "Item with this inventory number already exists!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            item = serializer.save()  # This triggers item.save() => generates QR code
            return Response(
                {
                    "message": "Item added successfully!",
                    "qr_code": item.qr_code.url if item.qr_code else None
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def item_detail_view(request, pk):
    """
    GET -> Retrieve a single item by primary key
    PUT -> Update an existing item
    DELETE -> Delete the item
    """
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()  # will re-generate QR if self.qr_code was cleared, etc.
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(
            {"message": "Item deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
