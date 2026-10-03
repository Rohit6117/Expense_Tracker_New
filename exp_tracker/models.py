from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    # A unique category_cd to identify the category (e.g., 'FOOD', 'RENT', 'UTIL')
    category_cd = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100) # Display name (e.g., 'Food & Dining')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} ({self.category_cd})"


class Expense(models.Model):
    # Multi-user link: Keeps track of which user made the expense
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Links the expense to a Category using the category code/object
    category_cd = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, to_field='category_cd')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    payment_mode = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.category_cd_id}) on {self.date}"