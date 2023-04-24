from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.conf import settings
from customuser.models import user_type
from teacher.models import course, session
from student.models import project, file
from django.contrib import messages

def landing(request):
    return render(request,'base.html')

def landing(request):
    return render(request,'landing.html')

def home(request):
    if (request.method == 'POST'):
        print("ashche")
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print("now")
        if user is not None:
            login(request, user)
            print("HERE")
            try:
                type_obj = user_type.objects.get(user=user)
            except user_type.DoesNotExist:
                type_obj = 'teach'
                
            if user.is_authenticated and type_obj.is_student:
                return redirect('shome')
            elif user.is_authenticated and type_obj.is_teach:
                return redirect('thome')
        else:
            print("PAI NAI")
            return redirect('home')

    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('/')

def user_profile(request):
    type = ""
    if request.user.is_authenticated:
        if user_type.objects.get(user=request.user).is_teach:
            type = "teach"
        else:
            type = "student"
        user = request.user
        return render(request, 'user_profile.html', {'user':user, 'type':type})
    else:
        return ('home')

def projectdetails(request, session_id, project_id):
    # print(project_title, session)
    if request.user.is_authenticated:
        if request.method == 'POST':
            for uploaded_file in request.FILES.getlist('file'):
                # uploaded_file = request.FILES['file']
                # fs = FileSystemStorage()
                # fs.save(uploaded_file.name, uploaded_file)
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

        print("there", project_id)
        files = file.objects
        project_obj = get_object_or_404(project, pk=project_id)

        type = ""
        if user_type.objects.get(user=request.user).is_teach:
            type = "teach"
        else:
            type = "student"

        return render(request, 'upload.html', {'project_obj': project_obj, 'files': files, 'type':type})
    else:
        return redirect('home')

# def delete_file(self, *args, **kwargs):
#     print(self)
#     self.file_content.delete()
#     super.delete(*args, **kwargs)
