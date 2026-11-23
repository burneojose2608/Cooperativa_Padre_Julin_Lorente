from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings


class RespaldoTests(SimpleTestCase):
    def test_respaldo_se_publica_solo_tras_exito_de_pg_dump(self):
        with TemporaryDirectory() as directorio,override_settings(RESPALDOS_DIR=directorio,PG_DUMP_BIN='pg_dump'):
            def ejecutar(args,**kwargs):
                Path(args[args.index('--file')+1]).write_bytes(b'PGDMPcontenido-de-prueba')
                self.assertNotIn('PASSWORD',str(args))
                return SimpleNamespace(returncode=0)
            with patch('apps.plataforma.management.commands.respaldar_base.subprocess.run',side_effect=ejecutar):
                call_command('respaldar_base',stdout=StringIO())
            self.assertEqual(len(list(Path(directorio).glob('*.dump'))),1)
            self.assertEqual(list(Path(directorio).glob('*.partial')),[])

    def test_fallo_de_pg_dump_no_se_presenta_como_respaldo_correcto(self):
        with TemporaryDirectory() as directorio,override_settings(RESPALDOS_DIR=directorio,PG_DUMP_BIN='pg_dump'):
            with patch('apps.plataforma.management.commands.respaldar_base.subprocess.run',return_value=SimpleNamespace(returncode=1)):
                with self.assertRaises(CommandError):call_command('respaldar_base',stdout=StringIO())
            self.assertEqual(list(Path(directorio).glob('*.dump')),[])
