from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import PrintRequest
from .forms import PrintRequestForm
import os


def login_view(request):
    """Login view for teachers and secretary"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'prints/login.html')


def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """
    Dashboard view - shows different content for teachers vs secretary
    Secretary: is_staff=True
    Teachers: is_staff=False
    """
    if request.user.is_staff:
        return secretary_dashboard(request)
    else:
        return teacher_dashboard(request)


@login_required
def teacher_dashboard(request):
    """Teacher dashboard with upload form and request history"""
    if request.method == 'POST':
        form = PrintRequestForm(request.POST, request.FILES)
        if form.is_valid():
            print_request = form.save(commit=False)
            print_request.teacher = request.user
            print_request.filename = request.FILES['file'].name
            print_request.save()
            
            # Send notification to secretary via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'secretary',
                {
                    'type': 'new_request',
                    'request_id': print_request.id,
                    'teacher': request.user.get_full_name() or request.user.username,
                    'filename': print_request.filename,
                    'deadline': print_request.deadline.strftime('%Y-%m-%d %H:%M'),
                }
            )
            
            messages.success(request, f'Print request submitted successfully! File: {print_request.filename}')
            return redirect('dashboard')
    else:
        form = PrintRequestForm()
    
    # Get teacher's requests
    requests = PrintRequest.objects.filter(teacher=request.user)
    pending_count = requests.filter(status='pending').count()
    printed_count = requests.filter(status='printed').count()
    
    context = {
        'form': form,
        'requests': requests,
        'pending_count': pending_count,
        'printed_count': printed_count,
    }
    
    return render(request, 'prints/teacher_dashboard.html', context)


@login_required
def secretary_dashboard(request):
    """Secretary dashboard with pending requests queue"""
    if not request.user.is_staff:
        return redirect('dashboard')
    
    # Get all pending requests, ordered by deadline
    pending_requests = PrintRequest.objects.filter(status='pending').order_by('deadline')
    printed_requests = PrintRequest.objects.filter(status='printed').order_by('-printed_at')[:20]
    
    pending_count = pending_requests.count()
    printed_count = PrintRequest.objects.filter(status='printed').count()
    
    context = {
        'pending_requests': pending_requests,
        'printed_requests': printed_requests,
        'pending_count': pending_count,
        'printed_count': printed_count,
    }
    
    return render(request, 'prints/secretary_dashboard.html', context)


@login_required
def mark_printed(request, request_id):
    """Mark a print request as printed (secretary only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    print_request = get_object_or_404(PrintRequest, id=request_id)
    print_request.mark_printed()
    
    # Send notification to teacher via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'teacher_{print_request.teacher.id}',
        {
            'type': 'request_printed',
            'request_id': print_request.id,
            'filename': print_request.filename,
        }
    )
    
    messages.success(request, f'Marked "{print_request.filename}" as printed')
    return redirect('dashboard')


@login_required
def download_file(request, request_id):
    """Download a print request file"""
    print_request = get_object_or_404(PrintRequest, id=request_id)
    
    # Check permissions: teacher can only download their own, secretary can download all
    if not request.user.is_staff and print_request.teacher != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    file_path = print_request.file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=print_request.filename)
    else:
        messages.error(request, 'File not found')
        return redirect('dashboard')
