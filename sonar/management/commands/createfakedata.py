from datetime import datetime
from itertools import cycle

from django.core.management.base import BaseCommand
from faker import Faker

from sonar.models import ActivityLog, Post, User


fake = Faker(['en-US'])


class Command(BaseCommand):

    help = 'Load fake data (users, posts, activity Logs)'

    def handle(self, *args, **options):
        # First let's create the admin user.
        if not User.objects.filter(username='admin', is_superuser=True).exists():
            admin = User()
            admin.username = 'admin'
            admin.email = 'admin@admin'
            admin.set_password(admin.username)
            admin.is_staff = admin.is_superuser = True
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user created. Username: {admin.username} Password: {admin.username}'))  # noqa
        else:
            self.stdout.write(self.style.WARNING('Admin user already created.'))

        # Create random users.
        if not User.objects.exclude(is_superuser=True).exists():
            self.stdout.write('Creating random users. This could take a few seconds...')
            users = []
            for _ in range(99):
                profile = fake.simple_profile()
                user = User()
                user.username = profile['username']
                user.email = profile['mail']
                user.first_name = fake.first_name()
                user.last_name = fake.last_name()
                user.set_password(profile['username'])  # Bad idea, I know.
                users.append(user)
            User.objects.bulk_create(users)
            del users
            self.stdout.write(self.style.SUCCESS('Users created.'))
        else:
            self.stdout.write(self.style.WARNING('Users already created.'))

        # Create random posts.
        if not Post.objects.exists():
            self.stdout.write('Creating random posts. This could take a few seconds...')

            post_images = cycle([
                'https://images.unsplash.com/photo-1547586696-ea22b4d4235d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1679&q=80',  # noqa
                'https://images.unsplash.com/photo-1496128858413-b36217c2ce36?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1679&q=80',  # noqa
                'https://images.unsplash.com/photo-1492724441997-5dc865305da7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1679&q=80',  # noqa
            ])

            for _ in range(20):
                post = Post.objects.create(image_src=next(post_images), title=fake.catch_phrase(),
                                    description=fake.text())
                self.stdout.write(self.style.SUCCESS(f'Post "{post.title}" created.'))

        else:
            self.stdout.write(self.style.WARNING('Posts already created.'))

        # Create random activity.
        if not ActivityLog.objects.exists():
            random_users = User.objects.order_by('?')[:5]
            # Users start liking some post.
            random_post = Post.objects.order_by('?').first()
            for user in random_users:
                ActivityLog.objects.create(post=random_post, user=user, interaction_type=ActivityLog.LIKE)
            random_post = Post.objects.order_by('?').first()
            ActivityLog.objects.create(post=random_post, user=random_users[0], interaction_type=ActivityLog.LIKE)
            ActivityLog.objects.create(post=random_post, user=random_users[2], interaction_type=ActivityLog.LIKE)
            ActivityLog.objects.create(post=random_post, user=random_users[4], interaction_type=ActivityLog.LIKE)
            for _ in range(3):
                random_post = Post.objects.order_by('?').first()
                ActivityLog.objects.create(post=random_post, user=random_users[3], interaction_type=ActivityLog.LIKE)
            # Users start viewing some post.
            random_post = Post.objects.order_by('?').first()
            ActivityLog.objects.create(post=random_post, user=random_users[0], interaction_type=ActivityLog.VIEW)
            ActivityLog.objects.create(post=random_post, user=random_users[2], interaction_type=ActivityLog.VIEW)
            ActivityLog.objects.create(post=random_post, user=random_users[4], interaction_type=ActivityLog.VIEW)
            random_post = Post.objects.order_by('?').first()
            ActivityLog.objects.create(post=random_post, user=random_users[1], interaction_type=ActivityLog.VIEW)
            ActivityLog.objects.create(post=random_post, user=random_users[3], interaction_type=ActivityLog.VIEW)
            self.stdout.write(self.style.SUCCESS('Activity Logs created.'))
        else:
            self.stdout.write(self.style.WARNING('Activity Logs already created.'))
