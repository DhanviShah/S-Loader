from django.shortcuts import render
from django.http import HttpResponse
# import mysql.connector
from uploadFile.forms import NameForm


from django. shortcuts import render
# Create your views here.
# from uploadFile.models import NameFormModel

# def index(request) :
#         saved = False
#         form = NameForm()
#         if request. method == "POST":
#                 #Get the posted form
#                 MyNameForm = NameForm(request.POST, request. FILES)
                
#                 if MyNameForm.is_valid() :
#                         profile = NameFormModel()
#                         profile.name = MyNameForm.cleaned_data["name" ]
#                         # if form. is_valid() is True, form, cleaned_data is where all validated fields are stored.
#                         profile.picture = MyNameForm. cleaned_data["picture"]
#                         profile.save()

#                         saved = True
       
#         return render(request,"basic_form.html",{'form':form}) 
def index(request):  
        form = NameForm()  
        
        return render(request,"basic_form.html",{'form':form}) 
