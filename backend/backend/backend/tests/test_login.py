from django.test import TestCase, Client
from unittest.mock import patch

class LoginUsuarioTestCase(TestCase):
    @patch('backend.views.supabase')
    @patch('backend.views.enviar_codigo_whatsapp')
    def test_login_usuario_exitoso(self, mock_whatsapp, mock_supabase):
        # Datos de prueba
        email = 'test@correo.com'
        password_plano = '123456'
        password_hash = 'pbkdf2_sha256$...'  # Supón que es válido
        rol = 'Creador'

        # Simular respuesta de Supabase
        mock_supabase.table().select().eq().execute.return_value.data = [{
            'correo': email,
            'contrasenia': password_hash,
            'rol': rol,
            'telefono': '71234567',
            'idcreador': 1
        }]

        # Simular check_password devolviendo True
        from django.contrib.auth.hashers import make_password
        from django.contrib.auth.hashers import check_password
        password_hash = make_password(password_plano)
        mock_supabase.table().select().eq().execute.return_value.data[0]['contrasenia'] = password_hash

        # Simular código de WhatsApp
        mock_whatsapp.return_value = '123456'

        # Enviar POST
        client = Client()
        response = client.post('/login/', {
            'usuario': 'correo@ejemplo.com',
            'contrasenia': '123456',
            'rol': 'Creador'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json())
        self.assertEqual(response.json()['validador'], '123456')
        self.assertEqual(response.json()['rol'], rol)
