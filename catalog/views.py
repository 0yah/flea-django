from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse
from .models import Book,Author,BookInstance,Genre

# Create your views here.
def index(request):

    #Get the number of main objects from the models

    num_books =Book.objects.all().count()
    num_book_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()
    scifi_num_genre = Genre.objects.filter(name__iexact="Sci-Fi").count()

    #Get the number of available books (Status = 'a')
    num_book_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    
    #Dictonary that stores variables that can be used by the template

    context = {
        'num_books': num_books,
        'num_book_instances': num_book_instances,
        'num_book_instances_available': num_book_instances_available,
        'num_authors': num_authors,
        'num_sci_fi_genre':scifi_num_genre,
        'title':'Local Library'
    }
    return render(request,'catalog/index.html',context=context)
