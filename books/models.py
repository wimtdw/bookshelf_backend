from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название жанра"
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name


class Background(models.Model):
    url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Фоновое изображение",
        help_text="URL изображения для фона полки"
    )


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=100, verbose_name="Автор")
    publication_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Год публикации"
    )
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name="Жанры"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    entry_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    cover = models.URLField(
        null=True,
        blank=True,
        verbose_name="Обложка"
    )
    order = models.IntegerField(default=100, verbose_name="Порядок")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.author}"


class Shelf(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название полки")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shelves',
        verbose_name="Владелец"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание полки"
    )
    books = models.ManyToManyField(
        'Book',
        related_name='shelves',
        blank=True,
        verbose_name="Книги на полке"
    )
    background_image = models.ForeignKey(
        Background, verbose_name="Фон", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Полка"
        verbose_name_plural = "Полки"
        ordering = ['-created_at', 'title']

    def __str__(self):
        return f"{self.title} ({self.owner.username})"


class Achievement(models.Model):
    emoji = models.CharField(max_length=5, verbose_name="Эмодзи")
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.CharField(max_length=200, verbose_name="Описание")
    users = models.ManyToManyField(User, verbose_name="Достижения", blank=True)

    def __str__(self):
        return f"{self.emoji} {self.name}"

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"
