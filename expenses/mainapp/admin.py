from django.contrib import admin
from .models import Expense, UserProfile, Category

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "category", "user", "date")
    list_filter = ("category", "user", "date")  # 🔹 user filter add chesa
    search_fields = ("title", "user__username")
    ordering = ("-date",)  # 🔹 latest expense first

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "address")
    search_fields = ("user__username", "phone")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")  # 🔹 show which user created the category
    search_fields = ("name", "user__username")
    list_filter = ("user",)
