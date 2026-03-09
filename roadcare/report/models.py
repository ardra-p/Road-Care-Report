from django.db import models

class IssueReport(models.Model):

    # Severity / Depth
    SEVERITY_CHOICES = [
        ('Minor', 'Minor'),
        ('Moderate', 'Moderate'),
        ('Major', 'Major'),
        ('Critical', 'Critical'),
    ]

    # Admin Work Status
    ADMIN_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('working', 'Working'),
        ('resolved', 'Resolved'),
    ]

    issue_id = models.AutoField(primary_key=True)

    user_name = models.CharField(max_length=150,null=True, blank=True)
    user_email = models.EmailField(null=True, blank=True)
    user_phone = models.CharField(max_length=15,null=True, blank=True)

    issue_description = models.TextField()
    issue_type = models.CharField(max_length=100)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255)

    image_path = models.ImageField(upload_to='issue_images/')

    # Issue severity
    status = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='Minor'
    )

    # Admin workflow status
    admin_status = models.CharField(
        max_length=20,
        choices=ADMIN_STATUS_CHOICES,
        default='submitted'
    )

    # Admin remarks
    remarks = models.TextField(null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.issue_type 