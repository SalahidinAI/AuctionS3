from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import *
from rest_framework_simplejwt.exceptions import TokenError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password',
                  'phone_number', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class MyappLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')
        if not refresh_token:
            raise serializers.ValidationError('Refresh токен не предоставлен.')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            raise serializers.ValidationError('Недействительный токен.')

        return attrs


class CarListSerializers(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(
        queryset=UserProfile.objects.all(),
        slug_field='first_name'
    )

    class Meta:
        model = Car
        fields = '__all__'


class AuctionSerializers(serializers.ModelSerializer):
    car = serializers.SlugRelatedField(
        queryset=Car.objects.all(),
        slug_field='brand'
    )

    class Meta:
        model = Auction
        fields = '__all__'


class AuctionSimpleSerializers(serializers.ModelSerializer):
    car = serializers.SlugRelatedField(
        queryset=Car.objects.all(),
        slug_field='brand'
    )

    class Meta:
        model = Auction
        fields = ['car']


class BidSerializers(serializers.ModelSerializer):
    auction = AuctionSimpleSerializers()
    buyer = serializers.SlugRelatedField(
        queryset=UserProfile.objects.all(),
        slug_field='first_name'
    )

    class Meta:
        model = Bid
        fields = '__all__'


class FeedbackSerializers(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(
        queryset=UserProfile.objects.all(),
        slug_field='first_name'
    )
    buyer = serializers.SlugRelatedField(
        queryset=UserProfile.objects.all(),
        slug_field='first_name'
    )

    class Meta:
        model = Feedback
        fields = '__all__'

