from django import forms
from .models import Expense, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category_cd', 'amount', 'description', 'date','payment_mode']
        # This adds a native HTML5 date picker calendar widget to the date field
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),"payment_mode": forms.Select(attrs={"class": "form-select",}),
            'category_cd': forms.Select(attrs={"class": "in"}),
            'amount': forms.NumberInput(attrs={'class': 'in','placeholder': 'Enter Amount','step': '1',}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category_cd"].empty_label = "Select Category"