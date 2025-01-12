from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib import messages
from app.models import StudentProfile, Task, Subject, University, FieldOfStudy, Message
from app.forms import CustomUserCreationForm, TaskForm, SubjectForm, UserWithProfileForm
import xml.etree.ElementTree as et

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['tasks'] = Task.objects.filter(user=self.request.user, type='TASK').order_by('due_date')[:3]
            context['tests'] = Task.objects.filter(user=self.request.user, type='TEST').order_by('due_date')[:3]
            context['exams'] = Task.objects.filter(user=self.request.user, type='EXAM').order_by('due_date')[:3]
            
            try:
                student_profile = StudentProfile.objects.get(user=self.request.user)
            except StudentProfile.DoesNotExist:
                student_profile = None
        
            context['user_data'] = {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
            'school': student_profile.school if student_profile else 'Unknown',
            'field_of_study': student_profile.field_of_study if student_profile else 'Unknown',
            }
        else:
            context['tasks'] = []
            context['tests'] = []
            context['exams'] = []
            context['user_data'] = {}

        return context

class RegisterView(UserPassesTestMixin, FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def test_func(self):
        return not self.request.user.is_authenticated
    
    def form_valid(self, form):
        user = form.save() 
        birthdate = form.cleaned_data.get('birthdate')
        school = form.cleaned_data.get('school')
        field_study = form.cleaned_data.get('field_of_study')

        university = University.objects.filter(name__iexact=school).first()
        if not university:
            university = University.objects.create(name=school)

        field_of_study = FieldOfStudy.objects.filter(name__iexact=field_study, university=university).first()
        if not field_of_study:
            field_of_study = FieldOfStudy.objects.create(name=field_study, university=university)

        StudentProfile.objects.create(
            user=user,
            birthdate=birthdate,
            school=university,
            field_of_study=field_of_study
        )
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs) 
    
class CustomLoginView(LoginView):
    template_name = 'login/login.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    
class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = 'profile.html'
    form_class = UserWithProfileForm
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        profile = StudentProfile.objects.get(user=self.request.user)
        kwargs.update({
            'instance': self.request.user,
            'profile_instance': profile,
        })
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        form.save(user_instance=user)
        return super().form_valid(form)
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'login/logged_out.html'
    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            return redirect(reverse_lazy('home'))
        
        return super().dispatch(request, *args, **kwargs)
    
class TasksListView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks.html'
    type = 'TASK'
    name_context_field = 'tasks'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.name_context_field] = Task.objects.filter(type = self.type, user = self.request.user)
        return context

class TestListView(TasksListView):
    template_name = 'tests.html'
    type = 'TEST'
    name_context_field = 'tests'
    
class ExamListView(TasksListView):
    template_name = 'exams.html'
    type = 'EXAM'
    name_context_field = 'exams'

class SubjectListView(LoginRequiredMixin, TemplateView):
    template_name = 'subjects.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        return context

@login_required
def add_or_edit_task(request, task_id=None):
    next_url = request.GET.get('next')
    
    if task_id:
        task = get_object_or_404(Task, id=task_id, user=request.user)
    else:
        task = Task(user=request.user, type='TASK')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.type='TASK'
            task.save()

            if next_url:
                return redirect(next_url)
            else:
                return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'taskform.html', {'form': form, 'task' : task})

@login_required
def add_or_edit_test(request, test_id=None):
    next_url = request.GET.get('next')
    
    if test_id:
        test = get_object_or_404(Task, id=test_id, user=request.user)
    else:
        test = Task(user=request.user, type='TEST')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=test)
        if form.is_valid():
            test = form.save(commit=False)
            test.user = request.user
            test.type='TEST'
            test.save()

            if next_url:
                return redirect(next_url)
            else:
                return redirect('tests')
    else:
        form = TaskForm(instance=test)
    
    return render(request, 'taskform.html', {'form': form, 'task' : test})

@login_required
def add_or_edit_exam(request, exam_id=None):
    next_url = request.GET.get('next')
    
    if exam_id:
        exam = get_object_or_404(Task, id=exam_id, user=request.user)
    else:
        exam = Task(user=request.user, type='EXAM')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=exam)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.type = 'EXAM'
            task.save()

            if next_url:
                return redirect(next_url)
            else:
                return redirect('exams')
    else:
        form = TaskForm(instance=exam)
    
    return render(request, 'taskform.html', {'form': form, 'task' : exam})

@login_required
def delete_task(request,task_id):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        exam = get_object_or_404(Task, id=task_id, user=request.user)
        exam.delete()
    return redirect(next_url)

@login_required
def mark_done(request, task_id):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.is_done = True
        task.save()
    return redirect(next_url)

@login_required
def add_subject(request):
    next_url = request.GET.get('next')
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            if next_url:
                return redirect(next_url)
            else:
                return redirect('subjects')
    else:
        form = SubjectForm()
    
    return render(request, 'subjectsform.html', {'form': form})

@login_required
def get_messages(request):
    try:
            student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
            student_profile = None
    
    if student_profile:
        messages = Message.objects.filter(university=student_profile.school)
        data = [
            {
                'user': message.user.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%H:%M:%S'),
            }
            for message in messages
        ]
        return JsonResponse({'messages': data}, safe=False)
    else:
        return JsonResponse({'messages': []}, safe=False)

@login_required
def post_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            student_profile = None
        
        if content and student_profile and request.user.is_authenticated:
            Message.objects.create(user=request.user, university=student_profile.school, content=content, timestamp=now())
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def import_tasks(request):
    next_url = request.GET.get('next')
    if request.method == 'POST' and request.FILES.get('xml_file'):
        xml_file = request.FILES['xml_file']

        try:
            tree = et.parse(xml_file)
            root = tree.getroot()

            for task_element in root.findall('Task'):

                subject_name = task_element.find('Subject').text
                subject, created = Subject.objects.get_or_create(name=subject_name)

                Task.objects.create(
                    type=task_element.find('Type').text.upper(),
                    title=task_element.find('Title').text,
                    description=task_element.find('Description').text,
                    created_at=task_element.find('CreatedAt').text,
                    due_date=task_element.find('DueDate').text if task_element.find('DueDate').text else None,
                    is_done=(task_element.find('IsDone').text == 'Yes'),
                    user=request.user,
                    subject = subject
                )

            messages.success(request, 'Tasks imported successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred during import: {str(e)}")

        return redirect(next_url)

    return redirect(next_url)

@login_required
def export_tasks_xml(request):
    task_ids = request.GET.get('task_ids')
    if not task_ids:
        return HttpResponse("No tasks selected.", status=400)

    task_ids = task_ids.split(',')
    tasks = Task.objects.filter(id__in=task_ids)

    root = et.Element('Tasks')
    for task in tasks:
        task_element = et.SubElement(root, 'Task')
        et.SubElement(task_element, 'ID').text = str(task.id)
        et.SubElement(task_element, 'Type').text = task.get_type_display()
        et.SubElement(task_element, 'Title').text = task.title
        et.SubElement(task_element, 'Description').text = task.description
        et.SubElement(task_element, 'CreatedAt').text = str(task.created_at)
        et.SubElement(task_element, 'DueDate').text = str(task.due_date) if task.due_date else ''
        et.SubElement(task_element, 'IsDone').text = 'Yes' if task.is_done else 'No'
        et.SubElement(task_element, 'Subject').text = task.subject.name

    xml_data = et.tostring(root, encoding='utf-8')

    response = HttpResponse(xml_data, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="tasks.xml"'

    return response
