from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
# from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from onboarding.models import DpyInstitute, DpyInstituteUsers, DpyUsers
from onboarding.serializers import InstituteUserSerializer

# Create your views here.


def calculate_profile(request):
    profile_count = 0
    total_col = 35
    studentsArr = []
    teachersArr = []
    profileArr = [] 
    instituteArr = []
    # print(request.session['user_info'])
    queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
    serializer = InstituteUserSerializer(queryset)
    InstUserid = (serializer.data["id"])
    InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
    InstUserarr = ['role','designation','date_of_joining','is_active','status','institute_id','user_id']
    User = DpyUsers.objects.get(id=InstUser.user_id)
    Userarr = ['username','first_name','last_name','is_staff','is_active','date_joined','email','middle_name','mobile','dob','image','status' ]
    Institute = DpyInstitute.objects.get(id=InstUser.institute_id)
    
    if InstUser.role == None or InstUser.role == "":
        profile_count += 1

    if InstUser.designation == None or InstUser.designation == "":
        profile_count += 1

    if InstUser.date_of_joining == None or InstUser.date_of_joining == "":
        profile_count += 1

    if InstUser.status == None or InstUser.status == "":
        profile_count += 1

    if User.username == None or User.username == "":
        profile_count += 1

    if User.first_name == None or User.first_name == "":
        profile_count += 1

    if User.last_name == None or User.last_name == "":
        profile_count += 1

    if User.is_staff == None or User.is_staff == "":
        profile_count += 1

    
    if User.email == None or User.email == "":
        profile_count += 1

    if User.middle_name == None or User.middle_name == "":
        profile_count += 1

    if User.mobile == None or User.mobile == "":
        profile_count += 1

    if User.dob == None or User.dob == "":
        profile_count += 1

    if User.image == None or User.image == "":
        profile_count += 1

    if Institute.name == None or Institute.name == "":
        profile_count += 1


    if Institute.institute_email == None or Institute.institute_email == "":
        profile_count += 1


    if Institute.contact == None or Institute.contact == "":
        profile_count += 1


    if Institute.board == None or Institute.board == "":
        profile_count += 1


    if Institute.nature == None or Institute.nature == "":
        profile_count += 1

    if Institute.logo == None or Institute.logo == "":
        profile_count += 1

    if Institute.school_image == None or Institute.school_image == "":
        profile_count += 1

    if Institute.medium == None or Institute.medium == "":
        profile_count += 1

    if Institute.university == None or Institute.university == "":
        profile_count += 1

    if Institute.address == None or Institute.address == "":
        profile_count += 1

    if Institute.city == None or Institute.city == "":
        profile_count += 1

    if Institute.pin_code == None or Institute.pin_code == "":
        profile_count += 1

    if Institute.state == None or Institute.state == "":
        profile_count += 1

    if Institute.country == None or Institute.country == "":
        profile_count += 1

    students = DpyStudents.objects.all().filter(institute_id = InstUser.institute_id)
    print(len(students))
    incomplete_students = [] #will take this array's length for total incomolete students detail in one institute
    # counter = 0
    for student in students:
        print(student.first_name)
        if student.first_name == "" or student.middle_name == "" or student.last_name == "" or student.mother_name == "" or student.date_of_addmission == "" or student.roll_no == "" or student.gr_no == "" or student.email == "" or student.dob == "" or student.blood_group == "" or student.caste == "" or student.nationality == "" or student.communication_address == "" or student.permanent_address == "" or student.adhar_no == "" or student.house == "" or student.gender == "" or student.mobile == "" or student.student_class == "" or student.section == "":
            incomplete_students.append(student.id)
        
    percentage = ((27+1)-(profile_count+len(incomplete_students)))/27 * 100

    print(User.first_name)
    return int(percentage), incomplete_students

@login_required(login_url='/')
def home_view(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search_query = request.GET.get('search_box', None)
            if request.GET.get('search_box'):
                # search_query = request.GET.get('search_box', None)
                search_colleges = DpyInstitute.objects.all().filter(pin_code=search_query)
                count,incomplete_students = calculate_profile(request)
                # print(incomplete_students)
                return render(request,'dashboard/home.html',{'search_colleges':search_colleges,'count':count, 'incomplete_students':incomplete_students})
        colleges = DpyInstitute.objects.all()
        count,incomplete_students = calculate_profile(request)
        # print(incomplete_students)
        return render(request,'dashboard/home.html',{'institutes':colleges,'count':count, 'incomplete_students':incomplete_students})
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
# from .resources import StudentsResource, UsersResource
from tablib import Dataset
import json


@login_required(login_url='/')

def bulk_upload(request):
    queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
    serializer = InstituteUserSerializer(queryset)
    InstUserid = (serializer.data["id"])
    InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
    instituteId = InstUser.institute_id
    # if request.method == 'POST':
    #     student_resource =StudentsResource()
    #     # user_resource = UsersResource()
    #     dataset =Dataset()
    #     new_students = request.FILES['csv_file']
    #     imported_data = dataset.load(new_students.read().decode("utf7"))
    #     result = student_resource.import_data(dataset, dry_run=True)  # Test the data import
    #     # result1 = user_resource.import_data(dataset, dry_run=True)  # Test the data import
    #     print(dataset)
    #     if not result.has_errors():
    #         student_resource.import_data(dataset, dry_run=False)  # Actually import now
    #         # user_resource.import_data(dataset, dry_run=False)  # Actually import now
    # return render(request, 'dashboard/bulk_upload.html',{})

    data = {}
    if request.method == 'GET':
        return render(request, "dashboard/bulk_upload.html", data)
    ############################
    # if not GET, then proceed##
    ############################
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("dashboard:bulk_upload"))
        ###############################
        #if file is too large, return##
        ###############################
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("dashboard:bulk_upload"))
        file_data = csv_file.read().decode('utf7')
        lines = file_data.split("\n")
        counter = 0
        listdata = []
        #######################################################################################
        #loop over the lines and save them in db. If error , store as string and then display##
        #######################################################################################
        for line in lines:
            counter +=1
            if counter == 1:
                continue
            fields = line.split(",")
            data_dict = {}            
            arr = ["first_name","middle_name","last_name","mother_name","date_of_addmission","roll_no","gr_no","email","dob","blood_group","caste","nationality","religion","communication_address","permanent_address","adhar_no","house","mother_tongue","special_quata","gender","student_type","mobile","student_class","section"]
            for i in range(0,len(arr),1):
                data_dict[arr[i]] = fields[i]
            try:
                data_dict["institute_id"]=instituteId
                print(instituteId)
                form = Students_reg_form(data_dict)
                if form.is_valid():
                    form.save()                    
                else:
                    # uploadFailed[0] = data_dict
                    logging.getLogger("error_logger").error(form.errors.as_json())                                                
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))                    
                pass
        #     listdata.append(data_dict.copy())
        #     # upload_func(listdata)
        # Students = DpyStudents.objects.bulk_create(listdata,counter)
        # Students.save()
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    # print(uploadFailed)
    return HttpResponseRedirect(reverse("dashboard:bulk_upload"))
    #return render(request,'bulk_upload.html',{'form':[]})



from . models import DpyStudents
# def upload_func(multiDict):
#     Students = DpyStudents.objects.bulk_create(multiDict)
#     Students.save()




from django.conf import settings
from django.http import HttpResponse,Http404
from onboarding.models import DpyInstitute
import os
##############################
#Csv File Download function ##
##############################

def download(request, path="Students.csv"):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


####################################################################################
# action='.' <-- This tells django to do the GET action in the same URL as you are##
####################################################################################
from django.views.decorators.csrf import csrf_exempt


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def register_students(request):
    if request.method == 'POST':
        studentData = request.POST.getlist('studentData[]')
        student = DpyStudents()
        student.first_name  = studentData[0]
        student.middle_name  = studentData[1]
        student.last_name  = studentData[2]
        student.mother_name  = studentData[3]
        # student.dob  = studentData[4]+"/"+studentData[5]+"/"+studentData[6]
        student.dob = studentData[4]
        student.blood_group  = studentData[5]
        student.caste  = studentData[6]
        student.mobile  = studentData[7]
        student.nationality  = studentData[8]
        student.religion  = studentData[9]
        student.mother_tongue  = studentData[10]
        student.adhar_no  = studentData[11]
        student.gender  = studentData[12]
        student.communication_address  = studentData[13]
        student.permanent_address  = studentData[14]
        student.house  = studentData[15]
        student.roll_no  = studentData[16]
        student.gr_no  = studentData[17]
        student.date_of_addmission  = studentData[18]
        student.special_quata  = studentData[19]
        student.student_type  = studentData[20]
        student.student_class  = studentData[21]
        student.section  = studentData[22]
        student.save()
        response_data ={'Status':True, 'Message':'done'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")   
    return render(request,'dashboard/register_student.html',{'form':[]});



def view_students(request):
    if request.method == 'GET':
        queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
        serializer = InstituteUserSerializer(queryset)
        InstUserid = (serializer.data["id"])
        InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
        InstUserarr = ['role','designation','date_of_joining','is_active','status','institute_id','user_id']
        students = DpyStudents.objects.all().filter(institute_id = InstUser.institute_id)
        return render(request,"dashboard/view_student.html",{'students':students})



def student_profile(request, id=None):
    student = DpyStudents.objects.get(id=id)
    return render(request,'dashboard/student_profile.html',{'form':student})
    return HttpResponse("sfadf"+id)

from .serializers import StudentsSerializer
import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update_student_profile(request, id=None):
    if request.method == 'POST':
        formData = request.POST.getlist('formData[]')
        #for personal details
        if (formData[11]) == '1':
            for i in range(0,len(formData)):
                if formData[i]=="none" or formData[i]==" " :
                    formData[i]=""
            
            DpyStudents.objects.filter(id=id).update(first_name=formData[0],
            middle_name=formData[1],
            last_name=formData[2],
            email=formData[3],
            mobile=formData[4],
            dob=formData[5],
            religion=formData[6],
            caste=formData[7],
            adhar_no=formData[8],
            gender=formData[9],
            blood_group=formData[10]
            )   
            #return Response({"status": True, "message": "Updated Successfully."}, status=status.HTTP_201_UPDATED)
            response_data ={'Status':True, 'Message': formData[0] }
            return HttpResponse(json.dumps(response_data), content_type="application/json")

            #for update of institute details
        if formData[11] == '2':
            for i in range(0,len(formData)):
                if formData[i]=="none" or formData[i]==" " :
                    formData[i]=""
            
            DpyStudents.objects.filter(id=id).update(
            date_of_addmission=formData[0],
            mother_name=formData[1],
            roll_no=formData[2],
            gr_no=formData[3],
            communication_address=formData[4],
            permanent_address=formData[5],
            house=formData[6],
            special_quata=formData[7],
            student_type=formData[8],
            student_class=formData[9],
            section=formData[10]
            )   
            #return Response({"status": True, "message": "Updated Successfully."}, status=status.HTTP_201_UPDATED)
            response_data ={'Status':True, 'Message': formData[0] }
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    student = DpyStudents.objects.get(id=id)
    return render(request,'dashboard/student_profile.html',{'form':student})


@login_required(login_url='/')
def profile_edit(request):
    if request.user.is_authenticated:
        return render(request,'dashboard/profile_edit.html',{})
    return redirect('login_view')

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        formData = request.POST.getlist('formData[]')
        for i in range(0,len(formData)):
            if formData[i]=="none" or formData[i]==" " :
                formData[i]=""
        
        DpyUsers.objects.filter(id=formData[0]).update(
        email=formData[1],
        mobile=formData[2],
        )
        DpyInstituteUsers.objects.filter(user_id=formData[0]).update(
        role=formData[3],
        )
        DpyInstitute.objects.filter(id=formData[4]).update(
        name=formData[5],
        contact=formData[6],
        address=formData[7],
        ) 
        #return Response({"status": True, "message": "Updated Successfully."}, status=status.HTTP_201_UPDATED)
        response_data ={'Status':True, 'Message': formData[0] }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request,'dashboard/profile.html',{})
    return HttpResponse("carzola")

def incomplete_student(request):
    return HttpResponse('incomplete students')