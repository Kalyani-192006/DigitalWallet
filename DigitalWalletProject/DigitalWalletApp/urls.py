from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parent_register/', views.parent_register, name='parent_register'),
    path('parent_login/', views.parent_login, name='parent_login'),
    # path('parent_logout/', views.logout_parent, name='logout_parent'),
    path('parentdashboard/', views.parentdashboard, name='parentdashboard'),
    # path('addstudent/', views.addstudent, name='addstudent'),
    # path('generate-qr/<int:student_id>/', views.generate_qr, name='generate_qr'),
    path('generate_qr/', views.generate_student_qr, name='generate_qr'), 
    path('fund_student/', views.fund_student, name='fund_student'),
    path('transaction_history', views.transaction_history, name='transaction_history'),
    path('parent_profile/', views.parent_profile, name='parent_profile'),
    path('parent_logout/', views.parent_logout, name='parent_logout'),
    path('student_login/', views.student_login, name='student_login'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),  
    path('student_transactions/', views.student_transactions, name='student_transactions'),
    path('student_logout/', views.student_logout, name='student_logout'),
    path('vendor_register/', views.vendor_register, name='vendor_register'),
    path('vendor_login/', views.vendor_login, name='vendor_login'),
    path('vendor_dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor_payment/', views.vendor_payment, name='vendor_payment'),
    path('vendor_transactions/', views.vendor_transactions, name='vendor_transactions'),
    path('vendor_logout/', views.vendor_logout, name='vendor_logout'),

]


