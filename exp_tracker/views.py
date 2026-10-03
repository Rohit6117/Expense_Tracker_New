from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from .forms import CategoryForm, ExpenseForm
from django.db.models import Sum
from django.utils import timezone
from django.core.paginator import Paginator
import json

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register_user.html', {'form': form})


@login_required(login_url='login')
def dashboard_view(request):
    # Filter expenses and categories so users only see their own data
    # .select_related('category_cd') performs an SQL JOIN to fetch the category details at the same time
    user_expenses = Expense.objects.filter(user=request.user).select_related('category_cd')
    categories = Category.objects.all()
    total_expenses = ( user_expenses.aggregate( total=Sum('amount') )['total'] or 0 )
    total_transactions = user_expenses.count()
    
    today = timezone.localdate()
    today_expenses = ( user_expenses .filter(date=today) .aggregate( total=Sum('amount') )['total'] or 0 )
    
    current_month_expenses = ( user_expenses .filter( date__year=today.year, date__month=today.month ) .aggregate( total=Sum('amount') )['total'] or 0 )

    category_expenses = ( user_expenses .values( 'category_cd__name' ) .annotate( total=Sum('amount') ) .order_by('-total') )
    category_labels = [
        item["category_cd__name"]
        for item in category_expenses
    ]
    category_data = [
        float(item["total"])
        for item in category_expenses
    ]
    context = {
        'expenses': user_expenses,
        'categories': categories,
        'total_expenses': total_expenses,
        'total_transactions': total_transactions,
        'today_expenses': today_expenses,
        'current_month_expenses': current_month_expenses,

        # 'category_expenses': category_expenses,
        "category_labels": json.dumps(category_labels),
        "category_data": json.dumps(category_data),

    }
    return render(request, 'dashboard.html', context)

@login_required(login_url="login") 
def exp_transaction(request): 
    expenses = Expense.objects.filter( user=request.user ).select_related("category_cd").order_by("-date")
    search = request.GET.get("search", "").strip() 
    if search: expenses = expenses.filter( description__icontains=search ) | expenses.filter( category_cd__name__icontains=search )
    selected_category = request.GET.get("category", "") 
    if selected_category: expenses = expenses.filter( category_cd_id=selected_category ) 
    payment_mode = request.GET.get("payment_mode", "") 
    if payment_mode: expenses = expenses.filter( payment_mode=payment_mode )
    from_date = request.GET.get("from_date", "") 
    if from_date: expenses = expenses.filter( date__gte=from_date ) 

    to_date = request.GET.get("to_date", "")
    if to_date: expenses = expenses.filter( date__lte=to_date ) 
    categories = Category.objects.all() 
    
    paginator = Paginator(expenses, 10) 
    page_number = request.GET.get("page") 
    page_obj = paginator.get_page(page_number)
    context = { 
            # "expenses": expenses,
            "expenses": page_obj, 
            "page_obj": page_obj,
            "categories": categories, 
            "search": search, 
            "selected_category": selected_category, 
            "payment_mode": payment_mode, 
            "from_date": from_date, 
            "to_date": to_date, 
            } 
    return render( request, "transactions.html", context )    

@login_required(login_url='login')
def add_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    categories = Category.objects.all().order_by("name")
    return render(request, 'add_category.html', {'form':form,"categories": categories,})
    

@login_required(login_url='login')
def add_expense_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user   # Automatically assign the logged-in user!
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form':form})


@login_required(login_url="login")
def delete_category(request, category_cd):

    if request.method == "POST":

        category = Category.objects.get(
            category_cd=category_cd
        )

        category.delete()

    return redirect("add_category")

@login_required(login_url="login")
def delete_expense(request, expense_id):

    if request.method == "POST":

        expense = Expense.objects.get(
            id=expense_id,
            user=request.user
        )
        expense.delete()

    return redirect("transactions")
 