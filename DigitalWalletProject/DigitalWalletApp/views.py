from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (
    ParentRegisterForm, ParentLoginForm, AddStudentForm,
    FundForm, TransactionSearchForm, StudentLoginForm,
    VendorRegisterForm, VendorProfileForm, VendorLoginForm,
    VendorPaymentForm
)

from .models import Parent, Student, Vendor, VendorTransaction


# -------------------- Home --------------------

def home(request):
    return render(request, 'home.html')


# -------------------- Parent Views --------------------

def parent_register(request):
    if request.method == 'POST':
        form = ParentRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Parent.objects.create(user=user, phone=form.cleaned_data['phone'])
            messages.success(request, "Registration successful. Please log in.")
            return redirect('parent_login')
    else:
        form = ParentRegisterForm()
    return render(request, 'parent/register.html', {'form': form})


def parent_login(request):
    if request.method == 'POST':
        form = ParentLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None and hasattr(user, 'parent'):
                login(request, user)
                return redirect('parentdashboard')
            else:
                messages.error(request, "Invalid credentials or not a parent account.")
    else:
        form = ParentLoginForm()
    return render(request, 'parent/login.html', {'form': form})


@login_required
def parentdashboard(request):
    return render(request, 'parent/dashboard.html')


@login_required
def parent_profile(request):
    parent = Parent.objects.get(user=request.user)
    students = Student.objects.filter(parent=parent)
    return render(request, 'parent/profile.html', {
        'parent': parent,
        'students': students
    })


@login_required
def generate_student_qr(request):
    qr_data = None
    student = None
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.parent = request.user.parent
            student.save()
            qr_data = student.student_id
    else:
        form = AddStudentForm()
    return render(request, 'parent/generate_qr.html', {
        'form': form,
        'student': student,
        'qr_data': qr_data
    })


@login_required
def fund_student(request):
    parent = Parent.objects.get(user=request.user)
    student = None
    if request.method == 'POST':
        form = FundForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            amount = form.cleaned_data['amount']
            limit = form.cleaned_data['limit']
            try:
                student = Student.objects.get(student_id=student_id, parent=parent)
                student.wallet_balance += amount
                student.spending_limit = limit
                student.save()
                messages.success(request, f"₹{amount} added to {student.name}'s wallet. Limit set to ₹{limit}.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found or does not belong to you.")
    else:
        form = FundForm()
    return render(request, 'parent/fund_student.html', {'form': form, 'student': student})


@login_required
def transaction_history(request):
    parent = Parent.objects.get(user=request.user)
    transactions = []
    student = None
    if request.method == 'POST':
        form = TransactionSearchForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            try:
                student = Student.objects.get(student_id=student_id, parent=parent)
                transactions = VendorTransaction.objects.filter(student=student).order_by('-timestamp')
            except Student.DoesNotExist:
                messages.error(request, "Student not found or does not belong to you.")
    else:
        form = TransactionSearchForm()
    return render(request, 'parent/transaction_history.html', {
        'form': form,
        'student': student,
        'transactions': transactions
    })


def parent_logout(request):
    logout(request)
    return redirect('parent_login')


# -------------------- Student Views --------------------

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            student_id = form.cleaned_data['student_id']
            try:
                student = Student.objects.get(name=name, student_id=student_id)
                request.session['student_id'] = student.id
                return redirect('student_dashboard')
            except Student.DoesNotExist:
                messages.error(request, "Invalid name or roll number, or student not registered by parent.")
    else:
        form = StudentLoginForm()
    return render(request, 'student/login.html', {'form': form})


def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')
    student = Student.objects.get(id=student_id)
    return render(request, 'student/dashboard.html', {'student': student})


def student_transactions(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('student_login')
    transactions = VendorTransaction.objects.filter(student=student).order_by('-timestamp')
    return render(request, 'student/transactions.html', {
        'student': student,
        'transactions': transactions
    })


def student_logout(request):
    request.session.flush()
    return redirect('student_login')


# -------------------- Vendor Views --------------------

def vendor_register(request):
    if request.method == 'POST':
        user_form = VendorRegisterForm(request.POST)
        profile_form = VendorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            vendor = profile_form.save(commit=False)
            vendor.user = user
            vendor.save()
            messages.success(request, "Vendor registered successfully.")
            return redirect('vendor_login')
    else:
        user_form = VendorRegisterForm()
        profile_form = VendorProfileForm()
    return render(request, 'vendor/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def vendor_login(request):
    if request.method == 'POST':
        form = VendorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is not None and hasattr(user, 'vendor'):
                    login(request, user)
                    return redirect('vendor_dashboard')
                else:
                    messages.error(request, "Invalid credentials or not a vendor.")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
    else:
        form = VendorLoginForm()
    return render(request, 'vendor/login.html', {'form': form})


def vendor_dashboard(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'vendor'):
        return redirect('vendor_login')
    return render(request, 'vendor/dashboard.html', {'vendor': request.user.vendor})


def vendor_payment(request):
    student = None
    if not request.user.is_authenticated or not hasattr(request.user, 'vendor'):
        return redirect('vendor_login')
    vendor = request.user.vendor
    if request.method == 'POST':
        form = VendorPaymentForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            amount = form.cleaned_data['amount']
            try:
                student = Student.objects.get(student_id=student_id)
                if student.wallet_balance >= amount:
                    student.wallet_balance -= amount
                    student.save()
                    VendorTransaction.objects.create(
                        vendor=vendor,
                        student=student,
                        amount=amount,
                        description="Purchase by vendor"
                    )
                    messages.success(request, f"₹{amount} deducted from {student.name}'s wallet.")
                    return redirect('vendor_transactions')
                else:
                    messages.error(request, "Insufficient balance in student's wallet.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
    else:
        form = VendorPaymentForm()
    return render(request, 'vendor/payment.html', {
        'form': form,
        'student': student
    })


def vendor_transactions(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'vendor'):
        return redirect('vendor_login')
    transactions = VendorTransaction.objects.filter(vendor=request.user.vendor).order_by('-timestamp')
    return render(request, 'vendor/transactions.html', {'transactions': transactions})


def vendor_logout(request):
    logout(request)
    return redirect('vendor_login')
