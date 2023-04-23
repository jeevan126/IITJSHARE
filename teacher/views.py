from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from teacher.models import course, session, teacher
from student.models import project, file, Message
from django.core import serializers
from customuser.models import user_type
from django.conf import settings
import os
from django.core.mail import EmailMessage
from django.core.mail import send_mail


# Create your views here.

def thome(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teach:
        if (request.method == 'POST'):
            if request.POST.get('end_session') is not None:
                ssn = request.POST.get('session')
                ob = session.objects.get(session_id=ssn)
                ob.running = False
                ob.save()
                print(session.objects.get(session_id=ssn).running)
                # session.objects.get().running = False
            else:
                course_code = course.objects.get(course_code=request.POST.get('course-code-list'))
                batch = request.POST.get('batch')
                session_id = course_code.course_code + batch
                date = request.POST.get('start-date')
                t_code = teacher.objects.get(email=request.user)
                print(t_code.teacher_code)
                if course_code and batch and session_id and date and t_code:
                    sn = session(course_code=course_code, batch=batch, session_id=session_id, date=date,
                                 teacher_code=t_code)
                    sn.save()

        teacher_id = teacher.objects.get(email=request.user)
        print(teacher_id.teacher_code)
        sessions_obj = session.objects.filter(teacher_code=teacher_id.teacher_code)
        data = []

        for x in sessions_obj:
            tit = course.objects.get(course_code=x.course_code.course_code).course_title
            data.append({'session': x, 'title': tit})
        print(data)

        type = "teach"
        return render(request, 'teacher/teach-home.html', {'data': data, 'type':type})
    elif request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
        return redirect('shome')
    else:
        return redirect('home')


def createsession(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teach:
        if (request.method == 'POST'):
            course_code = request.POST.get('course-code')
            course_title = request.POST.get('course-title')
            credit = request.POST.get('credit-input')
            t_code = teacher.objects.get(email=request.user)
            if course_code and course_title and credit:
                c = course(course_code=course_code, course_title=course_title, course_credit=credit,
                           teacher_code=t_code)
                c.save()

        course_obj = course.objects

        type = "teach"
        return render(request, 'teacher/create-session.html', {'courses': course_obj, 'type':type})
    else:
        if request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
            return redirect('shome')


def batchinfo(request, session_id):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_teach:
        session_obj = get_object_or_404(session, pk=session_id)
        print(session_obj.session_id)
        project_objs = project.objects.raw("select * from student_project where session_id LIKE %s",
                                           [session_obj.session_id])

        type = "teach"
        return render(request, 'teacher/teacher_projects.html', {'projects': project_objs, 'session': session_obj, 'type':type})
    else:
        if request.user.is_authenticated and user_type.objects.get(user=request.user).is_student:
            return redirect('shome')


def projectdetails(request, session_id, project_id):
    # print(project_title, session)
    if request.user.is_authenticated :
        if request.method == 'POST':
            print("this is  request")

            if request.POST.get('delete') is not None:
                print("this is delete request")
                path = request.POST.get('delete')
                print("1:")
                print(path)
                full_path = os.path.join(settings.MEDIA_ROOT, path)
                full_path = full_path.replace("/", "\\")
                print(full_path)
                try:
                    print("2:")
                    os.remove(full_path)
                except FileNotFoundError:
                    print("3:")
                    return redirect(request.path_info)

                fileob = file.objects.get(file_content=request.POST.get('delete'))
                print("4:")
                fileob.delete()


            else:
                print("this is okay0")
                for uploaded_file in request.FILES.getlist('file'):
                    # uploaded_file = request.FILES['file']
                    # fs = FileSystemStorage()
                    # fs.save(uploaded_file.name, uploaded_file)
                    size = uploaded_file.size

                    ext = ""
                    if size < 512000:
                        size = size / 1024.0
                        ext = 'Kb'
                    elif size < 4194304000:
                        size = size / 1048576.0
                        ext = 'Mb'
                    else:
                        size = size / 1073741824.0
                        ext = 'Gb'
                    value = '%.2f' % size
                    value = value + ext
                    # print(value)
                    project_ob = project.objects.get(project_id=request.POST.get("project_id"))
                    file_obj = file(file_name=uploaded_file.name, project_id=project_ob, file_content=uploaded_file,
                                    file_size=value)
                    file_obj.save()
                    project_obj = get_object_or_404(project, pk=project_id)
                    s1 = project_obj.member1_reg  
                    s2 = project_obj.member2_reg  
                    s3 = project_obj.member3_reg 
                    lst = [s1.email, s2.email, s3.email] 
                    teacher_obj = teacher.objects.get(email=request.user)
                    email = EmailMessage(
                                    'New file shared with you',
                                    f"{teacher_obj.name}({teacher_obj.email}) send you a file in {project_ob.project_title} project ",
                                    'jschouhan2325@gmail.com',
                                    to = lst,
                                    )
                    email.send()
                    print("this is okay")
        project_obj = get_object_or_404(project, pk=project_id)
        session_obj = get_object_or_404(session, pk=session_id)
        project_messages = project_obj.message_set.all().order_by('-created')
        Project = project.objects.get(pk=project_id)
        teacher_obj = teacher.objects.get(email=request.user)
        if request.method == 'POST' and request.POST.get('body') is not None:
            print("jii")
            print("The name of the user is this:::", teacher_obj.name)
            s1 = project_obj.member1_reg  
            s2 = project_obj.member2_reg  
            s3 = project_obj.member3_reg 
            lst = [s1.email, s2.email, s3.email] 
            email = EmailMessage(
                            'New message',
                            f"{teacher_obj.name}({teacher_obj.email}) send you a message in {project_obj.project_title} project ",
                            'jschouhan2325@gmail.com',
                            to = lst,
                            )
            email.send()
            message = Message.objects.create(
                user = request.user,
                project = project_obj,
                body = request.POST.get('body'),
                name = teacher_obj.name 
            )
            return redirect('projectdetails', session_id, project_id)
        
        files = file.objects
        project_obj = get_object_or_404(project, pk=project_id)

        type = ""
        if user_type.objects.get(user=request.user).is_teach:
            type = "teach"
        else:
            type = "student"
        print("hello this is the page", session_obj.session_id, project_obj.project_id)
        return render(request, 'uploads.html', {'project_obj': project_obj, 'session_obj': session_obj, 'files': files, 'type':type, 'project_messages':project_messages})
    else:
        return redirect('home')
