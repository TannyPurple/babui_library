from django.contrib import admin
from .models import Book,BookCopy,Genre,Author


# Register your models here.

class BookCopyInlines(admin.TabularInline):
    model = BookCopy
    extra = 0



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_no_copies','display_genres')
    list_filter = ('author','genre')
    fieldsets= (
        ('Section 1',{'fields':('title','author','genre')}),
        ('Section 2',{'fields':('isbn','summary')})
    )
    inlines = [BookCopyInlines,]


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display= ('id','book','status','due_back')
    list_filter =('status','due_back')
    fieldsets= (
        ('Genaral',{'fields':('id','book','imprint',)}),
        ('Availability',{'fields':('status','due_back','borrower')})
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display= ('__str__', 'birth_date', 'death_date')
    fields = (('first_name','last_name'), 'profile', ('birth_date','death_date'))

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass