from django.shortcuts import render
from .models import *
from rest_framework.authtoken.models import Token
from .serializers import *
from .permissions import IsClient
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
def getProducts(request):
    products = Products.objects.all()
    prod_ser = ProductsSer(products, many=True)
    return Response({'data':prod_ser.data})

@api_view(['POST'])
def login(request):
    user_ser = LoginSer(data=request.data)
    if user_ser.is_valid():
        try:
            user = User.objects.get(email=user_ser.validated_data['email'])
        except:
            return Response({'error':{'code': 401, 'message':'Authentication failed'}})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'data':{'user_token':token.key}})
    return Response({'error': {'code': 422, 'message': 'Validation error', 'errors':user_ser.errors}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'data':{'message':'Logout is succes'}})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    prod_ser=ProductsSer(data=request.data)
    if prod_ser.is_valid():
        prod_ser.save
        return Response({'data':{'id':prod_ser.data['id'], 'message':'Product added'}})
    return Response({'error':{'code':422, 'message':'Validation error', 'errors':prod_ser.errors}})


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def changeproduct(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except:
        return Response({'error':{'code': 404, 'message': 'Not found'}})
    if request.method == 'DELETE':
        product.delete()
        return Response({'data': {'message':'Product removed'}})
    elif request.method == 'PATCH':
        prod_ser = ProductsSer(data=request.data, instance=product, partial=True)
        if prod_ser.is_valid():
            prod_ser.save()
            return Response({'data': prod_ser.data})
        return Response({'error':{'code': 422, 'message': 'Validation error', 'errors':prod_ser.errors}})


@api_view(['GET'])
@permission_classes([IsClient])
def getCarts(request):
    carts = Carts.objects.filter(user=request.user)
    carts_ser = CartsSer(carts, many=True)
    return Response({'data':carts_ser.data})


@api_view(['POST', 'DELETE'])
@permission_classes([IsClient])
def changecart(request, pk):
    try:
        cart = Carts.objects.get(pk=pk)
    except:
        return Response({'error':{'code': 404, 'message': 'Not found'}})
    if request.method == 'DELETE':
        cart.delete()
        return Response({'data': {'message':'Item removed from cart'}})
    elif request.method == 'POST':
        try:
            product = Products.objects.get(pk=pk)
        except:
            return Response({'error':{'code':403, 'message':'not found'}})
        Carts.objects.create(user=request.user, product=product)
        return Response({'data':{'message':'Product added to cart'}})