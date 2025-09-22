from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'phone', 'address', 'total_amount', 'savings', 'monthly_limit']  # ✅ Extra fields add chesam
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter your address',
                'rows': 3,
                'class': 'form-control'
            }),
            'total_amount': forms.NumberInput(attrs={
                'placeholder': 'Enter your monthly income',
                'class': 'form-control'
            }),
            'savings': forms.NumberInput(attrs={
                'placeholder': 'Enter your savings',
                'class': 'form-control'
            }),
            'monthly_limit': forms.NumberInput(attrs={
                'placeholder': 'Enter your monthly budget limit',
                'class': 'form-control'
            }),
        }
