from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
def timetable_view(request):
    if request.user.is_authenticated:
        return render(request,'class_user_profiling/time-table.html',{})
    return redirect('login_view')