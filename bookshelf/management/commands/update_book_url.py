from django.core.management.base import BaseCommand, CommandError
from books.models import Background


class Command(BaseCommand):
    help = 'Updates the URL field of the books_background entry with id=5'

    def handle(self, *args, **options):
        try:
            background_entry = Background.objects.get(pk=5)
            original_url = background_entry.url
            background_entry.url = 'https://mir-s3-cdn-cf.behance.net/project_modules/1400/fcee6692300971.5e47d656aae59.jpg'  # Replace with the desired URL
            background_entry.save()

            self.stdout.write(self.style.SUCCESS(
                f'Successfully updated URL for background entry with id=5 from {original_url} to {background_entry.url}'))

        except Background.DoesNotExist:
            raise CommandError('Background entry with id=5 does not exist')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')
