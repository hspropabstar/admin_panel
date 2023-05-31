from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class FilmWork(UUIDMixin):
    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField('rating', blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    def __str__(self):
        return self.title

    class ContentType(models.TextChoices):
        MOVIE = 'movie', 'Movie'
        TV_SHOW = 'tv_show', 'TV Show'

    type = models.CharField(
        max_length=10,
        choices=ContentType.choices
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    certification = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')


    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"

class Person(UUIDMixin):
    full_name = models.TextField('full_name', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"person"

    def __str__(self):
        self.full_name

class PersonFilmWork(UUIDMixin):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    role = models.TextField('role', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"

    def __str__(self):
        self.role




