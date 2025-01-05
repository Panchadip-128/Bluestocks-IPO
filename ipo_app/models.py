from django.db import models
from django.contrib.auth.models import AbstractUser

# User Table
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)  # To differentiate between admin and regular users
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# IPO Table
class IPO(models.Model):
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    ipo_date = models.DateTimeField()
    price_range = models.CharField(max_length=50)  # Example: "100-120"
    total_shares = models.IntegerField()
    available_shares = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

# Subscription Table
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ipo = models.ForeignKey(IPO, on_delete=models.CASCADE)
    subscribed_shares = models.IntegerField()
    subscription_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.ipo.company_name}"

# Transactions Table
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ipo = models.ForeignKey(IPO, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.user.username} for {self.ipo.company_name}"

# Notifications Table
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


class Stock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
