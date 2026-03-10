from django.shortcuts import render ,redirect
from django.contrib.auth import logout
from .models import Admin_data
from report.models import IssueReport
# Create your views here.

def admin_login(request):
    if request.method == "POST":
        admin_name = request.POST.get("admin_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            admin = Admin_data.objects.get(
                admin_name=admin_name,
                email=email,
                password=password
            )

            request.session['admin_id'] = admin.admin_id
            return redirect('admin_dashboard')

        except Admin_data.DoesNotExist:
            return render(request,'admin_pages/admin_login.html',{
                "error":"Invalid login details"
            })

    return render(request,'admin_pages/admin_login.html')


def admin_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('login')

    total_reports = IssueReport.objects.count()

    pending_issues = IssueReport.objects.filter(admin_status='submitted').count()

    in_progress = IssueReport.objects.filter(admin_status='working').count()

    resolved_cases = IssueReport.objects.filter(admin_status='resolved').count()

    recent_reports = IssueReport.objects.all().order_by('-submitted_at')[:5]
    danger=IssueReport.objects.filter(status__in=['Critical', 'Major'])
    resolved_percent = 0
    progress_percent = 0
    pending_percent = 0

    if total_reports > 0:
        resolved_percent = round((resolved_cases / total_reports) * 100)
        progress_percent = round((in_progress / total_reports) * 100)
        pending_percent = round((pending_issues / total_reports) * 100)


    context = {
            'total_reports': total_reports,
            'pending_issues': pending_issues,
            'in_progress': in_progress,
            'resolved_cases': resolved_cases,
            'recent_reports': recent_reports,
            'danger':danger,
            'resolved_percent': resolved_percent,
        'progress_percent': progress_percent,
        'pending_percent': pending_percent,
        }
    return render(request,'admin_pages/admin_dashboard.html',context)

def list_complaints(request):
    recent_reports = IssueReport.objects.all().order_by('-submitted_at',)
    return render(request,'admin_pages/list_complaints.html',{'recent_reports': recent_reports})

def urgent_reports(request):

    urgent_reports = IssueReport.objects.filter(status='Critical').order_by('-submitted_at')

    return render(request, "admin_pages/urgentlist.html", {
        "recent_reports": urgent_reports
    })

def logout_view(request):
    logout(request)
    return redirect('home')

