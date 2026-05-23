import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Cria superusuário a partir de variáveis de ambiente, se não existir'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.WARNING('Variáveis de superusuário não definidas. Pulando.'))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superusuário "{username}" já existe. Pulando.'))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso!'))
