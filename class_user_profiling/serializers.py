from rest_framework import serializers
from .models import (
    DpyDepartment,
    DpyInstituteClass,
    DpyInstituteClassSession,
    DpyInstituteClassSessionSubject,
    DpyInstituteClassSessionSubjectUser,
    DpyInstituteTimeTable,
    DpyInstituteUserClass,
    DpyInstituteClassUserPresenties,)
from onboarding.serializers import UserSerializer
from django.forms.models import model_to_dict


class DpyInstituteUserClassSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    middle_name = serializers.CharField(source='user.middle_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = DpyInstituteUserClass
        fields = ('id','status','roll_no','user','user_type','ic','is_class_teacher','first_name','middle_name','last_name')


class DpyInstituteCSSUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpyInstituteClassSessionSubjectUser
        fields = ('id','status','css','user','user_type')


class DpyInstituteClassSessionSubjectSerializer(serializers.ModelSerializer):
    # user = DpyInstituteCSSUserSerializer(many=True, read_only=True)
    class Meta:
        model = DpyInstituteClassSessionSubject
        fields = ('id','name','cs','prerequisite_subject')


class DpyInstituteClassSessionSerializer(serializers.ModelSerializer):
    subject = DpyInstituteClassSessionSubjectSerializer(many=True, read_only=True)
    # def create(self, validated_data):
    #     ics = DpyInstituteClassSession.objects.create(**validated_data)
    #     # ics.ic_id = validated_data['ic_id']
    #     # ics.save()
    #     return model_to_dict(ics)
    # class_details = DpyInstituteClassSerializer()
    class Meta:
        model = DpyInstituteClassSession
        fields = ('id','start_month','end_month','ic','prerequisite_session','subject')


class DpyInstituteClassSerializer(serializers.ModelSerializer):
    class_session = DpyInstituteClassSessionSerializer(many=True, read_only=True)
    class Meta:
        model = DpyInstituteClass
        fields = ('id','standard','division','batch','sort_index','department_id','institute_id','class_session')


class DpyDepartmentSerializer(serializers.ModelSerializer):
    departments = DpyInstituteClassSerializer(many=True, read_only=True)
    class Meta:
        model = DpyDepartment
        fields = ('id','name','institute_id','departments')


class ViewClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpyInstituteClass
        fields = ('id','standard','division','batch','sort_index','department_id','institute_id')


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpyInstituteTimeTable
        fields = ('id','institute_id','css','user','start_time','end_time','lecture_no','day_id','status')


class ClassPresentieSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='css.name', read_only=True)

    class Meta:
        model = DpyInstituteClassUserPresenties
        fields = ('id', 'ic', 'css', 'marked_by', 'date', 'user','subject_name')
