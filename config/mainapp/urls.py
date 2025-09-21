from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard & Reports
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),

    # Profile & Password
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),

    # Expenses & Categories
    path('add_expense/', views.add_expense, name='add_expense'),
    path('category/', views.categories, name='category'),
    path('category/delete/<int:id>/', views.delete_category, name='delete_category'),  # delete category
]
