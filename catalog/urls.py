from .import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('books/',views.BookListView.as_view(),name= 'books'),
    path('authors/',views.AuthorListView.as_view(),name='authors'),
    path('genres/',views.GenreListView.as_view(),name='genres'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name="book_detail"),
    path('author/<int:pk>/',views.AuthorDetailView.as_view(),name="author_detail"),
    path('poet/<int:author_id>/', views.author_book_list_view, name="poet_detail"),
    path('myborrowed/',views.LoanedCopiesByUserListView.as_view(),name="my_borrowed"),
    path('books/myborrowed/', views.loaned_book_by_user, name = 'loaned_to_user'),
    path('genre/<int:pk>/',views.GenreDetailView.as_view(),name="genre_detail"),
    path('allborrowed/',views.LoanedBookListView.as_view(),name="all_loaned_book"),
    path('books/allborrowed/',views.all_loaned_books,name="all_borrowed_book"),
    path('copy/<uuid:pk>/renew/', views.renew_book, name = "renew_book"),
    path('bookcopy/<uuid:pk>/renew/', views.renew_bookcopy, name="renew_bookcopy"),
    path('author/create/', views.AuthorCreate.as_view(), name = 'author_create'),
    path('author/update/<int:pk>/',views.AuthorUpdate.as_view(),name='author_update'),
    path('author/delete/<int:pk>/',views.AuthorDelete.as_view(),name='author_delete'),
    path('book/create/',views.BookCreate.as_view(),name='book_create'),
    path('book/update/<int:pk>/',views.BookUpdate.as_view(),name='book_update'),
    path('book/delete/<int:pk>/',views.BookDelete.as_view(),name='book_delete'),



]