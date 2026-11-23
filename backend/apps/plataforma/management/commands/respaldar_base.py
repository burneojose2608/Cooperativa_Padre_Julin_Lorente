import os
from pathlib import Path
import shutil
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help='Crea un respaldo privado PostgreSQL. No elimina respaldos anteriores.'
    def handle(self,*args,**options):
        ejecutable=getattr(settings,'PG_DUMP_BIN','') or shutil.which('pg_dump')
        if not ejecutable: raise CommandError('Configure PG_DUMP_BIN o incluya pg_dump en PATH.')
        db=settings.DATABASES['default']
        destino=Path(getattr(settings,'RESPALDOS_DIR',Path(settings.BASE_DIR)/'.backups')).resolve()
        destino.mkdir(parents=True,exist_ok=True)
        archivo=destino/f'cooperativa-{timezone.now():%Y%m%d-%H%M%S-%f}.dump'
        temporal=archivo.with_suffix('.partial')
        env=os.environ.copy();env['PGPASSWORD']=db.get('PASSWORD','')
        try:
            r=subprocess.run([str(ejecutable),'--host',db.get('HOST',''),'--port',str(db.get('PORT','5432')),
                '--username',db.get('USER',''),'--dbname',db['NAME'],'--format=custom','--file',str(temporal)],
                env=env,capture_output=True,timeout=600)
        except (OSError,subprocess.TimeoutExpired) as error:
            raise CommandError(f'No se completó el respaldo ({type(error).__name__}).') from None
        if r.returncode or not temporal.exists(): raise CommandError('pg_dump no completó el respaldo.')
        with temporal.open('rb') as f:
            if f.read(5)!=b'PGDMP': raise CommandError('El archivo no es un respaldo PostgreSQL válido.')
        temporal.replace(archivo)
        self.stdout.write(self.style.SUCCESS(f'Respaldo privado creado: {archivo.name}'))
