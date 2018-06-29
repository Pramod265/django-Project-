from django.shortcuts import render,redirect
from .import models
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db import connection, transaction
from . import models
import json
from django import template
from django.core import serializers

# Create your views here.
def home(request):
    user = models.Employee.objects.all()
    data = serializers.serialize( "python", models.Employee.objects.all())

    return render(request ,'manage_hr/home.html',{'data':data,})

def update_user(request):
    data = request.POST.getlist('studentData[]')
    models.DpyTable.objects.filter(id=data[0]).update(email=data[3],mobile_number=data[4],adhaar_number=data[5])
    response_data ={'Status':True, 'Message':'Successfully Updated.'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def insert_emp(request):
    data = request.POST.getlist('studentData[]')
    u = models.Employee(first_name=data[0],middle_name=data[1],last_name=data[2],mobile_number=data[3],email=data[4],date_of_join=data[5],designation=data[6],department=data[7],gender=data[8],basic_salary=data[9],casual_leaves=20,paid_leaves=20,sick_leaves=20)
    u.save()
    data ={'Status':True, 'Message':'Successfully Added.'}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")

def leave(request):
    user = models.Employee.objects.values('first_name','emp_id')
    data = serializers.serialize( "python", models.Employee.objects.all())
    v = models.Employee.objects.all().filter(emp_id=3).values('casual_leaves','paid_leaves','sick_leaves')
    cll =v[0]['casual_leaves']
    pll =v[0]['paid_leaves']
    sll =v[0]['sick_leaves']
    return render(request ,'manage_hr/leave.html',{'data':user,'cll':cll,'pll':pll,'sll':sll},)

def numleave(request):
    data = request.POST.getlist('studentData[]')
    if data[0]=="":
        emp_id=int('3')
    else:
        emp_id=data[0]
    user = models.Employee.objects.values('first_name','emp_id')
    data = serializers.serialize( "python", models.Employee.objects.all())
    v = models.Employee.objects.all().filter(emp_id=emp_id).values('casual_leaves','paid_leaves','sick_leaves')
    cll =v[0]['casual_leaves']
    pll =v[0]['paid_leaves']
    sll =v[0]['sick_leaves']
    data ={'Status':True,'Message':'Successfull','cll':cll,'pll':pll,'sll':sll}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")   
def addleave(request):
    data = request.POST.getlist('studentData[]')
    u = models.Leave(emp_id=data[0],emp_name=data[1],leave_type=data[2],start_date=data[3],end_date=data[4],reason=data[5])
    u.save()
    v = models.Employee.objects.all().filter(emp_id=data[0]).values('casual_leaves','paid_leaves','sick_leaves')
    lt=data[2]
    days=int(data[6])
    cll =v[0]['casual_leaves']
    pll =v[0]['paid_leaves']
    sll =v[0]['sick_leaves']
    if lt=='Casual leaves':
        print(cll)
        ncl=int(int(cll)-days)
        print(ncl)
        models.Employee.objects.filter(emp_id=data[0]).update(casual_leaves=ncl)
    if lt=='Paid leaves':
        npl=int(int(pll)-days)
        print(npl)
        models.Employee.objects.filter(emp_id=data[0]).update(paid_leaves=npl)
    if lt=='Sick leaves':
        print(sll)
        nsl=int(int(sll)-days)
        # print(nsl)
        models.Employee.objects.filter(emp_id=data[0]).update(sick_leaves=nsl)
    data ={'Status':True, 'Message':'Successfully Added.'}
    return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type="application/json")
