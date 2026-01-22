from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default-profile.png')




from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    account_status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Frozen', 'Frozen')])
    is_verified = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    last_login_location = models.BooleanField(default=False)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_status = models.CharField(max_length=20, choices=[('Verified', 'Verified'), ('Fraud', 'Fraud')])
    transaction_type = models.CharField(max_length=20, choices=[('Credit', 'Credit'), ('Debit', 'Debit')])
    location = models.ForeignKey(UserLocation, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField()

class FraudDetection(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    is_fraud = models.BooleanField()
    fraud_score = models.DecimalField(max_digits=5, decimal_places=2)
    detection_date = models.DateTimeField(auto_now_add=True)
    detection_method = models.CharField(max_length=50)
    remarks = models.TextField(null=True, blank=True)

class Report(models.Model):
    date = models.DateField()
    total_transactions = models.IntegerField()
    fraudulent_transactions = models.IntegerField()
    detection_rate = models.DecimalField(max_digits=5, decimal_places=2)
    high_risk_accounts = models.IntegerField()
    time_period = models.CharField(max_length=20, choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')])

class AdminActions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=20, choices=[('Warning', 'Warning'), ('Freeze Account', 'Freeze Account')])
    action_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)

