from django.shortcuts import render, redirect, get_object_or_404
from .models import IssueReport
import base64
from django.core.files.base import ContentFile
from django.contrib import messages


# Create your views here.

def homepage(request):
    return render(request,'home/home.html')

def report(request):
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        description = request.POST.get("description")
        issue_type = request.POST.get("issue_type")

        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        address = request.POST.get("address")

        status = request.POST.get("status")   # ← slider value added

        photo_data = request.POST.get("photo")
        if not issue_type:
            messages.error(request, "Please select an issue type before submitting.")
            return redirect('report')   # return to issue reporting page


        image_file = None

        # Convert base64 camera image to file
        if photo_data:
            format, imgstr = photo_data.split(';base64,')
            ext = format.split('/')[-1]
            image_file = ContentFile(base64.b64decode(imgstr), name='issue.' + ext)

        IssueReport.objects.create(
            user_name=name,
            user_email=email,
            user_phone=phone,
            issue_description=description,
            issue_type=issue_type,
            latitude=latitude,
            longitude=longitude,
            address=address,
            status=status,   # ← saving slider value
            image_path=image_file
        )
        messages.success(request, "Your road issue has been reported successfully.")
        return redirect('home')

    return render(request,'home/issuereport.html')

def manage(request,issue_id):
    issue = get_object_or_404(IssueReport, issue_id=issue_id)
    if request.method == "POST":

        # Update admin status
        admin_status = request.POST.get("admin_status")

        if admin_status:
            issue.admin_status = admin_status

        # Save remark / note
        remark = request.POST.get("remark")

        if remark:
            issue.remarks = remark

        issue.save()

        return redirect('manage', issue_id=issue.issue_id)

    return render(request,'home/manageissue.html', {
        "issue": issue
    })

def delete_issue(request, id):
    issue = get_object_or_404(IssueReport, issue_id=id)
    issue.delete()
    return redirect('admin_dashboard')

def map_view(request):
    reports = IssueReport.objects.all()
    return render(request,'home/issueinmap.html',{"reports": reports})