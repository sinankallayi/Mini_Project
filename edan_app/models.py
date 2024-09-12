from django.db import models

# Create your models here.
class LoginTable(models.Model):
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class guest_table(models.Model):
    login = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number=models.BigIntegerField()
    email=models.CharField(max_length=100)
    image=models.ImageField(upload_to='guest_images/')

    def __str__(self):
        return self.name
    

    

class room_table(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.CharField(max_length=50)

class RoomImage(models.Model):
    room = models.ForeignKey(room_table, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')

class RoomVideo(models.Model):
    room = models.ForeignKey(room_table, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='room_videos/')
    
