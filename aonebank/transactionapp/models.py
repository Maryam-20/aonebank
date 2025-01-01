from django.db import models
from django.contrib.auth.models import User
import random 


# Create your models here.
class Account_table(models.Model):
    acc_type = [
        ("Savings", "Savings"),
        ("Current", "Current"),
        ("Fixed Deposit", " Fixed Deposit"),
        ("Domicilliary", "Domicilliary"),
        
    ]
    
    status = [
        ("Active", "Active"),
        ("Retired", "Retired"),
        ("Suspended", "Suspended"),
        ("Freeze", "Freeze"),
        ("On Leave", "On Leave"),
        ("Dormant", "Dormant"),
    ]
    
    account = "22" + str(random.randint(00000000, 99999999))
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.BigIntegerField(unique=False, default=0000)
    account_type = models.CharField(choices=acc_type, unique=False, max_length=20)
    account_number = models.CharField(unique=True, max_length= 10, default=account)
    account_pin = models.IntegerField(default= 0000, unique = False)
    account_status = models.CharField(choices= status, default= "Active", unique= False, max_length= 10)
    
    
class Transaction_table(models.Model):
    transaction_id = models.AutoField(primary_key= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account_table, on_delete= models.CASCADE)
    transaction_type = models.CharField(unique= False, max_length= 20)
    transaction_date = models.DateField(auto_now_add=True)
    transaction_amount = models.BigIntegerField(unique=False)
    beneficiary_account_number = models.CharField(unique= False, max_length= 11, null= True)
    beneficiary_bank = models.CharField(unique=False, max_length= 15, null= True)
    recepient_phone_number = models.CharField(unique=False, max_length= 11, null= True)
    recepient_bank_name = models.CharField(unique=False, max_length= 30, null= True)
    recepient_account_number = models.CharField(max_length= 10, unique=False, null=True)
    sender_bank_name = models.CharField(unique=False, max_length= 20, null = True)
    sender = models.ForeignKey(Account_table, related_name="sender", on_delete=models.CASCADE, unique=False, null=True)    
    bill_type = models.CharField(unique=False, max_length=10, null= True)
    mobile_network = models.CharField(unique=False, max_length=10, null=True)