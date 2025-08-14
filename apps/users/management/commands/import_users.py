import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.users.models import User


class Command(BaseCommand):
    """Команда для импорта пользователей из CSV файла."""

    help = 'Импорт пользователей из CSV файла'

    def handle(self, *args, **options):
        file_path = os.path.join(
            settings.BASE_DIR,
            'apps',
            'users',
            'fixtures',
            'users.csv'
        )

        try:

            with open(file_path, encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                users_count = 0
                for row in reader:
                    User.objects.create(
                        email=row['email'],
                        username=row['username'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    )
                    users_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Импортировано {users_count} пользователей'
                    )
                )

        except FileNotFoundError:
            raise CommandError(f'Файл не найден по пути: {file_path}')
        except Exception as error:
            raise CommandError(f'Ошибка при импорте: {str(error)}')
