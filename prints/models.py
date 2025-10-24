from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PrintRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('printed', 'Printed'),
    ]
    
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='print_requests')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    copies = models.IntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    printed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['deadline', '-created_at']
        
    def __str__(self):
        return f"{self.filename} - {self.teacher.get_full_name() or self.teacher.username}"
    
    def is_urgent(self):
        """Check if request is due within 2 hours"""
        if self.status == 'printed':
            return False
        time_until_deadline = self.deadline - timezone.now()
        return time_until_deadline.total_seconds() <= 7200  # 2 hours in seconds
    
    def mark_printed(self):
        """Mark request as printed"""
        self.status = 'printed'
        self.printed_at = timezone.now()
        self.save()
