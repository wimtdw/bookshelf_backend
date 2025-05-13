from rest_framework import generics, filters
from .serializers import CustomUserSerializer
from .serializers import BackgroundSerializer
import re
from googletrans import Translator
import requests
import random
from rest_framework.views import APIView
from urllib.parse import quote
from .serializers import AchievementSerializer
from books.models import Achievement, Background, Shelf
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from books.models import Book
from .serializers import BookSerializer, ShelfSerializer
from rest_framework import viewsets, exceptions
from django.contrib.auth import get_user_model
from django.db.models import Max
from rest_framework.pagination import PageNumberPagination

User = get_user_model()
translator = Translator()


class BackgroundViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    ViewSet только для чтения (GET-запросы)
    Позволяет получить список всех фоновых изображений или отдельное изображение
    '''
    queryset = Background.objects.all()
    serializer_class = BackgroundSerializer


class BookViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для управления книгами
    '''
    serializer_class = BookSerializer

    def get_queryset(self):
        '''
        Возвращает queryset только для книг, созданных текущим пользователем.
        '''
        username = self.request.GET.get('username')
        if username:
            user = User.objects.get(username=username)
        else:
            user = self.request.user

        shelf_id = self.request.GET.get('shelf_id')
        queryset = Book.objects.filter(entry_author=user)

        if shelf_id:
            try:
                shelf_id = int(shelf_id)
                shelf = Shelf.objects.get(pk=shelf_id)
                queryset = queryset.filter(shelves=shelf)
            except ValueError:
                return Book.objects.none()
            except Shelf.DoesNotExist:
                return Book.objects.none()
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        max_order = Book.objects.filter(
            entry_author=user).aggregate(Max('order'))['order__max']
        new_order = max_order + 1 if max_order else 1
        serializer.save(entry_author=user, order=new_order)

    def perform_update(self, serializer):
        if (not self.request.user.is_staff and
                serializer.instance.entry_author != self.request.user):
            raise exceptions.PermissionDenied(
                'Изменение чужого контента запрещено!')
        serializer.save(entry_author=self.request.user)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        if (not self.request.user.is_staff and
                instance.entry_author != self.request.user):
            raise exceptions.PermissionDenied(
                'Удаление чужого контента запрещено!')
        instance.delete()


class ShelfViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для управления полками
    '''
    serializer_class = ShelfSerializer

    def get_queryset(self):
        '''
        Возвращает queryset только для полок, созданных текущим пользователем.
        '''
        username = self.request.GET.get('username')
        if username:
            user = User.objects.get(username=username)
            return Shelf.objects.filter(owner=user)
        else:
            return Shelf.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    def perform_update(self, serializer):
        if (not self.request.user.is_staff and
                serializer.instance.owner != self.request.user):
            raise exceptions.PermissionDenied(
                'Изменение чужого контента запрещено!')
        serializer.save(owner=self.request.user)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        if (not self.request.user.is_staff and
                instance.owner != self.request.user):
            raise exceptions.PermissionDenied(
                'Удаление чужого контента запрещено!')
        instance.delete()


class UserListView(generics.ListAPIView):
    '''
    ViewSet для поиска пользователей
    '''
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['^username']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('random') == 'True':
            user_ids = queryset.values_list('id', flat=True)
            if user_ids:
                random_id = random.choice(user_ids)
                return queryset.filter(id=random_id)
            else:
                return queryset.none()
        return queryset


class AchievementViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для получения достижений и связывания достижения с пользователем
    '''
    serializer_class = AchievementSerializer
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if username:
            return Achievement.objects.filter(users__username=username)
        return Achievement.objects.all()

    def partial_update(self, request, *args, **kwargs):
        achievement = self.get_object()
        user = request.user
        is_new = False

        if not achievement.users.filter(pk=user.pk).exists():
            achievement.users.add(user)
            is_new = True

        serializer = self.get_serializer(achievement)
        return Response({
            **serializer.data,
            'is_new': is_new
        }, status=status.HTTP_200_OK)


class OpenLibrarySearch(APIView):
    '''
    ViewSet для запроса данных о книге с API
    '''

    def get(self, request):
        search_title = request.GET.get('title', '')
        if not search_title:
            return Response({'error': 'Необходим параметр title'}, status=400)
        search_desc = request.GET.get(
            'search_description', 'true').lower() != 'false'
        try:
            translated_title = self._translate_text(search_title, 'en')
            book_data, work_id = self._search_books(translated_title)
            editions = self._get_editions(work_id)
            result = self._process_editions_data(
                editions, book_data, search_title, search_desc)

            return Response(result)
        except ValueError as e:
            return Response({'error': str(e)}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def _translate_text(self, text, target_lang):
        '''Helper method for text translation'''
        if not text:
            return ''
        try:
            translation = translator.translate(text, dest=target_lang)
            return translation.text
        except Exception as e:
            print(f'Translation error: {e}')
            return text

    def _search_books(self, translated_title):
        '''Search for books on OpenLibrary'''
        encoded_title = quote(translated_title.encode('utf-8'))
        url = f"https://openlibrary.org/search.json?title={encoded_title}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not data.get('docs'):
            raise ValueError('Книга не найдена')

        book_data = data['docs'][0]
        return book_data, book_data['key']

    def _get_editions(self, work_id):
        '''Get editions data for a work'''
        url = f"https://openlibrary.org/{work_id}/editions.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("entries", [])

    def _process_editions_data(self, editions, book_data, original_title, search_desc=True):
        '''Process editions data to build final result'''
        description, subjects = self._extract_metadata(
            editions, include_description=search_desc)
        physical_book_data = self._find_physical_book(editions)

        description_text = (
            self._clean_and_translate_description(description)
            if search_desc
            else ''
        )

        return {
            'title': self._format_title(original_title),
            'author': self._translate_author(book_data.get('author_name', [])),
            'publication_date': book_data.get('first_publish_year', ''),
            'description': description_text,
            'subjects': self._process_subjects(subjects),
            'cover': self._get_cover_url(physical_book_data, book_data)
        }

    def _extract_metadata(self, editions, include_description=True):
        '''Extract description and subjects from editions'''
        description = ''
        subjects = set()

        for edition in editions:
            if include_description and not description and 'description' in edition:
                desc = edition['description']
                description = desc.get('value', desc) if isinstance(
                    desc, dict) else desc

            if 'subjects' in edition:
                subjects.update(edition['subjects'])

        return description, subjects

    def _find_physical_book(self, editions):
        '''Find appropriate physical book data (prefer Russian editions)'''
        russian_editions = [
            edition for edition in editions
            if any(lang.get('key') == '/languages/rus'
                   for lang in edition.get('languages', []))
        ]
        return russian_editions[0] if russian_editions else editions[0]

    def _get_cover_url(self, edition, book_data):
        '''Get cover image URL'''
        cover_id = edition.get('covers', [book_data.get('cover_i', '')])[0]
        return f'https://covers.openlibrary.org/b/id/{cover_id}-L.jpg' if cover_id else None

    def _translate_author(self, author_names):
        '''Translate author names to Russian'''
        return self._translate_text(', '.join(author_names), 'ru') if author_names else ''

    def _clean_and_translate_description(self, description):
        '''Clean and translate description text'''
        if not description:
            return ''
        cleaned = re.sub(r'[^a-zA-Z.\s]+', '', str(description))
        cleaned = re.sub(r"\s*back cover\s*", "", cleaned, flags=re.IGNORECASE)
        return self._translate_text(cleaned, 'ru')

    def _process_subjects(self, subjects):
        '''Process and translate subjects'''
        processed = set()
        for subject in subjects:
            for sub in subject.split(',.'):
                sub = sub.strip()
                if len(sub.split()) == 1:
                    translated = self._translate_text(
                        sub, 'ru').strip().lower()
                    processed.add(translated)
        return list(processed) or None

    def _format_title(self, title):
        '''Format title with capitalized words'''
        return title.title()
