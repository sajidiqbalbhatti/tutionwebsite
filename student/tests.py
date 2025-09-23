from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import User
from courses.models import Course, Category, Level, Subject
from Tutor.models import TutorProfile
from .models import Student
from datetime import date, time
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

User = get_user_model()

class StudentModelTest(TestCase):
    def generate_image(self):
        image = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        image.save(img_bytes, format='JPEG')
        return SimpleUploadedFile(name='test_image.jpg', content=img_bytes.getvalue(), content_type='image/jpeg')

    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='student')

        self.category = Category.objects.create(name='Mathematics')
        self.level = Level.objects.create(name='Grade 10')
        self.subject = Subject.objects.create(subject_name='Algebra', level=self.level)

        self.course = Course.objects.create(
            title='Algebra Basics',
            description='Learn Algebra from scratch',
            category=self.category,
            level=self.level,
            subject=self.subject,
            course_level='beginner',
            duration=40,
            fee=5000,
            start_date=date.today(),
            created_by=self.user
        )

        # Dummy images for testing
        self.profile_image = self.generate_image()
        self.id_card_image = self.generate_image()

        # Create TutorProfile
        self.tutor = TutorProfile.objects.create(
            user=self.user,
            name='Test Tutor',
            bio='Expert in Algebra and Geometry',
            phone_number='03001234567',
            email='tutor@example.com',
            id_card_number='12345-6789012-3',
            id_card_picture=self.id_card_image,
            education='Masters in Mathematics',
            certifications='Certified Algebra Tutor',
            experience_years=5,
            hourly_rate=Decimal('500.00'),  # ✅ Decimal value dena zaroori hai
            languages_spoken='English, Urdu',
            profile_picture=self.profile_image,
            available_from=time(9, 0),
            available_until=time(17, 0),
            country='Pakistan',
            city='Karachi',
            is_featured=True
        )

        # self.tutor.subjects.add(self.subject)
        self.tutor.courses.add(self.course)
        self.subject = Subject.objects.create(level=self.level,subject_name='Python')
 # Unpack karo agar queryset hai


        # Create Student
        self.student = Student.objects.create(
            user=self.user,
            category='SCI',
            level='FSC',
            name='Test Student',
            phone='03123456789',
            date_of_birth=date(2000, 1, 1),
            address='Test Address',
            parent_name='Test Parent',
            parent_contact='03999999999',
            profile_picture=self.generate_image()  # ✅ yeh missing tha
        )

    def test_student_create(self):
        self.assertEqual(str(self.student), 'teststudent (No Courses)')
        self.assertEqual(self.course.category.name, 'Mathematics')
        self.assertEqual(self.student.parent_name,'Test Parent')   
