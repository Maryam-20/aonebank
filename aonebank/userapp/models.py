from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profiles(models.Model):
    countries = [
        ("Nigeria", "Nigeria"),
        ("Ghana", "Ghana"),
        ("UK", "UK"),
        ("USA", "USA"),
    ]
    
    states = [
        ("Abia", "Abia"),
        ("Oyo", "Oyo"),
        ("Osun", "Osun"),
        ("Lagos", "Lagos"),
        ("Kano", "Kano"),
        ("Abuja", "Abuja"),
    ]

    position = [
        ("CEO", "CEO"),
        ("GMD", "GMD"),
        ("CTO", "CTO"),
        ("Supervisor", "Supervisor"),
        ("Marketer", "Marketer"),
        ("Accountant", "Accountant"),
        ("Cashier", "Cashier"),
        ("Driver", "Driver"),
        ("Customer care", "Customer care"),
    ]
    
    ma_status = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Divorce", "Divorce"),
        ("Complicated", "Complicated"),
    ]
    
    userStatus = [
        ("Active", "Active"),
        ("Retired", "Retired"),
        ("Suspended", "Suspended"),
        ("Freeze", "Freezer"),
        ("On leave", "On leave"),
    ]
    
    sex = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    
    dept = [
        ("Accounting/Finance", "Accounting/Finance"),
        ("Customer Service", "Customer Service"),
        ("Human Resources", "Human Resources"),
        ("Information Technology", "Information Technology"),
        ("Investment Banking & Market", "Investment Banking & Market"),
    ]
    
    profile = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(unique=False, max_length=100, null=True)
    phone = models.CharField(unique=True, max_length=11, null=True)
    date_of_birth = models.DateField(unique=False, null=True, max_length=10)
    bvn = models.CharField(unique=True, null=True, max_length=10)
    occupation = models.CharField(unique=False, null = True, max_length= 50)
    # status = models.CharField(unique = False, max_length=20, null=True)
    sex = models.CharField(choices=sex, max_length=20, null = True, unique= False)
    nationality = models.CharField(choices=countries, unique= False, max_length= 50, null= True)
    state = models.CharField(choices= states, unique=False, max_length= 20, null=True )
    means_of_identity = models.ImageField(upload_to= "identityImage/", unique = False, null = True)
    particulars = models.FileField(upload_to='particularsImage/', unique= False, null = True)
    profile_passport = models.ImageField(upload_to="userImage/", unique = False, null = True)
    position = models.CharField(choices= position, unique = False, max_length= 20, null = True)
    department = models.CharField(choices=dept, unique=False, max_length= 60, null = True, )
    marital_status = models.CharField(choices = ma_status, unique= False, max_length= 20, null = True)
    staff = models.BooleanField(default= False, unique= False)
    user_status = models.CharField(choices=userStatus, unique = False, max_length= 20, null = True)
    
    
    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profiles.objects.create(user=instance)
            
    @receiver(post_save, sender= User)
    def safe_user_profile(sender, instance, **kwargs):
        instance.profiles.save()