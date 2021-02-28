from datetime import datetime
from django.db import models
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse,reverse_lazy
from .models import Book,Author,BookInstance,Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import RenewBookForm
from django.contrib.auth.decorators import login_required,permission_required
from django.views.generic.edit import CreateView,UpdateView,DeleteView

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
    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    #Override default list view query
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o')


class LibrarianViewListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/librarian_view.html'
    permission_required = ('can_mark_returned')
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)


    if request.method == "POST":

        #Create a form instance and populate it with data from the request
        form = RenewBookForm(request.POST)

        #Check if the form is valid
        if form.is_valid():
            # Process the data in form.cleaned_data as required
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        #Set inital renewal date value
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})

    context = {
        'form':form,
        'book_instance':book_instance
    }

    return render(request,'catalog/book_renew_librarian.html',context)


"""
Overide the template form using


    template_name_suffix = '_update_form'

"""

class AuthorCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Author
    fields = [
        'first_name','last_name','date_of_birth','date_of_death'
    ]
    permission_required = ('can_add_author')
    #Set inital values
    initial = {'date_of_death':'11/06/2020'}

class AuthorUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Author
    permission_required = ('can_change_author','can_delete_author','can_view_author')
    fields = [
        'first_name','last_name','date_of_birth','date_of_death'
    ]

class AuthorDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Author
    permission_required = ('can_change_author','can_delete_author','can_view_author')
    success_url = reverse_lazy('authors')


class BookCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Book
    permission_required = ('can_change_book','can_delete_book','can_view_book')
    fields = [
        'title','author','language','summary','isbn','genre'
    ]

class BookUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Book
    permission_required = ('can_change_book','can_delete_book','can_view_book')
    fields = [
        'first_name','last_name','date_of_birth','date_of_death'
    ]

class BookDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Book
    permission_required = ('can_change_book','can_delete_book','can_view_book')
    success_url = reverse_lazy('books')
