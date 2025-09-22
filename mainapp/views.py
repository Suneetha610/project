from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from django import forms

from .models import Expense, UserProfile, Category
from .forms import UserProfileForm


# ✅ Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category']


# ✅ Welcome Page
def welcome(request):
    return render(request, 'welcome.html')


# ✅ Signup
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Signup successful! ✅")
            return redirect('dashboard')
    return render(request, 'signup.html')


# ✅ Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


# ✅ Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully ✅")
    return redirect('login')


# ✅ Dashboard
@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    today = now().date()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    today_expense = expenses.filter(date__date=today).aggregate(total=Sum('amount'))['total'] or 0
    yesterday_expense = expenses.filter(date__date=yesterday).aggregate(total=Sum('amount'))['total'] or 0
    last_7_days_expense = expenses.filter(date__date__gte=last_7_days).aggregate(total=Sum('amount'))['total'] or 0
    last_30_days_expense = expenses.filter(date__date__gte=last_30_days).aggregate(total=Sum('amount'))['total'] or 0
    current_year_expense = expenses.filter(date__year=today.year).aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0

    profile = UserProfile.objects.filter(user=request.user).first()

    context = {
        'today_expense': today_expense,
        'yesterday_expense': yesterday_expense,
        'last_7_days_expense': last_7_days_expense,
        'last_30_days_expense': last_30_days_expense,
        'current_year_expense': current_year_expense,
        'total_expenses': total_expenses,
        'categories_count': expenses.values('category').distinct().count(),
        'users_count': User.objects.count(),
        'profile': profile,
    }
    return render(request, 'dashboard.html', context)


# ✅ Reports
@login_required
def reports(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'reports.html', {'expenses': expenses})


# ✅ Profile
@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully! ✅")
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile!")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})


# ✅ Change Password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully! ✅")
            return redirect('dashboard')
        else:
            messages.error(request, "Error changing password.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


# ✅ Add Expense with Budget Check
@login_required
def add_expense(request):
    categories = Category.objects.filter(user=request.user)
    profile = UserProfile.objects.filter(user=request.user).first()

    if request.method == "POST":
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')

        if title and amount and category_id:
            category = get_object_or_404(Category, id=category_id, user=request.user)
            expense = Expense.objects.create(
                user=request.user,
                title=title,
                amount=amount,
                category=category
            )

            # 🔹 Budget Check
            total_expenses = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
            if profile and profile.monthly_limit and total_expenses > profile.monthly_limit:
                messages.warning(request, "⚠️ You have exceeded your monthly limit!")
                # JS beep will be triggered from template
            else:
                messages.success(request, "Expense added successfully! ✅")

            return redirect('add_expense')
        else:
            messages.error(request, "Please fill all fields!")

    return render(request, 'add_expense.html', {'categories': categories, 'profile': profile})


# ✅ Manage Categories
@login_required
def categories(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            if Category.objects.filter(user=request.user, name=name).exists():
                messages.error(request, "This category already exists.")
            else:
                Category.objects.create(user=request.user, name=name)
                messages.success(request, "Category added successfully! ✅")
            return redirect("category")

    cats = Category.objects.filter(user=request.user)
    return render(request, "category.html", {"category": cats})


# ✅ Delete Category
@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id, user=request.user)
    category.delete()
    messages.success(request, "Category deleted successfully! ❌")
    return redirect('category')
