from django.shortcuts import render,redirect
from .import models
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db import connection, transaction
from onboarding.models import DpyInstituteUsers,DpyInstitute,DpyUsers
import json
from django import template
from django.core import serializers
from onboarding.serializers import InstituteUserSerializer,InstituteSerializer
# from .models import DpyLeaveTypes
# Create your views here.
def institute_id(request):
    queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
    serializer = InstituteUserSerializer(queryset)
    institute = serializer.data['institute']
    inst_id = institute['id']
    return inst_id

def home(request):
    inst_id = institute_id(request)
    print(inst_id)
    user = DpyUsers.objects.all()
    data = serializers.serialize( "python", DpyUsers.objects.all())
    return render(request ,'manage_hr/home.html',{'data':data,})

def salary(request):
    inst_id = institute_id(request)
    institute = DpyInstitute.objects.all().filter(id=inst_id)
    array = [3,4,5,6]
    inst_users = DpyInstituteUsers.objects.all().filter(role__in=array,type=0)
    userIds = []
    for inst_user in inst_users:
        userIds.append(inst_user.user_id)
    users = DpyUsers.objects.all().filter(id__in=userIds)
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    return render(request ,'manage_hr/generate_salary_slip.html',{'data':users,'range': range(1980,2021),'months':months, 'institute': institute})

def salary_structure(request):
    array = [3,4,5,6]
    inst_users = DpyInstituteUsers.objects.all().filter(role__in=array,type=0)
    userIds = []
    for inst_user in inst_users:
        userIds.append(inst_user.user_id)
    users = DpyUsers.objects.all().filter(id__in=userIds)
    return render(request ,'manage_hr/salary_structure.html',{'data':users,})

# def update_user(request):
#     data = request.POST.getlist('studentData[]')
#     models.DpyTable.objects.filter(id=data[0]).update(email=data[3],mobile_number=data[4],adhaar_number=data[5])
#     response_data ={'Status':True, 'Message':'Successfully Updated.'}
#     return HttpResponse(json.dumps(response_data), content_type="application/json")

def insert_emp(request):
    inst_id = int(institute_id(request))
    data = request.POST.getlist('studentData[]')
    # data.push(fname, mname, lname, mobno, email, fulldate, desig, depart, gender,role);
    u = DpyUsers(first_name=data[0],middle_name=data[1],username=data[0],last_name=data[2],mobile=data[3],email=data[4],gender=data[8])
    # department=data[7],basic_salary=0,
    u.save()
    empid=u.id
    v = DpyInstituteUsers(date_of_joining=data[5],role=data[9],designation=data[6],institute_id=inst_id,user_id=empid)
    v.save()
    data ={'Status':True, 'Message':'Successfully Added.','empid':empid,}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")

def insert_leave(request):
    inst_id = int(institute_id(request))
    data = request.POST.getlist('studentData[]')
    u = models.DpyLeaveTypes(emp_id=data[0],institute_id=inst_id,leave_name=data[1],leaves_remaining=data[2])
    u.save()
    data ={'Status':True, 'Message':'Successfully Added.'}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")

def leave(request):
    inst_id = institute_id(request)
    print(inst_id)
    array = [3,4,5,6]
    inst_users = DpyInstituteUsers.objects.all().filter(role__in=array,type=0)
    userIds = []
    for inst_user in inst_users:
        userIds.append(inst_user.user_id)
    users = DpyUsers.objects.all().filter(id__in=userIds)
    leaves = models.DpyLeaveTypes.objects.all().filter(emp_id__in=userIds)
    # data = serializers.serialize( "python", models.DpyEmployee.objects.all())
    # v = models.DpyEmployee.objects.all().filter(id=4).values('casual_leaves','paid_leaves','sick_leaves')
    # print(v)
    # cll =v[0]['casual_leaves']
    # pll =v[0]['paid_leaves']
    # sll =v[0]['sick_leaves']  
    # return render(request ,'manage_hr/leave.html',{'data':user,'cll':cll,'pll':pll,'sll':sll})
    return render(request ,'manage_hr/leave.html',{'data':users,'leaves':leaves})


# def leavename(request): 
#     data = request.POST.getlist('studentData[]')
#     if data[0]=="":
#         emp_id=int('3')
#     else:
#         emp_id=data[0]
#     v = models.DpyLeaveTypes.objects.all().filter(id=emp_id).values('casual_leaves','paid_leaves','sick_leaves')
#     cll =v[0]['casual_leaves']
#     pll =v[0]['paid_leaves']
#     sll =v[0]['sick_leaves']
#     data ={'Status':True,'Message':'Successfull','cll':cll,'pll':pll,'sll':sll}
#     return JsonResponse(data)
#     return HttpResponse(json.dumps(data), content_type="application/json")  

# def numleave(request): 
#     data = request.POST.getlist('studentData[]')
#     if data[0]=="":
#         emp_id=int('3')
#     else:
#         emp_id=data[0]
#     v = models.DpyLeaveTypes.objects.all().filter(emp_id=emp_id).values('leave_name','leaves_remaining')
#     data ={'Status':True,'Message':'Successfull'}
#     return JsonResponse(data)
#     return HttpResponse(json.dumps(data), content_type="application/json")  

def structure(request):
    data = request.POST.getlist('studentData[]')
    try:
        # trans = models.DpyEmployeeSalaryStructure.objects.all().filter(emp_id=data[0],month=data[1],year=data[2])
        # data = list(trans.values('hra','ta','da','med','bonus','spal','others','tds','pt','pf'))
        u = models.DpyEmployeeSalaryStructure.objects.all().filter(emp_id=data[0])
        users = DpyUsers.objects.get(id=data[0])
        desg = DpyInstituteUsers.objects.all().filter(user_id=data[0])
        for i in desg:
            desgn=i.designation
        name = users.first_name+" "+users.last_name
        datalist = list(u.values('hra','ta','da','med','basic','bonus','spal','others','tds','pt','pf'))
        data ={'Status':True,'data':datalist,'name':name,'desg':desgn}
    except IndexError:
      data ={'Status':False,'Message':'DETAILS UNAVILABLE.'}
    
    return HttpResponse(json.dumps(data))

def slipstructure(request):
    data = request.POST.getlist('studentData[]')
    try:
        u = models.DpyEmployeeSalaryStructure.objects.all().filter(emp_id=data[0],month=data[1],year=data[2])
        users = DpyUsers.objects.get(id=data[0])
        desg = DpyInstituteUsers.objects.all().filter(user_id=data[0])
        for i in desg:
            desgn=i.designation
        name = users.first_name+" "+users.last_name
        datalist = list(u.values('hra','ta','da','med','basic','bonus','spal','others','tds','pt','pf'))
        data ={'Status':True,'data':datalist,'name':name,'desg':desgn}
    except IndexError:
      data ={'Status':False,'Message':'DETAILS UNAVILABLE.'}
    
    return HttpResponse(json.dumps(data))

def add_sal_struc(request):
    inst_id = int(institute_id(request))
    print(inst_id)
    data = request.POST.getlist('studentData[]')
    dempid = data[0]
    # data.push(empid, bs, hra, ta, da, med, bonus, spal, others, tds, pt, pf,month,year);
    emps = models.DpyEmployeeSalaryStructure.objects.all().filter(emp_id=dempid)
    if len(emps) > 0:
        models.DpyEmployeeSalaryStructure.objects.all().filter(emp_id=data[0]).update(basic=data[1],institute_id=inst_id,hra=data[2],ta=data[3],da=data[4],med=data[5],bonus=data[6],spal=data[7],others=data[8],tds=data[9],pt=data[10],pf=data[11],month=data[12],year=data[13])
        data ={'Status':True,'Message':'Successfull'}
        return HttpResponse(json.dumps(data), content_type="application/json")

    u = models.DpyEmployeeSalaryStructure(emp_id=data[0],basic=data[1],institute_id=inst_id,hra=data[2],ta=data[3],da=data[4],med=data[5],bonus=data[6],spal=data[7],others=data[8],tds=data[9],pt=data[10],pf=data[11],month=data[12],year=data[13])
    u.save()
    data ={'Status':True,'Message':'Successfull'}
    return HttpResponse(json.dumps(data), content_type="application/json")

def addleave(request):
    inst_id = int(institute_id(request))
    data = request.POST.getlist('studentData[]')
    # data.push(empid, employee, leavetype, fullstartdate, fullenddate, reason, days, leaveid);
    u = models.Leave(emp_id=data[0],institute_id=inst_id,emp_name=data[1],leave_type=data[2],start_date=data[3],end_date=data[4],reason=data[5])
    u.save()
    days=int(data[6])#leaves taken
    leaves= models.DpyLeaveTypes.objects.get(id=data[7])
    actual_leaves = leaves.leaves_remaining - days
    models.DpyLeaveTypes.objects.all().filter(id=data[7]).update(leaves_remaining=actual_leaves)
    data ={'Status':True, 'Message':'Successfully Added.'}
    return JsonResponse(data)
    # return HttpResponse(json.dumps(data), content_type="application/json")