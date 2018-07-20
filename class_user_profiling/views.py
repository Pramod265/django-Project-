import json
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.forms.models import model_to_dict

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    DpyDepartmentSerializer,
    DpyInstituteClassSerializer,
    DpyInstituteClassSessionSerializer,
    DpyInstituteClassSessionSubjectSerializer,
    DpyInstituteCSSUserSerializer,
    ViewClassSerializer,
    TimeTableSerializer,
    DpyInstituteUserClassSerializer,
    ClassPresentieSerializer,)
from .models import (
    DpyDepartment,
    DpyInstituteClass,
    DpyInstituteClassSession,
    DpyInstituteClassSessionSubject,
    DpyInstituteClassSessionSubjectUser,
    DpyInstituteTimeTable,
    DpyInstituteUserClass,
    DpyInstituteClassUserPresenties,)
from onboarding.models import DpyInstituteUsers, DpyUsers


# Create your views here.
@login_required(login_url='/')
def timetable_view(request):
    if request.user.is_authenticated:
        return render(request, 'class_user_profiling/time-table.html',{})
    return redirect('login_view')


@login_required(login_url='/')
def addclass_view(request):
    if request.user.is_authenticated:
        queryset = DpyDepartment.objects.all()
        data = DpyDepartmentSerializer(queryset, many=True)
        return render(request, 'class_user_profiling/add-class.html', {'dept':data.data})
    return redirect('login_view')


@login_required(login_url='/')
def class_view(request, dep_id):
    if request.user.is_authenticated:
        return render(request, 'class_user_profiling/view-classes.html',{'dep_id': dep_id})
    return redirect('login_view')


@login_required(login_url='/')
def classinfo_view(request,dep_id,ic_id):
    if request.user.is_authenticated:
        queryset = DpyInstituteClass.objects.get(pk=ic_id)
        serializer = DpyInstituteClassSerializer(queryset)
        return render(request, 'class_user_profiling/view-class.html',{'ic_id':ic_id,'dep_id':dep_id,'class_info':serializer.data})
    return redirect('login_view')


@login_required(login_url='/')
def department_view(request):
    if request.user.is_authenticated:
        return render(request,'class_user_profiling/view-departments.html',{})
    return redirect('login_view')


class ManageDepartments(APIView):
    def get(self, request):
        queryset = DpyDepartment.objects.filter(institute_id=request.session['institute_id'])
        data = DpyDepartmentSerializer(queryset, many=True)
        return Response({"status": True, "message": "Data found Successfully","data":data.data})

    def post(self, request):
        serializer = DpyDepartmentSerializer(data=request.data)
        if serializer.is_valid():
            exdata = {"created_by": self.request.user.id, "institute_id": request.session['institute_id']}
            serializer.save(**exdata)
            return Response({"status": True, "message": "Created Successfully."}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ManageClass(APIView):
    def get(self, request):
        queryset = DpyInstituteClass.objects.all().filter(institute_id=request.session['institute_id'])
        data = DpyInstituteClassSerializer(queryset, many=True)
        return Response({"status": True, "message": "Data found Successfully","data":data.data})
    # def post(self, request, format='json'):
        # import json
        # err = resp = [];
        # for i in request.data:
        #     # i["created_by"] = request.user.id
        #     # if 'institute_id' in request.session:
        #     #     i["institute_id"] = request.session['institute_id']
        #     # else:
        #     #     instuser = DpyInstituteUsers.objects.get(user_id=request.user.id)
        #     #     i["institute_id"] = instuser.institute_id
        # #     aaa = DpyInstituteClass.objects.create(**i)
        # #     resp.append(model_to_dict(aaa))
        # # return Response({"status": True, "message": "Created Successfully.","data":resp}, status=status.HTTP_201_CREATED)
        #     serializer = DpyInstituteClassSerializer(data=i)
        #     if serializer.is_valid():
        #         serializer.save(**{'institute_id':instuser.institute_id,'department_id':i.get('department_id')})
        #         resp.append(serializer.data)
        #     else:
        #         err.append(serializer.errors)

        # if len(err) == len(resp) :
        #     return Response({"status": True, "message": "Created Successfully.","data":resp}, status=status.HTTP_201_CREATED)
        # else:
        #     return Response({"status": False, "message": err}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = DpyInstituteClassSerializer(data=json.loads(request.data.get('data')),many=True)
        if serializer.is_valid():
            exdata = {"created_by":self.request.user.id,'institute_id':request.session['institute_id'],'department_id':request.data.get('department_id')}
            serializer.save(**exdata)
            return Response({"status": True, "message": "Created Successfully.","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def class_details(request, dep_id):
    try:
        inst_class = DpyInstituteClass.objects.filter(department_id=dep_id)
    except inst_class.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ViewClassSerializer(inst_class,many=True)
        findata = []
        final_data = {}
        for value in serializer.data:
            # final_data.setdefault(value['standard'], []).append(value)
            final_data.setdefault(value['standard'], {})[value['division'] if value['division'] else value['standard']] = value

        return Response({"status": True, "message": "Data Found Successfully.","data":final_data})


# class ManageClassSession(APIView):
    # def post(self, request, format=None):
    #     serializer = DpyInstituteClassSessionSerializer(data=json.loads(request.data.get('data')),many=True)
    #     if serializer.is_valid():
    #         # data = serializer.create(json.loads(request.data.get('data')))
    #         serializer.save(**{'created_by':request.user.id})
    #         return Response({"status": True, "message": "Created Successfully.","data":serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ManageClassSession(ModelViewSet):
    serializer_class = DpyInstituteClassSessionSerializer
    queryset = DpyInstituteClassSession.objects.all()

    def perform_create(self, serializer):
            serializer.save(**{'created_by':self.request.user.id})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
            class_ids = DpyInstituteClass.objects.filter(institute_id=self.request.session['institute_id'], status=1)
            ic_ids = class_ids.values_list('id', flat=True)
            queryset = super(ModelViewSet, self).get_queryset()

            if self.request.GET.get('ic', None):
                return queryset.filter(ic__in=self.request.GET['ic'].split('/'), status=1)
            return queryset.filter(ic__in=ic_ids,status=1)


class ManageClassSessionSubject(APIView):
    def post(self, request, format=None):
        serializer = DpyInstituteClassSessionSubjectSerializer(data=json.loads(request.data.get('data')),many=True)
        if serializer.is_valid():
            # data = serializer.create(json.loads(request.data.get('data')))
            serializer.save(**{'created_by':request.user.id})
            return Response({"status": True, "message": "Created Successfully.","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/')
@api_view(['GET'])
def subject_by_class(request, ic_id):
    if request.user.is_authenticated:
        from django.core import serializers

        queryset = DpyInstituteClassSession.objects.filter(ic_id=ic_id,status=1)
        data = json.loads(serializers.serialize('json', queryset))
        cs_ids = list(map(lambda x: x["pk"], data))
        queryset2 = DpyInstituteClassSessionSubject.objects.filter(cs_id__in=cs_ids)
        data1 = json.loads(serializers.serialize('json', queryset2, fields = ['name','cs','prerequisite_subject']))

        final_data = []
        for value in data1:
            value['fields']['css_id'] = value['pk']
            value['fields']['cs_id'] = value['fields']['cs']
            del value['fields']['cs']
            final_data.append(value["fields"])

        return Response({"status": True, "message": "Data found Successfully.",'data':final_data})
    return redirect('login_view')


@login_required(login_url='/')
@api_view(['GET'])
def user_by_icid(request, ic_id, user_type):
    if request.user.is_authenticated:
        from django.core import serializers
        final_data, user_map, sub_map = {}, {}, {}

        q1 = DpyInstituteClassSession.objects.filter(ic_id=ic_id, status=1)
        data = json.loads(serializers.serialize('json', q1))
        cs_ids = list(map(lambda x: x["pk"], data))

        q2 = DpyInstituteClassSessionSubject.objects.filter(cs_id__in=cs_ids, status=1)
        data1 = json.loads(serializers.serialize('json', q2, fields = ['name', 'cs', 'prerequisite_subject']))
        css_ids = list(map(lambda x: x["pk"], data1))

        q3 = DpyInstituteClassSessionSubjectUser.objects.filter(css_id__in=css_ids, status=1, user_type=user_type)
        data2 = json.loads(serializers.serialize('json', q3, fields=['user', 'css', 'user_type']))
        user_ids = list(map(lambda x: x["fields"]["user"], data2))

        q4 = DpyUsers.objects.filter(pk__in=user_ids,status=1)
        data3 = json.loads(serializers.serialize('json', q4, fields=['first_name', 'middle_name', 'last_name']))

        for value in data3:
            user_map.setdefault(value['pk'], {}).update(value["fields"])

        for value in data1:
            sub_map.setdefault(value['pk'], {}).update(value["fields"])

        for value in data2:
            value['fields']['cssu_id'] = value['pk']
            value['fields']['css_id'] = value['fields']['css']
            value['fields']['user_id'] = value['fields']['user']
            del value['fields']['css'],value['fields']['user']
            final_data.setdefault(value['fields']['cssu_id'], {}).update(value["fields"])
            final_data[value['fields']['cssu_id']].update(user_map[value["fields"]["user_id"]])
            final_data[value['fields']['cssu_id']].update(sub_map[value["fields"]["css_id"]])

        return Response({"status": True, "message": "Data found Successfully.",'data':final_data})
    return redirect('login_view')


class ManageClassSessionSubjectUser(APIView):
    def post(self, request, format=None):
        try:
            classuser = DpyInstituteUserClass.objects.get(user=request.data.get('user'),ic=request.data.get('ic'),user_type=request.data.get('user_type'))
            serializer1 = DpyInstituteUserClassSerializer(classuser,data=request.data,partial=True)
            if serializer1.is_valid(): serializer1.save(**{'status':1,'updated_by':request.user.id})
            else: return Response({"status": False, "message": serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DpyInstituteUserClass.DoesNotExist:
            serializer1 = DpyInstituteUserClassSerializer(data=request.data)
            if serializer1.is_valid(): serializer1.save(**{'created_by':request.user.id})
            else: return Response({"status": False, "message": serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cssuser = DpyInstituteClassSessionSubjectUser.objects.get(user=request.data.get('user'),css=request.data.get('css'),user_type=request.data.get('user_type'),status=0)
            serializer2 = DpyInstituteCSSUserSerializer(cssuser,data=request.data,partial=True)
            if serializer2.is_valid():
                serializer2.save(**{'status':1,'updated_by':request.user.id})
                return Response({"status": True, "message": "Created Successfully.","data":{'classuser':serializer1.data,'cssuser':serializer2.data}}, status=status.HTTP_201_CREATED)
            return Response({"status": False, "message": serializer2.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DpyInstituteClassSessionSubjectUser.DoesNotExist:
            serializer2 = DpyInstituteCSSUserSerializer(data=request.data)
            if serializer2.is_valid():
                serializer2.save(**{'created_by':request.user.id})
                return Response({"status": True, "message": "Created Successfully.","data":{'classuser':serializer1.data,'cssuser':serializer2.data}}, status=status.HTTP_201_CREATED)
            return Response({"status": False, "message": serializer2.errors}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, format=None):
        # from django.core import serializers

        cssuser = DpyInstituteClassSessionSubjectUser.objects.get(user=request.data.get('user'),css=request.data.get('css'),user_type=request.data.get('user_type'))
        serializer = DpyInstituteCSSUserSerializer(cssuser,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(**{'status':0,'updated_by':request.user.id})
            return Response({"status": True, "message": "Updated Successfully.","data":serializer.data})
        return Response({"status": False, "message": serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)

        # q1 = DpyInstituteClassSession.objects.filter(ic_id=request.data.get('ic'),status=1)
        # data = json.loads(serializers.serialize('json', q1))
        # cs_ids = list(map(lambda x: x["pk"], data))
        # q2 = DpyInstituteClassSessionSubject.objects.filter(cs_id__in=cs_ids,status=1)
        # data1 = json.loads(serializers.serialize('json', q2, fields = ['name','cs','prerequisite_subject']))
        # css_ids = list(map(lambda x: x["pk"], data1))
        # q3 = DpyInstituteClassSessionSubjectUser.objects.filter(css_id__in=css_ids,status=1)
        # cssu_ids = json.loads(serializers.serialize('json', q3))
        # print("================================")
        # print(len(data))
        # if len(data) == 0:
        #     classuser = DpyInstituteUserClass.objects.get(ic=request.data.get('ic'),user=request.data.get('user'))
        #     serializer1 = DpyInstituteUserClassSerializer(classuser,data=request.data,partial=True)
        #     if serializer1.is_valid(): serializer1.save(**{'status':1,'updated_by':request.user.id})
        #     else: return Response({"status": False, "message": serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)


class ManageTimeTable(APIView):
    def post(self, request, format=None):
        data = json.loads(request.data.get('data'))
        serializer = TimeTableSerializer(data=data)
        if serializer.is_valid():
            # userclass = {'user_type':2,'roll_no':None,'ic':request.data.get('ic_id'),'user':data['user']}
            # serializer1 = DpyInstituteUserClassSerializer(data=userclass)
            # if serializer1.is_valid():
            #     userclass = {'user_type':2,'css':data['css'],'user':data['user']}
            #     serializer2 = DpyInstituteCSSUserSerializer(data=userclass)
            #     if serializer2.is_valid():
                    # serializer1.save(**{'created_by':request.user.id})
                    # serializer2.save(**{'created_by':request.user.id})
                    # serializer.save(**{'created_by':request.user.id,'institute_id':request.session['institute_id']})
            #         return Response({"status": True, "message": "Created Successfully.","data":serializer2.data}, status=status.HTTP_201_CREATED)
            #     return Response({"status": False, "message": serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"status": False, "message": serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(**{'created_by':request.user.id,'institute_id':request.session['institute_id']})
            return Response({"status": True, "message": "Created Successfully.","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','PATCH'])
def lecture_detail(request, pk):
    try:
        query = DpyInstituteTimeTable.objects.get(pk=pk,status=1)
    except DpyInstituteTimeTable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TimeTableSerializer(query)
        # response = {**serializer.data,'something':1}
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = TimeTableSerializer(query, data=json.loads(request.data.get('data')), partial=True)
        if serializer.is_valid():
            serializer.save(**{'updated_by':request.user.id})
            return Response({"status": True, "message": "Updated Successfully.","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ManageClassPresentie(ModelViewSet):
    serializer_class = ClassPresentieSerializer
    queryset = DpyInstituteClassUserPresenties.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(**{'created_by': self.request.user.id})
    #
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        final_data = {}
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        q1 = DpyInstituteUserClass.objects.filter(ic=self.request.GET['ic'])
        q1_serializer = DpyInstituteUserClassSerializer(q1,many=True)
        for value in q1_serializer.data:
            final_data.setdefault(value['user'], {}).update(value)
        for value in serializer.data:
            final_data.setdefault(value['user'], {}).update(value)
        return Response(final_data)

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        if self.request.GET.get('ic', None):
            queryset.filter(ic=self.request.GET['ic'], status=1)
            return queryset
