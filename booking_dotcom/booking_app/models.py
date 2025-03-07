from django.db import models

# Create your models here.


class Member(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    booking_count = models.IntegerField()
    date_joined = models.DateTimeField()

    def __str__(self):
        return self.name


class Inventory(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    remaining_count = models.PositiveIntegerField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Booking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=50)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.name} - {self.inventory.title}"
