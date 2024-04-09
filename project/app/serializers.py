from .models import *
from rest_framework import serializers

class ProductsSer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CartsSer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'


class OrdersSer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class LoginSer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegistrationSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','fio','password']

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['email'],
            fio=self.validated_data['fio'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user