from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('car-list/', CarListView.as_view(), name='car-list'),
    path('car-create/', CarCreateView.as_view(), name='car-create'),
    path('auction-list/', AuctionListView.as_view(), name='car-list'),
    path('auction-create/', AuctionCreateView.as_view(), name='car-create'),
    path('bid-list/', BidListView.as_view(), name='car-list'),
    path('bid-create/', BidCreateView.as_view(), name='car-create'),
    path('feedback-list/', FeedbackListView.as_view(), name='car-list'),
    path('feedback-create/', FeedbackCreateView.as_view(), name='car-create'),

]