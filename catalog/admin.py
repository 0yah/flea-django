from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Author, Genre,Book,BookInstance,Language

#admin.site.register(Author)
class BookItems(admin.TabularInline):
    model = Book


@admin.register(Author) #Does the same thing as admin.site.register(Author,AuthorAdmin)
class AuthorAdmin(admin.ModelAdmin):
    #Columns to be displayed in the administrator panel
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]
    inlines = [BookItems]



class BooksInstanceInline(admin.TabularInline):
    model = BookInstance



@admin.register(Book) #Does the same thing as admin.site.register(Book,BookAdmin)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]





@admin.register(BookInstance) #Does the same thing as admin.site.register(BookInstance,BookInstanceAdmin)
class BookInstanceAdmin(admin.ModelAdmin):
    #Displays a filter section on the adminstrator page
    list_filter = ('status', 'due_back')

    list_display = ('book', 'status', 'borrower', 'due_back', 'id')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
    


@admin.register(Genre) #Does the same thing as admin.site.register(Genre,GenreAdmin)
class GenreAdmin(admin.ModelAdmin):
    pass



"""
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Genre)

"""
admin.site.register(Language)


