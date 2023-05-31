from django.contrib import admin
from .models import Genre, FilmWork, GenreFilmWork

# Register your models here.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmWork

@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)

    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified', )

    list_filter = ('type', )

    search_fields = ('title', 'description', 'id')



