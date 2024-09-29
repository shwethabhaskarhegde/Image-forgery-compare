from django.db import models

# Create your models here.
class UserRegistration(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=30)

class UserLogin(models.  Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
    utype = models.CharField(max_length=20)

class ImageDetails(models.Model):
    image_type = models.CharField(max_length=20)
    image_name = models.CharField(max_length=30)
    image_location = models.CharField(max_length=100)
    details = models.CharField(max_length=300)
    created_date = models.CharField(max_length=15)
    created_by = models.CharField(max_length=30)

class UserImage(models.Model):
    user_name = models.CharField(max_length=30)
    date = models.CharField(max_length=10)
    image_type = models.CharField(max_length=20)
    details = models.CharField(max_length=300)
    imglocation = models.CharField(max_length=200)


class Results(models.Model):
    original_img_id = models.CharField(max_length=10)
    user_image_id = models.CharField(max_length=10)
    result = models.CharField(max_length=100)
    date = models.CharField(max_length=10)
    by = models.CharField(max_length=30)

class Feedback(models.Model):
    from_details = models.CharField(max_length=30)
    to = models.CharField(max_length=30)
    date = models.CharField(max_length=10)
    details = models.CharField(max_length=300)