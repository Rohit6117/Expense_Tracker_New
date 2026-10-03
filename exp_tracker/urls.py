from django.urls import path
from django.contrib.auth import views as auth_views
from .views import add_category_view, add_expense_view, register_view, dashboard_view, exp_transaction, delete_category, delete_expense


urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name='logout'),
    
    # New URLs for adding data
    path('add-category/', add_category_view, name='add_category'),
    path('add-expense/', add_expense_view, name='add_expense'),
    path('transactions/', exp_transaction, name='transactions'), 
    path('delete-category/<int:category_cd>/', delete_category,name="delete_category"),
    path("delete-expense/<int:expense_id>/",delete_expense,name="delete_expense"),
]
