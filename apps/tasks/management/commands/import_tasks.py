import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.tasks.models import Category, Tag, Task
from apps.users.models import User


class Command(BaseCommand):
    """Команда для импорта задач, категорий и тегов из CSV файлов."""

    help = 'Импорт задач, категорий, тегов и их связей из CSV файлов'

    def handle(self, *args, **options):
        fixtures_dir = os.path.join(
            settings.BASE_DIR,
            'apps',
            'tasks',
            'fixtures'
        )
        files = {
            'categories': os.path.join(fixtures_dir, 'categories.csv'),
            'tags': os.path.join(fixtures_dir, 'tags.csv'),
            'tasks': os.path.join(fixtures_dir, 'tasks.csv'),
            'task_tags': os.path.join(fixtures_dir, 'task_tags.csv'),
        }

        try:

            with open(files['categories'], encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                categories_count = 0
                for row in reader:
                    Category.objects.create(
                        title=row['title'],
                        slug=row['slug'],
                        owner=User.objects.get(id=row['owner_id'])
                    )
                    categories_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Импортировано {categories_count} категорий'
                    )
                )

            with open(files['tags'], encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                tags_count = 0
                for row in reader:
                    Tag.objects.create(
                        title=row['title'],
                        slug=row['slug'],
                        owner=User.objects.get(id=row['owner_id'])
                    )
                    tags_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Импортировано {tags_count} тегов')
                )

            with open(files['tasks'], encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                tasks_count = 0
                for row in reader:
                    Task.objects.create(
                        title=row['title'],
                        slug=row['slug'],
                        owner=User.objects.get(id=row['owner_id']),
                        description=row['description'],
                        is_done=row['is_done'].lower() == 'true',
                        deadline=datetime.strptime(
                            row['deadline'], '%Y-%m-%d'
                        ).date() if row['deadline'] else None,
                        priority=row['priority'],
                        category=Category.objects.get(
                            id=row['category_id']
                        ) if row['category_id'] else None,
                    )
                    tasks_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Импортировано {tasks_count} задач')
                )

            with open(files['task_tags'], encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                relations_count = 0
                for row in reader:
                    task = Task.objects.get(id=row['task_id'])
                    tag = Tag.objects.get(id=row['tag_id'])
                    task.tags.add(tag)
                    relations_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Добавлено {relations_count} связей задач с тегами'
                    )
                )

        except FileNotFoundError as e:
            raise CommandError(f'Файл не найден: {e.filename}')
        except User.DoesNotExist:
            raise CommandError('Указанный пользователь не существует')
        except Category.DoesNotExist:
            raise CommandError('Указанная категория не существует')
        except Tag.DoesNotExist:
            raise CommandError('Указанный тег не существует')
        except Task.DoesNotExist:
            raise CommandError('Указанная задача не существует')
        except Exception as error:
            raise CommandError(f'Ошибка при импорте: {str(error)}')
