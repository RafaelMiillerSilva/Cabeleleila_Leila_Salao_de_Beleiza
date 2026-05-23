import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Cria ou corrige superusuário a partir de variáveis de ambiente'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.WARNING('Variáveis não definidas. Pulando.'))
            return

        user, created = User.objects.get_or_create(username=username)
        
        user.email = email
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" corrigido!'))