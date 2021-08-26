import datetime
from django.utils import timezone
from django.db import reset_queries
from django.http import response
from django.test import TestCase
from django.urls import reverse
from catalog.models import Author,BookCopy,Book,Genre
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import Permission 

class AuthorListViewTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        num_authors = 13

        for author_id in range(num_authors):
            Author.objects.create(first_name = f"Mahbub{author_id}", last_name = f"Huq{author_id}",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertTrue(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertTrue(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response,'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertTrue(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['authors']), 8)

    def test_list_all_authors(self):
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertTrue(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['authors']), 5)

    
class LoanedBookCopyByUserListViewTestcase(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username="testuser1",password = "abc123")
        test_user2 = User.objects.create_user(username="testuser2",password = "abc123")

        test_user1.save()
        test_user2.save()

        test_author = Author.objects.create(first_name ="ruku",last_name = "vusu")
        test_genre = Genre.objects.create(name = "fantasy")
        test_book =Book.objects.create(title ="Rukusdairy",summary = "bla blah blah",isbn = "abcd",author = test_author)
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()


        num_copies = 30
        for book_copy in range(num_copies):
            return_date = timezone.localtime()+datetime.timedelta(days = book_copy % 5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = "m"
            BookCopy.objects.create(book= test_book,imprint = "1st edition",due_back = return_date,borrower = the_borrower,status=status)


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("my_borrowed"))
        self.assertRedirects(response,"/accounts/login/?next=/catalog/myborrowed/")


    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1",password = "abc123")
        response = self.client.get(reverse("my_borrowed"))
        self.assertEqual(str(response.context['user']),"testuser1")
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"catalog/loaned_copies_by_user.html")
        

    
    
    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='abc123')
        response = self.client.get(reverse('my_borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('copies' in response.context)
        self.assertEqual(len(response.context['copies']), 0)


        books = BookCopy.objects.all()[:10]

        for book in books:
            book.status = 'o'
            book.save()
        
        response = self.client.get(reverse('my_borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('copies' in response.context)

        for bookitem in response.context['copies']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual(bookitem.status, 'o')


    def test_pages_ordered_by_due_date(self):

        for book in BookCopy.objects.all():
            book.status='o'
            book.save()

        login = self.client.login(username='testuser1', password='abc123')
        response = self.client.get(reverse('my_borrowed'))
    
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
    
        self.assertEqual(len(response.context['copies']), 10)

        last_date = 0
        for book in response.context['copies']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back    


class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        permission = Permission.objects.get(name='extend renewal date')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
        )
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookCopy.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user1,
            status='o',
        )
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookCopy.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user2,
            status='o',
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew_book', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('renew_book', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_book', kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_book', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_book', kwargs={'pk':test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_book', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_renew.html')