import json
# from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.forms.models import model_to_dict

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route, action
from rest_framework.exceptions import APIException

from .serializers import (
    DpyDepartmentSerializer,
    DpyInstituteClassSerializer,
    DpyInstituteClassSessionSerializer,
    DpyInstituteClassSessionSubjectSerializer,
    DpyInstituteCSSUserSerializer,
    ViewClassSerializer,
    TimeTableSerializer,
    DpyInstituteUserClassSerializer,
    ClassPresentieSerializer,
    UserDayPresentieSerializer,
    ClassBatchSerializer,
    AddClassBatchSerializer)

from .models import (
    DpyDepartment,
    DpyInstituteClass,
    DpyInstituteClassSession,
    DpyInstituteClassSessionSubject,
    DpyInstituteClassSessionSubjectUser,
    DpyInstituteTimeTable,
    DpyInstituteUserClass,
    DpyInstituteClassUserPresenties,
    DpyUserDayPresenties,
    DpyClassBatch)

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
        queryset = DpyDepartment.objects.filter(institute_id=request.GET.get('id'))
        data = DpyDepartmentSerializer(queryset, many=True)
        return render(request, 'class_user_profiling/add-class.html', {'dept':data.data})
    return redirect('login_view')


@login_required(login_url='/')
def class_view(request, dep_id):
    if request.user.is_authenticated:
        return render(request, 'class_user_profiling/view-classes.html', {'dep_id': dep_id})
    return redirect('login_view')


@login_required(login_url='/')
def classinfo_view(request,dep_id,ic_id):
    if request.user.is_authenticated:
        queryset = DpyInstituteClass.objects.get(pk=ic_id)
        serializer = DpyInstituteClassSerializer(queryset)
        return render(request, 'class_user_profiling/view-class.html',
                      {'ic_id': ic_id, 'dep_id': dep_id, 'class_info': serializer.data})
    return redirect('login_view')


@login_required(login_url='/')
def department_view(request):
    if request.user.is_authenticated:
        return render(request, 'class_user_profiling/view-departments.html', {})
    return redirect('login_view')


class ManageDepartments(APIView):
    def get(self, request):
        queryset = DpyDepartment.objects.filter(institute_id=request.GET.get('id'))
        data = DpyDepartmentSerializer(queryset, many=True)
        return Response({"status": True, "message": "Data found Successfully", "data":data.data})

    def post(self, request):
        serializer = DpyDepartmentSerializer(data=request.data)
        if serializer.is_valid():
            exdata = {"created_by": self.request.user.id, "institute_id": request.GET.get('id')}
            serializer.save(**exdata)
            return Response({"status": True, "message": "Created Successfully."}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ManageClass(ModelViewSet):
    queryset = DpyInstituteClass.objects.all()
    serializer_class = AddClassBatchSerializer

    def get_queryset(self):
        instid = self.request.GET['id']
        queryset = super(ModelViewSet, self).get_queryset()
        return queryset.filter(institute=instid,status=1)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": True, "message": "Data found Successfully", "data": serializer.data})

    def perform_create(self, serializer):
            serializer.save(**{'created_by': self.request.user.id})

    def create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True, "message": "Created Successfully.", "data": serializer.data},status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
def class_details(request, dep_id):
    try:
        inst_class = DpyInstituteClass.objects.filter(department_id=dep_id)
    except inst_class.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ViewClassSerializer(inst_class,many=True)
        final_data = {}
        for value in serializer.data:
            # final_data.setdefault(value['standard'], []).append(value)
            final_data.setdefault(value['standard'], {})[value['division'] if value['division'] else value['standard']] = value
        return Response({"status": True, "message": "Data Found Successfully.","data":final_data})


class ManageClassSession(ModelViewSet):
    serializer_class = DpyInstituteClassSessionSerializer
    queryset = DpyInstituteClassSession.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": True, "message": "Session Data.", 'data': serializer.data})

    def perform_create(self, serializer):
            serializer.save(**{'created_by': self.request.user.id})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True, "message": "Created Successfully.", "data": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
            queryset = super(ModelViewSet, self).get_queryset()
            if self.request.GET.get('ic'):
                return queryset.filter(ic__in=self.request.GET['ic'], ic__institute=self.request.GET.get('id')
                                       , status=1)
            return queryset.filter(ic__institute=self.request.GET.get('id'),
                                   status=1)


class ManageClassSessionSubject(ModelViewSet):
    serializer_class = DpyInstituteClassSessionSubjectSerializer
    queryset = DpyInstituteClassSessionSubject.objects.all()

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        if self.request.GET.get('ic'):
            return queryset.filter(cs__ic__institute=self.request.GET.get('id'), cs__ic=self.request.GET['ic'], status=1)
        return queryset.filter(cs__ic__institute=self.request.GET.get('id'), status=1)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": True, "message": "Subjects Data.", 'data': serializer.data})

    def perform_create(self, serializer):
        serializer.save(**{'created_by': self.request.user.id})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True, "message": "Attendance Marked Successfully."}, status=status.HTTP_201_CREATED, headers=headers)


@login_required(login_url='/')
@api_view(['GET'])
def cssuser_by_icid(request, ic_id, user_type):
    if request.user.is_authenticated:
        from django.core import serializers
        final_data, user_map, sub_map = {}, {}, {}

        q1 = DpyInstituteClassSession.objects.filter(ic_id=ic_id, status=1)
        data = json.loads(serializers.serialize('json', q1))
        cs_ids = list(map(lambda x: x["pk"], data))

        q2 = DpyInstituteClassSessionSubject.objects.filter(cs_id__in=cs_ids, status=1)
        data1 = json.loads(serializers.serialize('json', q2, fields=['name', 'cs', 'prerequisite_subject']))
        css_ids = list(map(lambda x: x["pk"], data1))

        q3 = DpyInstituteClassSessionSubjectUser.objects.filter(css_id__in=css_ids, status=1, user_type=user_type)
        data2 = json.loads(serializers.serialize('json', q3, fields=['user', 'css', 'user_type']))
        user_ids = list(map(lambda x: x["fields"]["user"], data2))

        q4 = DpyUsers.objects.filter(pk__in=user_ids, status=1)
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

        return Response({"status": True, "message": "Data found Successfully.", 'data': final_data})
    return redirect('login_view')


"""
Adding session's subject-user(user-subject) combination for a class.
This function add user to a class and then adds the subject-user combination for that class.
*note this function was only made for adding teacher-subject combination during time-table creation
"""
class ManageClassSessionSubjectUser(APIView):
    def post(self, request):
        try:
            """
            Checking if user already exist in the class irrespective of status(active/inactive)
            then make the user active(status=1) for the class
            """
            classuser = DpyInstituteUserClass.objects.get(user=request.data.get('user'), ic=request.data.get('ic'), user_type=request.data.get('user_type'))
            serializer1 = DpyInstituteUserClassSerializer(classuser,data=request.data,partial=True)
            if serializer1.is_valid(): serializer1.save(**{'status':1, 'updated_by': request.user.id})
            else: return Response({"status": False, "message": serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DpyInstituteUserClass.DoesNotExist:
            # if user does not exist add them in class
            serializer1 = DpyInstituteUserClassSerializer(data=request.data)
            if serializer1.is_valid(): serializer1.save(**{'created_by': request.user.id})
            else: return Response({"status": False, "message": serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            """
            Checking if users-subject combination already exist in a class.
            If not then making the user active(status=1) for the class
            """
            cssuser = DpyInstituteClassSessionSubjectUser.objects.get(user=request.data.get('user'), css=request.data.get('css'),user_type=request.data.get('user_type'),status=0)
            serializer2 = DpyInstituteCSSUserSerializer(cssuser, data=request.data, partial=True)
            if serializer2.is_valid():
                serializer2.save(**{'status':1,'updated_by':request.user.id})
                return Response({"status": True, "message": "Created Successfully.","data": {'classuser': serializer1.data, 'cssuser': serializer2.data}},status=status.HTTP_201_CREATED)
            return Response({"status": False, "message": serializer2.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DpyInstituteClassSessionSubjectUser.DoesNotExist:
            """
            Adding user-subject combination in a class if the combination does not exist
            """
            serializer2 = DpyInstituteCSSUserSerializer(data=request.data)
            if serializer2.is_valid():
                serializer2.save(**{'created_by': request.user.id})
                return Response({"status": True, "message": "Created Successfully.", "data":
                    {'classuser': serializer1.data, 'cssuser': serializer2.data}}, status=status.HTTP_201_CREATED)
            return Response({"status": False, "message": serializer2.errors}, status=status.HTTP_400_BAD_REQUEST)

    """
    TODO: Function only disabling user-css combination by doing status=0.
    Need to be able to do more.
    """
    def patch(self, request):
        # from django.core import serializers
        cssuser = DpyInstituteClassSessionSubjectUser.objects.get(user=request.data.get('user'), css=request.data.get('css'), user_type=request.data.get('user_type'))
        serializer = DpyInstituteCSSUserSerializer(cssuser, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(**{'status': 0, 'updated_by': request.user.id})
            return Response({"status": True, "message": "Updated Successfully.", "data": serializer.data})
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ManageTimeTable(APIView):
    def post(self, request):
        serializer = TimeTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(**{'created_by': request.user.id, 'institute_id': request.GET.get('id')})
            return Response({"status": True, "message": "Created Successfully.",
                             "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
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
            serializer.save(**{'updated_by': request.user.id})
            return Response({"status": True, "message": "Updated Successfully.",
                             "data": serializer.data}, status=status.HTTP_201_CREATED)
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
        if self.request.GET.get('ic', None):
            try:
                q1 = DpyInstituteUserClass.objects.filter(ic=self.request.GET['ic'])
                q1_serializer = DpyInstituteUserClassSerializer(q1,many=True)

                for value in q1_serializer.data:
                    final_data.setdefault(value['user'], {}).update(value)
                    final_data[value['user']]['attendance'] = {}

                for value in serializer.data:
                    if value['user'] in final_data:
                        final_data[value['user']['attendance']][value['date']] = value
                    # final_data.setdefault(value['user'], {}).update(value)
                return Response({"status": True, "message": "Attendance Data.","data":final_data})
            except DpyInstituteUserClass.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({"status": False, "message": "Please provide ic!"}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        if self.request.GET.get('ic', None):
            queryset.filter(ic=self.request.GET['ic'], status=1)
        return queryset


class ManageUserDayPresentie(ModelViewSet):
    serializer_class = UserDayPresentieSerializer
    queryset = DpyUserDayPresenties.objects.all()

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        if self.request.GET.get('date'):
            return queryset.filter(date=self.request.GET['date'])
        return queryset.filter(institute=self.request.GET.get('id'), status=1)

    def perform_create(self, serializer):
        serializer.save(**{'created_by': self.request.user.id})

    def create(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        if request.data.get('absent'):
            if len(request.data.get('absent')):
                DpyUserDayPresenties.objects.filter(id__in=request.data.get('absent')).delete()

        serializer = self.get_serializer(data=request.data.get('present'), many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True, "message": "Attendance Marked Successfully."},
                        status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        final_data = {}
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        if self.request.GET.get('ic') and self.request.GET.get('type'):
            try:
                q1 = DpyInstituteUserClass.objects.filter(
                    ic=self.request.GET['ic'], user_type=self.request.GET['type'],
                    ic__institute=self.request.GET.get('id'))
                q1_serializer = DpyInstituteUserClassSerializer(q1, many=True)
                for value in q1_serializer.data:
                    final_data.setdefault(value['user'], {}).update(value)
                for value in serializer.data:
                    if value['user'] in final_data:
                        final_data.setdefault(value['user'], {}).setdefault('attendance', {})\
                            .update({value['date']: value})

                return Response({"status": True, "message": "Attendance Data.", "data": final_data})
            except DpyInstituteUserClass.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({"status": True, "message": "Day Attendance Data.", "data": serializer.data})


"""
Function to get User in a Class (from class-user table)
@param {string} ic_id (Class Id)
@param {string} user_type (1:student, 2:teacher)
"""
class ManageClassUser(ModelViewSet):
    serializer_class = DpyInstituteUserClassSerializer
    queryset = DpyInstituteUserClass.objects.all()

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        filters = {'ic__institute': self.request.GET['inst_id'], 'status':1}
        if 'ic' in self.request.GET: filters['ic']=self.request.GET['ic']
        if 'type' in self.request.GET: filters['user_type']=self.request.GET['type']
        if 'pk' in self.request.GET: filters['pk']=self.request.GET['pk']
        return queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        if 'inst_id' not in self.request.GET:
            return Response({"status": False, "message": "Please provide Institute ID!"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": True, "message": "Class User Data.", "data": serializer.data})

    @list_route(methods=['patch'])
    def update_user_batch(self, request):
        try:
            if 'ic' not in request.data or not request.data.get('ic'):
                raise APIException('Please provide Class ID.')
            if 'batch' not in request.data or not request.data.get('batch'):
                raise APIException('Please provide Batch ID.')
            if 'user_id' not in request.data  or not request.data.get('user_id'):
                raise APIException('Please provide User ID.')

            DpyClassBatch.objects.get(pk=request.data.get('batch'))
            qs = DpyInstituteUserClass.objects.filter(ic=request.data.get('ic'),user__in=request.data.get('user_id'))
            qs.update(batch=request.data.get('batch'))
            serializer = self.get_serializer(qs, many=True)
            return Response({"status": True, "message": "Updated Successfully.",'data':serializer.data})
        except DpyClassBatch.DoesNotExist:
            return Response({'status':False,'message':'Batch not found'},status=status.HTTP_404_NOT_FOUND)


"""
Function to get/add (User)-(Session-Subject) combination in a Class
@param {int} ic (Class Id) --for GET
@param {int} inst_id (Institute Id) --for GET
@param {int} type (User Type) --for GET
@param {objects} [{}] --for CREATE
"""
class BulkClassSessionSubjectUser(ModelViewSet):
    serializer_class = DpyInstituteCSSUserSerializer
    queryset = DpyInstituteClassSessionSubjectUser.objects.all()

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        filters = {'css__cs__ic__institute': self.request.GET['inst_id'], 'status': 1}
        if 'ic' in self.request.GET: filters['css__cs__ic'] = self.request.GET['ic']
        if 'type' in self.request.GET: filters['user_type'] = self.request.GET['type']
        if 'css' in self.request.GET: filters['css'] = self.request.GET['css']
        if 'pk' in self.request.GET: filters['pk'] = self.request.GET['pk']
        return queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        if 'inst_id' not in self.request.GET:
            return Response({"status": False, "message": "Please provide Institute ID!"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        final_data = {}

        if self.request.GET.get('ic') and self.request.GET.get('type') and self.request.GET.get('css'):
            q = DpyInstituteUserClass.objects.filter(ic=self.request.GET['ic'], user_type=self.request.GET['type'], status=1)
            serial = DpyInstituteUserClassSerializer(q, many=True)
            user_map = {}

            for value in serializer.data:
                del value['first_name']
                del value['middle_name']
                del value['last_name']
                user_map.setdefault(value['user'], {}).update(value)

            for value in serial.data:
                final_data.setdefault(value['user'], {}).update(value)
                if value['user'] in user_map:
                    final_data[value['user']].update(user_map[value['user']])
        else:
            final_data = serializer.data

        return Response({"status": True, "message": "Class User's Subject Data.", "data": final_data})

    def perform_create(self, serializer):
        serializer.save(**{'created_by': self.request.user.id})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True, "message": "Added Successfully."}, status=status.HTTP_201_CREATED, headers=headers)


class ManageClassBatch(ModelViewSet):
    serializer_class = ClassBatchSerializer
    queryset = DpyClassBatch.objects.all()

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        filters = {'ic__institute': self.request.GET['inst_id'], 'status': 1}
        if 'ic' in self.request.GET: filters['ic'] = self.request.GET['ic']
        if 'pk' in self.request.GET: filters['pk'] = self.request.GET['pk']
        return queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        if 'inst_id' not in request.GET:
            return Response({"status": False, "message": "Please provide Institute ID!"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": True, "message": "Class Batch Data.", "data": serializer.data})

    def perform_create(self, serializer):
        serializer.save(**{'created_by': self.request.user.id})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True, "message": "Added Successfully."}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save(**{'updated_by':self.request.user.id})
