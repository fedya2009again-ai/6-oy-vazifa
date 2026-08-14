from django.db.models import Model
from django.shortcuts import render, redirect
from django.http import Http404, HttpRequest

from .models import Category, Book, Comment
from .forms import CommentForm

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
    context = {
        "book": book,
        'comments':comments
    }
    return render(request, "main/detail.html", context)

def save_comment(request: HttpRequest, book_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
           #text = request.POST.get('text')
           form = CommentForm(data=request.POST)
           if form.is_valid():
                book = Book.objects.get(id=book_id)
                comment = Comment.objects.create(text=form.cleaned_data.get("text"), book=book, user=request.user)
           else:
               print('simvollar soni 500 tadan kop')
           return redirect('detail', book_id=book_id)
        else:
            return redirect('home')
    else:
        print('login qiling')
        return redirect('home')

def update_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user.is_authenticated and request.user == comment.user:
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment.text = form.cleaned_data.get("text")
                comment.save()
                return redirect('detail', book_id=comment.book.id)
        else:
            form = CommentForm(initial={"text": comment.text})
        context = {
            "form": form
        }
        return render(request, "main/comment_update.html", context)
    else:
        print('login qiling')
        return redirect('home')



def delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user.is_authenticated and request.user == comment.user or request.user.is_superuser:
        book_id = comment.book.id
        if request.method == "POST":
            comment.delete()
            return redirect('detail', book_id=book_id)
        else:
            return render(request, 'main/coniform_delete.html', {"comment":comment})
    else:
        print('login qiling')
        return redirect('home')



