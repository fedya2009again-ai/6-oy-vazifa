from django.db.models import Model
from django.shortcuts import render, redirect
from django.http import Http404, HttpRequest

from .models import Category, Book, Comment


def index(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    context = {
        'books': books,
        'categories': categories
    }
    return render(request, 'main/index.html', context)


def books_by_category(request, category_id):
    categories = Category.objects.all()
    books = Book.objects.filter(category_id=category_id)
    context = {
        "books": books,
        "categories": categories
    }
    return render(request, "main/index.html", context)


def detail(request, book_id):
    book = Book.objects.get(id=book_id)
    comments = Comment.objects.filter(book_id=book_id)
    context = {"book": book, 'comments':comments}
    return render(request, "main/detail.html", context)

def save_comment(request: HttpRequest, book_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            text = request.POST.get('text')
            book = Book.objects.get(id=book_id)
            comment = Comment.objects.create(text=text, book=book, user=request.user)
            return redirect('detail', book_id=book_id)
        else:
            return redirect('home')
    else:
        print('login qiling')
        return redirect('home')






