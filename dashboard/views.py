from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
# from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from onboarding.models import DpyInstitute

# Create your views here.


@login_required(login_url='/')
def home_view(request):
    if request.user.is_authenticated:
        colleges = DpyInstitute.objects.all()
        return render(request,'dashboard/home.html',{'institutes':colleges})
    return redirect('login_view')


@login_required(login_url='/')
def profile_view(request):
    if request.user.is_authenticated:
        return render(request,'dashboard/profile.html',{})
    return redirect('login_view')


class ManageProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        import json
        institute = InstituteSerializer(data=json.loads(request.data.get('institute')))
        if institute.is_valid():
            userSerial = UserSerializer(data=json.loads(request.data.get('user')))
            if userSerial.is_valid():
                instUser = InstituteUserSerializer(data=json.loads(request.data.get('instuser')))
                if instUser.is_valid():
                    user = userSerial.save()
                    # if request.FILES.get('image') is not None : user.image = request.FILES.get('image')
                    # user.created_by = user.id
                    # user.save()

                    instData = {"created_by":user.pk}
                    # if request.FILES.get('logo') is not None : instData['logo'] = request.FILES.get('logo')
                    # if request.FILES.get('school_image') is not None : instData['school_image'] = request.FILES.get('school_image')
                    inst = institute.save(**instData)
                    
                    instUserdata = {"created_by":user.pk, "user_id":user.pk, "institute_id":inst.id}
                    instUser.save(**instUserdata)

                    return Response({"status": True, "message": "Created Successfully."}, status=status.HTTP_201_CREATED)
                return Response({"status": False, "message": instUser.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": False, "message": userSerial.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False, "message": institute.errors}, status=status.HTTP_400_BAD_REQUEST)

# bulk upload view
import logging
import csv, io, html, string
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import Students_reg_form
@login_required(login_url='/')
def bulk_upload(request):
    data = {}
    if request.method == "GET":
        return render(request, "dashboard/bulk_upload.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("dashboard:bulk_upload"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("dashboard:bulk_upload"))
        file_data = csv_file.read().decode('utf7')
        lines = file_data.split("\n")
        counter = 0
        #loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
        # for data in datas:
            counter +=1
            if counter == 1:
                continue
            fields = line.split(",")
            data_dict = {}
            # for i in range(len(fields)-1):
            #     fields[i].replace('+AEA-','@').replace('+AC0-','-').replace('+IBg-','\'').replace('+IBw-','\"').replace('+AF8-','_')
            # now here we will have to replace back the special character
            data_dict["first_name"] = fields[0]
            data_dict["middle_name"] = fields[1]
            data_dict["last_name"] = fields[2]
            data_dict["mother_name"] = fields[3]
            data_dict["date_of_addmission"] = fields[4]
            data_dict["roll_no"] = int(float(fields[5]))
            data_dict["gr_no"] = int(float(fields[6]))
            data_dict["dob"] = fields[7]
            data_dict["blood_group"] = fields[8]
            data_dict["caste"] = fields[9]
            data_dict["nationality"] = fields[10]
            data_dict["religion"] = fields[11]
            data_dict["communication_address"] = fields[12]
            data_dict["permanent_address"] = fields[13]
            data_dict["adhar_no"] = fields[14]
            data_dict["house"] = fields[15]
            data_dict["mother_tongue"] = fields[16]
            data_dict["special_quata"] = fields[17]
            data_dict["gender"] = fields[18]
            data_dict["student_type"] = fields[19]
            data_dict["mobile"] = fields[20]
            try:
                form = Students_reg_form(data_dict)
                if form.is_valid():
                    form.save()                    
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())                                                
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))                    
                pass
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
 
    return HttpResponseRedirect(reverse("dashboard:bulk_upload"))
    #return render(request,'bulk_upload.html',{'form':[]})


import os
from django.conf import settings
from django.http import HttpResponse,Http404
from onboarding.models import DpyInstitute

def download(request, path="Students.csv"):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


from django.views.decorators.csrf import csrf_exempt

def find_college(request):

    pincode = request.POST.getlist('pincode[]')
    colleges = DpyInstitute.objects.all(pin_code = pincode)
    response_data ={'Status':True, 'Message':pincode}
    return HttpResponseRedirect(request,'dashboard:home')
    # onboard_forms = models.DpyInstitute.objects.all().order_by('id')
    #return render(request,'list_data.html',{'onboard_forms':onboard_forms})
    # username = request.session['username']
    # return rende;r(request,"list_data.html",{'username':username,'onboard_forms':onboard_forms})
    return render(request,'dashboard/home.html',{'colleges':colleges})
    return redirect('login_view')
