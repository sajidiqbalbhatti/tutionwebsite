from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import LearningModeOption, Category,Level,Course,Subject
from datetime import date
from users.models import User

from datetime import date

# Create your tests here.

User = get_user_model()

class ModelTestCase(TestCase):
    
    def setUp(self):
       self.user= User.objects.create_user(username='testuser', password='testpassword')
       self.learning_mode = LearningModeOption.objects.create(mode='online')
       
       self.category = Category.objects.create(name='math', description='ABC')
       
       self.level = Level.objects.create(name='grade 10')
       
       self.subject = Subject.objects.create(level=self.level,subject_name='Python')

    def test_learning_mode_option_creation(self):
        self.assertEqual(str(self.learning_mode),'online')
        
    
    def test_category_creation(self):
        self.assertEqual(str(self.category),'math')
        
    def test_level_creation(self):
        self.assertEqual(str(self.level),'grade 10')
        
    def test_subject_creation(self):
        self.assertEqual(str(self.subject),'grade 10 - Python')
    
    def test_course_creation(self):
        course = Course.objects.create(
            title = 'Algebra',
            description='Learn the basics of Algebra',
            category = self.category,
            level = self.level,
            subject = self.subject,
            course_level = 'beginner',
            duration =40,
            fee = 5000,
            start_date=date.today(),
            created_by=self.user
        )
        course.mode.add(self.learning_mode)
        
        self.assertEqual(str(course),'Algebra')
        self.assertEqual(course.level.name,'grade 10')
        self.assertEqual(course.category.name,'math')
        self.assertEqual(course.subject.subject_name,'Python')
        self.assertTrue(course.is_active)
        self.assertFalse(course.is_featured)
        
        
# __________ViewTesting__________
from django.urls import reverse

class CourseListView(TestCase):
    
    def setUp(self):
        self.user= User.objects.create_user(username='testuser', password='testpassword')
    
        self.learning_mode = LearningModeOption.objects.create(mode='online')
       
        self.category = Category.objects.create(name='math', description='ABC')
       
        self.level = Level.objects.create(name='grade 10')
       
        self.subject = Subject.objects.create(level=self.level,subject_name='Python')
        
        # Course Create karte hain
        self.course = Course.objects.create(
            title='Algebra',
            description='Learn Algebra Basics',
            category=self.category,
            level=self.level,
            subject=self.subject,
            course_level='beginner',
            duration=40,
            fee=5000,
            start_date=date.today(),
            created_by=self.user
        )
        self.course.mode.add(self.learning_mode)
        
    def test_course_list_view_status_code(self):
        
        res = self.client.get(reverse('courses:course_list'))
        self.assertEqual(res.status_code, 200)
        
    def test_course_list_view_template(self):
        res = self.client.get(reverse('courses:course_list'))
        self.assertTemplateUsed(res,'courses/course_list.html')
    
    def test_course_list_view_context(self):
        res = self.client.get(reverse('courses:course_list'))
        self.assertIn(self.course, res.context['courses'])
    
