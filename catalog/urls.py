from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    #Author Routes
    path('author/', views.AuthorListView.as_view(), name='author'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    #Author Edit Routes
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    
    #Book Edit Routes
    path('author/create/', views.BookCreate.as_view(), name='book-create'),
    path('author/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('author/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    
    
    path('library/', views.LibrarianViewListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew', views.renew_book_librarian, name='renew-book-librarian'),
    
]

