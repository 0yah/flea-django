from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse
from .models import Book,Author,BookInstance,Genre
from django.views import generic

# Create your views here.
def index(request):

    #Get the number of main objects from the models
    num_books =Book.objects.all().count()
    num_book_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()
    scifi_num_genre = Genre.objects.filter(name__iexact="Sci-Fi").count()

    #Get the number of available books (Status = 'a')
    num_book_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_visits = request.session.get('num_visits',1)
    request.session['num_visits'] = num_visits + 1


    #Dictonary that stores variables that can be used by the template

    context = {
        'num_books': num_books,
        'num_book_instances': num_book_instances,
        'num_book_instances_available': num_book_instances_available,
        'num_authors': num_authors,
        'num_sci_fi_genre':scifi_num_genre,
        'title':'Local Library',
        'num_visits':num_visits,
    }
    return render(request,'catalog/index.html',context=context)

class BookListView(generic.ListView):
    model = Book
    contex_object_name = "book_list"
    template_name = "catalog/books_list.html"

class BookDetailView(generic.DetailView):

    model = Book
    template_name = "catalog/books_detail.html"


class AuthorDetailView(generic.DetailView):

    model = Author
    template_name = "catalog/author_detail.html"

class AuthorListView(generic.ListView):
    model = Author
    contex_object_name = "author_list"
    template_name = "catalog/author_list.html"
    