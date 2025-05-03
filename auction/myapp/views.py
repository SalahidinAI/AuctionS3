from tokenize import TokenError

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import SellerPermission, BuyerPermission
from .serializers import *
from .pagination import *


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = MyappLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='refresh_token'),
            },
            required=['refresh_token']
        ),
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarListView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand', 'model', 'year', 'fuel_type', 'transmission', 'price']
    ordering_fields = ['price']
    pagination_class = Pagination


class CarCreateView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializers
    permission_classes = [SellerPermission]


class AuctionCreateView(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializers
    permission_classes = [SellerPermission]


class AuctionListView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializers


class BidListView(generics.ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializers


class BidCreateView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializers
    permission_classes = [BuyerPermission]


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializers


class FeedbackListView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializers

