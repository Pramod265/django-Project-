from django.shortcuts import render,redirect
from .import models
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db import connection, transaction
from onboarding.models import DpyInstituteUsers,DpyInstitute,DpyUsers
import json
from django import template
from django.core import serializers
from onboarding.serializers import InstituteUserSerializer,InstituteSerializer

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
    user = models.DpyEmployee.objects.all()
    data = serializers.serialize( "python", models.DpyEmployee.objects.all())
    return render(request ,'manage_hr/home.html',{'data':data,})

def salary(request):
    user = models.DpyEmployee.objects.all()
    data = serializers.serialize( "python", models.DpyEmployee.objects.all())
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    return render(request ,'manage_hr/generate_salary_slip.html',{'data':user,'range': range(1980,2021),'months':months})

def salary_structure(request):
    user = models.DpyEmployee.objects.all()
    data = serializers.serialize( "python", models.DpyEmployee.objects.all())
    return render(request ,'manage_hr/salary_structure.html',{'data':user,})

def update_user(request):
    data = request.POST.getlist('studentData[]')
    models.DpyTable.objects.filter(id=data[0]).update(email=data[3],mobile_number=data[4],adhaar_number=data[5])
    response_data ={'Status':True, 'Message':'Successfully Updated.'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def insert_emp(request):
    inst_id = int(institute_id(request))
    print(inst_id)
    data = request.POST.getlist('studentData[]')
    u = models.DpyEmployee(institute_id=inst_id,first_name=data[0],middle_name=data[1],last_name=data[2],mobile_number=data[3],email=data[4],date_of_join=data[5],designation=data[6],department=data[7],gender=data[8],basic_salary=data[9],casual_leaves=20,paid_leaves=20,sick_leaves=20)
    u.save()
    data ={'Status':True, 'Message':'Successfully Added.'}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")

def leave(request):
    inst_id = institute_id(request)
    print(inst_id)
    user = models.DpyEmployee.objects.values('first_name','id')
    data = serializers.serialize( "python", models.DpyEmployee.objects.all())

    v = models.DpyEmployee.objects.all().filter(id=4).values('casual_leaves','paid_leaves','sick_leaves')
    print(v)
    cll =v[0]['casual_leaves']
    pll =v[0]['paid_leaves']
    sll =v[0]['sick_leaves']  
    return render(request ,'manage_hr/leave.html',{'data':user,'cll':cll,'pll':pll,'sll':sll})

def numleave(request):
    data = request.POST.getlist('studentData[]')
    if data[0]=="":
        emp_id=int('3')
    else:
        emp_id=data[0]
    user = models.DpyEmployee.objects.values('first_name','id')
    data = serializers.serialize( "python", models.DpyEmployee.objects.all())
    v = models.DpyEmployee.objects.all().filter(id=emp_id).values('casual_leaves','paid_leaves','sick_leaves')
    cll =v[0]['casual_leaves']
    pll =v[0]['paid_leaves']
    sll =v[0]['sick_leaves']
    data ={'Status':True,'Message':'Successfull','cll':cll,'pll':pll,'sll':sll}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")  

def structure(request):
    data = request.POST.getlist('studentData[]')
    u = models.DpyEmployeeSalaryStructure.objects.all().filter(emp_id=data[0],month=data[1],year=data[2]).values('hra','ta','da','med','bonus','spal','others','tds','pt','pf');
    v = models.DpyEmployee.objects.all().filter(id=data[0]).values('first_name','last_name','basic_salary');
    name = v[0]['first_name']+" "+v[0]['last_name']
    bs =v[0]['basic_salary']
    hra =u[0]['hra']
    ta =u[0]['ta']
    da =u[0]['da']
    med =u[0]['med']
    bonus =u[0]['bonus']
    spal =u[0]['spal']
    others = u[0]['others']
    tds = u[0]['tds']
    pt = u[0]['pt']
    pf = u[0]['pf']
    data ={'Status':True,'Message':'Successfull','name':name,'bs':bs,'hra':hra,'ta':ta,'da':da,'med':med,'bonus':bonus,'spal':spal,'others':others,'tds':tds,'pt':pt,'pf':pf}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")  

def add_sal_struc(request):
    inst_id = int(institute_id(request))
    print(inst_id)
    data = request.POST.getlist('studentData[]')
    v = models.DpyEmployee.objects.all().filter(id=data[0]).values('first_name','last_name','basic_salary',);
    bs =v[0]['basic_salary']
    u = models.DpyEmployeeSalaryStructure(emp_id=data[0],institute_id=inst_id,month=data[12],year=data[13],basic=bs,hra=data[2],ta=data[3],da=data[4],med=data[5],bonus=data[6],spal=data[7],others=data[8],tds=data[9],pt=data[10],pf=data[11])
    u.save()
    data ={'Status':True,'Message':'Successfull'}
    return HttpResponse(json.dumps(data), content_type="application/json")

def addleave(request):
    data = request.POST.getlist('studentData[]')
    u = models.Leave(emp_id=data[0],emp_name=data[1],leave_type=data[2],start_date=data[3],end_date=data[4],reason=data[5])
    u.save()
    v = models.DpyEmployee.objects.all().filter(id=data[0]).values('casual_leaves','paid_leaves','sick_leaves')
    lt=data[2]
    days=int(data[6])
    cll =v[0]['casual_leaves']
    pll =v[0]['paid_leaves']
    sll =v[0]['sick_leaves']
    if lt=='Casual leaves':
        print(cll)
        ncl=int(int(cll)-days)
        print(ncl)
        models.DpyEmployee.objects.filter(id=data[0]).update(casual_leaves=ncl)
    if lt=='Paid leaves':
        npl=int(int(pll)-days)
        print(npl)
        models.DpyEmployee.objects.filter(id=data[0]).update(paid_leaves=npl)
    if lt=='Sick leaves':
        print(sll)
        nsl=int(int(sll)-days)
        # print(nsl)
        models.DpyEmployee.objects.filter(id=data[0]).update(sick_leaves=nsl)
    data ={'Status':True, 'Message':'Successfully Added.'}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")