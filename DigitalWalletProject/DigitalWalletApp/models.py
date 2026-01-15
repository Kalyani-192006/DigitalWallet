from django.db import models
from django.contrib.auth.models import User

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=10, default='N/A')

    def __str__(self):
        return self.user.username

class Student(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="students")
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    qr_code = models.ImageField(upload_to="qr_codes", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

from django.db import models
from .models import Student

class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - ₹{self.amount} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name()

class VendorTransaction(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, default="Purchase")

    def __str__(self):
        return f"{self.vendor} → {self.student} ₹{self.amount}"
