from django.contrib.auth.models import User
from django.db import models


class County(models.Model):
    county_code = models.TextField(max_length=255, primary_key=True)
    county_name = models.CharField(max_length=200)

    def __str__(self):
        return self.county_name


class Constituency(models.Model):
    constituency_code = models.CharField(max_length=8, primary_key=True)
    constituency_name = models.CharField(max_length=200)
    county_code = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.constituency_name


class Ward(models.Model):
    ward_code = models.CharField(max_length=8, primary_key=True)
    ward_name = models.CharField(max_length=200)
    constituency_code = models.ForeignKey(Constituency, on_delete=models.CASCADE)

    def __str__(self):
        return self.ward_name


class Voter(models.Model):
    id_serial_number = models.CharField(max_length=8, default=None)
    email = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    photo = models.ImageField(default='car_placeholder.png')

    Male = 'Male'
    Female = 'Female'
    Other = 'Other'
    GENDER_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Other, 'Other'),
    ]
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    ward_code = models.ForeignKey(Ward, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
