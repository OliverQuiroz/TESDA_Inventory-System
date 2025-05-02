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

from rest_framework.parsers import MultiPartParser
from django.http import FileResponse
from PyPDF2 import PdfReader, PdfWriter
import io

@api_view(['POST'])
def protect_pdf(request):
    pdf_file = request.FILES.get('pdf')
    password = request.POST.get('password')

    if not pdf_file or not password:
        return Response({'error': 'Missing PDF or password.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        buffer = io.BytesIO()
        writer.write(buffer)
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename="Protected_Registered_Items.pdf")
    except Exception as e:
        return Response({'error': f'Failed to protect PDF: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
