from unittest.mock import MagicMock, patch
from django.test import SimpleTestCase
from django.test.runner import DiscoverRunner
from config.test_runner import RunnerConScriptsSQL


class SeguridadRunnerTests(SimpleTestCase):
    def test_pruebas_sin_base_no_ejecutan_sql_en_la_conexion_de_trabajo(self):
        conexion=MagicMock()
        conexion.settings_dict={'NAME':'cooperativa_db','TEST':{}}
        with patch('config.test_runner.connections') as conexiones, patch.object(DiscoverRunner,'setup_databases',return_value=[]):
            conexiones.all.return_value=[conexion]
            self.assertEqual(RunnerConScriptsSQL().setup_databases(aliases=set()),[])
        conexion.cursor.assert_not_called()

    def test_nombre_real_se_comprueba_despues_de_crear_base_aislada(self):
        conexion=MagicMock();conexion.alias='default'
        conexion.settings_dict={'NAME':'cooperativa_db','TEST':{}}
        with patch('config.test_runner.connections') as conexiones, patch.object(DiscoverRunner,'setup_databases',return_value=[]):
            conexiones.all.return_value=[conexion]
            with self.assertRaisesRegex(RuntimeError,'fuera de una base test_'):
                RunnerConScriptsSQL().setup_databases(aliases={'default'})
        conexion.cursor.assert_not_called()
