from django import forms
from django.contrib.auth.models import User
from .models import Parent

# 🔐 Parent Registration Form
class ParentRegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# 🔐 Parent Login Form
class ParentLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

from django import forms
from .models import Student

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Name'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}),
        }

class FundForm(forms.Form):
    student_id = forms.CharField(label="Student ID", max_length=50)
    amount = forms.DecimalField(label="Add Amount", max_digits=10, decimal_places=2)
    limit = forms.DecimalField(label="Set Spending Limit", max_digits=10, decimal_places=2)



class FundForm(forms.Form):
    student_id = forms.CharField(label="Student ID", max_length=50)
    amount = forms.DecimalField(label="Add Amount", max_digits=10, decimal_places=2)
    limit = forms.DecimalField(label="Set Spending Limit", max_digits=10, decimal_places=2)

class TransactionSearchForm(forms.Form):
    student_id = forms.CharField(label="Student ID", max_length=50)


class StudentLoginForm(forms.Form):
    name = forms.CharField(label="Student Name", max_length=100)
    student_id = forms.CharField(label="Roll Number", max_length=50)
 

from .models import Vendor

class VendorRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['phone']

class VendorLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class VendorPaymentForm(forms.Form):
    student_id = forms.CharField(label="Student ID")
    amount = forms.DecimalField(min_value=1, label="Amount to Deduct")
