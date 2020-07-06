from django.shortcuts import render
from .models import Category, Item 
# Create your views here.

def menu(request):
    categories = Category.objects.all()
    context = { 'categories': categories }
    return render(request, 'items/menu.html', context)