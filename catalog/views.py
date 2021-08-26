import datetime
from typing import ContextManager
from django.contrib.auth.models import Permission
from django.db import models
from django.db.models.base import Model
from django.forms.forms import Form
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book,BookCopy,Author,Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RenewBookForm,BookRenewModelForm
from django.urls import reverse,reverse_lazy



# Create your views here.


class BookListView(generic.ListView):
    model = Book
    paginate_by= 10
    context_object_name= "books"


class AuthorListView(generic.ListView):
    model = Author
    paginate_by =8
    context_object_name = "authors"


class GenreListView(generic.ListView):
    model = Genre
    paginate_by=8
    context_object_name = "genres"


class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorDetailView(generic.DetailView):
    model = Author


class GenreDetailView(generic.DetailView):
    model = Genre

def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_copies = BookCopy.objects.all().count()
    num_copies_available = BookCopy.objects.filter(status__exact='a').count 
    
    num_visits = request.session.get("num_visits",0) 
    num_visits += 1
    request.session["num_visits"]= num_visits


    context = {
        'num_books':num_books,
        'num_authors':num_authors,
        'num_copies':num_copies,
        'num_copies_available':num_copies_available,
        'num_visits': num_visits
    }

    return render(request,'index.html',context = context)


def author_book_list_view(request, author_id):
   author = Author.objects.get(pk = author_id)
   books = Book.objects.filter(author= author)

   context = {
       'author': author,
       'books': books
   }

   return render(request, "catalog/poet_detail.html", context=context)


class  LoanedCopiesByUserListView(LoginRequiredMixin,generic.ListView):
    models = BookCopy
    paginate_by = 10
    context_object_name = 'copies'
    template_name = "catalog/loaned_copies_by_user.html"

    def get_queryset(self):
        return BookCopy.objects.filter(borrower = self.request.user).filter(status = "o").order_by('due_back')


@login_required
def loaned_book_by_user(request):
    copies = BookCopy.objects.filter(borrower = request.user).filter(status = 'o').order_by('due_back')

    context = {'copies': copies}

    return render(request, "catalog/loaned_copies_by_user.html", context=context)


class LoanedBookListView(PermissionRequiredMixin,generic.ListView):
    model =  BookCopy
    permission_required = ('catalog.can_renew')
    paginate_by = 10
    context_object_name ='copies'
    template_name = "catalog/all_loaned_book.html"


    def get_queryset(self):
        return BookCopy.objects.filter(status = 'o').order_by('-due_back')


@login_required
@permission_required('catalog.can_renew', raise_exception=True)
def all_loaned_books(request):
    copies = BookCopy.objects.filter(status = 'o').order_by('due_back')
  

    context = {"copies": copies}


    return render(request,"catalog/all_loaned_book.html",context = context)

@login_required
@permission_required('catalog.can_renew', raise_exception=True)
def renew_book(request,pk):
    copy = get_object_or_404(BookCopy,pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            copy.due_back = form.cleaned_data['renew_date']
            copy.save()
            return HttpResponseRedirect( reverse("all_loaned_book"))
    else:
        proposed_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renew_date':proposed_date})

    context = {'form': form, 'copy': copy}
    return render(request, "catalog/book_renew.html", context=context)


def renew_bookcopy(request, pk):
   copy =  get_object_or_404(BookCopy,pk = pk)
   if request.method == 'POST':
       form = BookRenewModelForm(request.POST)
       if form.is_valid():
           copy.due_back = form.cleaned_data['due_back']
           copy.save()
           return HttpResponseRedirect(reverse('all_loaned_book'))
   else:
        proposed_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = BookRenewModelForm(initial={'due_back': proposed_date})
    
   context ={'copy':copy,'form':form}

   return render(request,"catalog/book_renew.html",context = context) 


class AuthorCreate(generic.CreateView):
    model = Author
    template_name = 'catalog/author_create.html'
    fields = ['first_name', 'last_name', 'birth_date', 'death_date']

class AuthorUpdate(generic.UpdateView):
    model = Author
    template_name = "catalog/author_update.html"
    fields = ['first_name','last_name','birth_date','death_date']
   

class AuthorDelete(generic.DeleteView):
    model =Author
    template_name ="catalog/author_delete.html"
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, generic.CreateView):
    model = Book
    template_name = "catalog/book_create.html"
    fields = ['title','author','genre','isbn','summary']
    permission_required = ('catalog.can_renew',)


class BookUpdate(generic.UpdateView):
    model = Book
    template_name = "catalog/book_update.html"
    fields=['title','author','genre','isbn','summary']


class BookDelete(generic.DeleteView):
    model = Book
    template_name = "catalog/book_delete.html"
    success_url = reverse_lazy('books')




