from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Cria os grupos padrão do sistema'

    def handle(self, *args, **kwargs):
        grupos = ['ADMIN', 'SUPERVISOR', 'TECNICO', 'USUARIO']
        
        for grupo_nome in grupos:
            grupo, created = Group.objects.get_or_create(name=grupo_nome)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{grupo_nome}" criado com sucesso!'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{grupo_nome}" já existe.'))