from django.shortcuts import render
from .models import Profile
from django.http import HttpResponse
from django.template import loader
import io
import pdfkit

def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        about = request.POST.get("about", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        experience = request.POST.get("experience", "")
        skills = request.POST.get("skills","")

        profile = Profile(name=name, email=email, phone=phone, about=about, degree=degree, school=school, university=university, experience=experience, skills=skills)
        profile.save()

    return render(request, 'cvgenerator/accept.html')

def cv(request,id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('cvgenerator/cv.html')
    html = template.render({'user_profile':user_profile})
    options={
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    cvgenerator = pdfkit.from_string(html,False, options)
    response = HttpResponse(cvgenerator, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = "cv.pdf"
    return response

def list(request):
    profiles =Profile.objects.all()
    return render(request,'cvgenerator/list.html',{'profiles':profiles})
