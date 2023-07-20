from django.shortcuts import render
from library.models import Book

def home(request):
    books = Book.objects.all()
    return render(request, 'home.html',{'books': books})


