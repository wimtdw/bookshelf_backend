from books.models import Background
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserSerializer
from books.models import Shelf, Achievement
from books.models import Book, Genre
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    entry_author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    genres = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('entry_author',)

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        book = Book.objects.create(**validated_data)
        self._process_genres(book, genres_data)
        return book

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', [])
        instance = super().update(instance, validated_data)
        instance.genres.clear()
        self._process_genres(instance, genres_data)
        return instance

    def _process_genres(self, book, genres_data):
        for genre_name in genres_data:
            genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
            book.genres.add(genre)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genres'] = [genre.name for genre in instance.genres.all()]
        return data


class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = ['url']
        read_only_fields = ['url']


class ShelfSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    books = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    background_image = serializers.SlugRelatedField(
        slug_field='url',
        queryset=Background.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Shelf
        fields = [
            'id',
            'title',
            'owner',
            'description',
            'books',
            'background_image',
        ]

    def create(self, validated_data):
        books_data = validated_data.pop('books', [])
        shelf = Shelf.objects.create(**validated_data)
        shelf.books.set(books_data)
        return shelf

    def update(self, instance, validated_data):
        books_data = validated_data.pop('books', None)
        instance = super().update(instance, validated_data)

        if books_data:
            instance.books.set(books_data)
        return instance


class AchievementSerializer(serializers.ModelSerializer):
    is_new = serializers.BooleanField(read_only=True)
    users = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=True
    )

    class Meta:
        model = Achievement
        fields = [
            'name',
            'description',
            'emoji',
            'users',
            'is_new'
        ]


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'is_staff')


class UserSerializer(BaseUserSerializer):
    is_staff = serializers.BooleanField(read_only=True)  # Read-only field

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('is_staff',)
