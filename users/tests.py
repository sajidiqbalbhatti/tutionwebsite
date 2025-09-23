from django.test import TestCase
from django.contrib.auth import get_user_model
from  users.models import User
from .models import LoginLog
# Create your tests here.

class UserModelTest(TestCase):
        
    def test_create_user_with_role(self):
        user=User.objects.create_user(username='student1',password='admin',role=User.STUDENT)
        self.assertEqual(user.username,'student1')
        self.assertEqual(user.role,User.STUDENT)
        self.assertTrue(user.check_password('admin'))
        
    def test_create_superuser(self):
        superuser = User.objects.create_superuser(username='admin', password='admin123')
        self.assertEqual(superuser.username, 'admin')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.role, User.ADMIN)
    
    def test_create_user_without_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='',password='erwer')
        
# __________LoginTestingCheck_________

class LoginLogModelTest(TestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username='student2' , password='admin123', role=User.STUDENT)
    
    def test_login_log_creation(self):
        log = LoginLog.objects.create(user=self.user)
        self.assertEqual(str(log),f'{self.user.username} logged in at {log.timestamp}')
        self.assertEqual(log.user.username, 'student2')
        

# _________View Testing_____

from django.urls import reverse

class UserListView(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1',password='password')
        
    def test_user_list_view_status_code(self):
        res = self.client.get(reverse('users:signup'))
        self.assertEqual(res.status_code, 200)
        
    def test_user_list_view_template(self):
        response = self.client.get(reverse('users:signup'))
        self.assertTemplateUsed(response,'users/signup.html')