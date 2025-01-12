from django.test import TestCase
from .forms import CustomUserCreationForm, TaskForm
from .models import StudentProfile, University, FieldOfStudy, Task, Subject
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
# Create your tests here.

class CustomUserCreationFormTest(TestCase):

    def setUp(self):
        self.university = University.objects.create(name='Test University')
        self.field_of_study = FieldOfStudy.objects.create(name='Computer Science', university=self.university)

        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'birthdate': '2000-01-01',
            'school': self.university.name,
            'field_of_study': self.field_of_study.name,
        }

    def test_register_creates_user_and_profile(self):
        response = self.client.post(reverse('register'), data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='testuser')
        profile = StudentProfile.objects.get(user=user)
        self.assertEqual(profile.school.name, self.university.name)
        self.assertEqual(profile.field_of_study.name, self.field_of_study.name)
        self.assertEqual(profile.birthdate.strftime('%Y-%m-%d'), '2000-01-01')

    def test_form_missing_field(self):
        data = self.valid_data.copy()
        data.pop('email')
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_passwords_mismatch(self):
        data = self.valid_data.copy()
        data['password2'] = 'WrongPassword123'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_invalid_email(self):
        data = self.valid_data.copy()
        data['email'] = 'invalidemail'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_duplicate_username(self):
        User.objects.create_user(username='testuser', password='password123')
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')

    def test_login_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('home'))

    def test_login_invalid_username(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_invalid_password(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_blank_fields(self):
        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_login_redirect_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('home')) 

class AddOrEditTaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.subject = Subject.objects.create(name='Math')
        self.client.login(username='testuser', password='password123')

        self.task_data = {
            'subject': self.subject.id,
            'title': 'New Task',
            'description': 'This is a test task',
            'due_date': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'), 
        }

    def test_add_task(self):
        response = self.client.post(reverse('add_task'), data=self.task_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task', user=self.user).exists())

        task = Task.objects.get(title='New Task')
        self.assertEqual(task.description, 'This is a test task')
        self.assertEqual(task.due_date.strftime('%Y-%m-%d'), self.task_data['due_date'])
        self.assertEqual(task.type, 'TASK')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.subject, self.subject)

    def test_invalid_due_date(self):
        invalid_task_data = self.task_data.copy()
        invalid_task_data['due_date'] = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        response = self.client.post(reverse('add_task'), data=invalid_task_data)

        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'The date cannot be later than today.') 

        self.assertIn('form', response.context)
        form = response.context['form']

        self.assertIn('due_date', form.errors)
        self.assertEqual(form.errors['due_date'][0], 'The date cannot be later than today.')

        self.assertFalse(Task.objects.filter(title='New Task').exists())