from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='userImg')


class BaseModel(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True)
    create_at = models.DateField(auto_now_add=True)
    upadate_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self):
        return self.amenity_name


class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=100)
    hotel_price = models.IntegerField()
    description = models.TextField()
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)

    def __str__(self):
        return self.hotel_name


class HotelImages(BaseModel):
    hotel = models.ForeignKey(
        Hotel, related_name='images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='hotel')
    room_img = models.ImageField(upload_to='room')


class Hotelbooking(BaseModel):
    hotel = models.ForeignKey(
        Hotel, related_name='hotel_booking', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="user_booking", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type = models.CharField(max_length=100,
                                    choices=(('Pre paid', 'Pre paid'), ('Post paid', 'Post Paid')))


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    query = models.TextField(max_length=1000)

    def __str__(self):
        return self.f_name
