from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

ROLE = (
    ('продавец', 'продавец'),
    ('покупатель', 'покупатель')
)


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    role = models.CharField(max_length=12, choices=ROLE)


class Car(models.Model):
    brand = models.CharField(max_length=65)
    model = models.CharField(max_length=65)
    year = models.DateField()
    fuel_type = models.CharField(max_length=65)
    mileage = models.PositiveIntegerField(null=True, blank=True)
    DRIVE_CHOICES = (
        ('Автомат', 'Автомат'),
        ('Механика', 'Механика'),
    )
    transmission = models.CharField(max_length=10, choices=DRIVE_CHOICES)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller')

    def __str__(self):
        return self.brand


class Auction(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='auction_car')
    start_price = models.IntegerField()
    max_price = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    STATUS = (
        ('активен', 'активен'),
        ('завершен', 'завершен'),
        ('отменен', 'отменен'),
    )
    status = models.CharField(max_length=25, choices=STATUS)

    def __str__(self):
        return str(self.car)


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer')
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.auction)


class Feedback(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='feedback_seller')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='feedback_buyer')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.seller)


