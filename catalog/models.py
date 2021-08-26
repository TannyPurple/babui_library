from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
import datetime

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True, verbose_name='died')
    profile = models.TextField(max_length=2080, blank=True, null=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('author_detail',args = [str(self.id)])


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre_detail',args=[str(self.id)])


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,blank=True)
    genre = models.ManyToManyField(Genre)
    summary = models.TextField(max_length=2060, blank=True, null=True)
    isbn = models.CharField('isbn',max_length=255, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail',args=[str(self.id)])

    def display_no_copies(self):
        return BookCopy.objects.filter(book = self).count()

    display_no_copies.short_description = 'copies'

    def display_genres(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genres.short_description = 'Genres'

    
class BookCopy(models.Model):
    book = models.ForeignKey(Book,on_delete=models.RESTRICT)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    imprint =models.CharField(max_length=280)

    LOAN_STATUS = (
        ('a','Availability'),
        ('o','On Loan'),
        ('m','Maintainance'),
        ('r','Reserved')
    )

   
    status = models.CharField(max_length=1,default='m',choices=LOAN_STATUS)
    due_back = models.DateField(blank=True, null=True)
    borrower = models.ForeignKey(User,on_delete= models.SET_NULL,null= True, blank= True)

    class Meta:
        permissions =(
            ('can_mark_returned','set book as returned'),
            ('can_renew','extend renewal date')
        )
        
                
    def __str__(self):
        return f'{self.book} {self.id}'

    def is_overdue(self):
        return self.due_back and datetime.date.today() > self.due_back
