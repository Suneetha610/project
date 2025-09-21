from django.db import models
from django.contrib.auth.models import User


# 🔹 Category Model (user-specific)
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user-wise categories
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'name')  # same user can't add duplicate category

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# 🔹 Expense Model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # linked to Category
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} in {self.category.name}"


# 🔹 UserProfile for extra details + Budget fields
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # 🔹 Budget details
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    savings = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.user.username
