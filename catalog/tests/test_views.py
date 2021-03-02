from logging import setLoggerClass
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.urls.base import resolve
import datetime
from django.utils import timezone
from django.contrib.auth.models import Permission, User
from catalog.models import Author,BookInstance, Book, Genre, Language
import uuid

class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username="testuser1",password="jkj#$DVFVd")
        test_user2 = User.objects.create_user(username="testuser2",password="jkj#$DVFVd")

        test_user1.save()
        test_user2.save()

        permission =Permission.objects.get(name="Set book as returned")

        test_user2.user_permissions.add(permission)
        test_user2.save()

        #Create a book
        test_author = Author.objects.create(first_name="John",last_name="Doe")
        test_genre = Genre.objects.create(name="Fantasy")
        test_language = Language.objects.create(name="English")
        test_book = Book.objects.create(
            title="Book Title",
            summary="My Book summary",

            isbn="AKKJKJ",
            author=test_author,
            language=test_language
        )


        #Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        #Create a bookinstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.testbookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint="Unlikely Imprint, 2016",
            due_back=return_date,
            borrower=test_user1,
            status="o"
        )

        #Create a bookinstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.testbookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint="Unlikely Imprint, 2016",
            due_back=return_date,
            borrower=test_user2,
            status="o"
        )


class LoanedBookInstanceByUserListViewTest(TestCase):
    def setUp(self):

        #Create Two users
        test_user1 = User.objects.create_user(username="testuser1",password="sdjnHH7*@jdsSD")
        test_user2 = User.objects.create_user(username="testuser2",password="sdjnHH7*@jdsSD")

        test_user1.save()
        test_user2.save()
        
        # Create a book 
        test_author =Author.objects.create(first_name="John",last_name="Smith")
        test_genre = Genre.objects.create(name="Fantasy")
        test_language = Language.objects.create(name="English")
        test_book = Book.objects.create(
            title="Book Title",
            summary="My book summary",
            isbn="sduuui",
            author=test_author,
            language=test_language
        )

        # Create Genre as a post step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) #Assignment of many to many type is not allowed

        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status= 'm'
            BookInstance.objects.create(
                book=test_book,
                imprint="Unlikely Imprint 2016",
                due_back=return_date,
                borrower=the_borrower,
                status=status
            )
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(response,'/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1",password="sdjnHH7*@jdsSD")
        response = self.client.get(reverse('my-borrowed'))

        #Is the user logged in??
        self.assertEqual(str(response.context['user']),'testuser1')

        #Was the response successful?
        self.assertEqual(response.status_code,200)

        # Is the correct template used
        self.assertTemplateUsed(response,'catalog/bookinstance_list_borrowed_user.html')

class AuthorListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f"Christian {author_id}",
                first_name=f"Surname {author_id}",
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code,200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code,200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 10)

    def test_lists_all_authors(self):

        response = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(response.status_code,200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 3)