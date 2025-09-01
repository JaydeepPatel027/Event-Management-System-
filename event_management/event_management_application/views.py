from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import EventCategory, EventService, ServiceOption  # 👈 use the correct model name


def login(request):
    if request.method == 'POST' and 'login' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Fetch user by Email_id
        with connection.cursor() as cursor:
            cursor.execute("SELECT Name, Password FROM client_details WHERE Email_id=%s", [email])
            row = cursor.fetchone()

        if row:
            db_name, db_password = row
            if db_password == password:
                request.session['user'] = db_name
                messages.success(request, f"Welcome back {db_name}!")
                return redirect('client_dashboard')
            else:
                messages.error(request, "Invalid password")
                return redirect('login_page')
        else:
            messages.error(request, "Email not found")
            return redirect('login_page')

    elif request.method == 'POST' and 'signup' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('Contact_Number')
        city = request.POST.get('city')
        password = request.POST.get('password')

        # Convert contact_number to integer safely
        try:
            contact_number = int(contact_number)
        except ValueError:
            messages.error(request, "Invalid contact number format")
            return redirect('login_page')

        with connection.cursor() as cursor:
            # Check if Email already exists
            cursor.execute("SELECT Email_id FROM client_details WHERE Email_id=%s", [email])
            if cursor.fetchone():
                messages.error(request, "Email already registered")
                return redirect('login_page')

            # Insert new record
            cursor.execute(
                """
                INSERT INTO client_details (Name, Email_id, Contact_Number, City, Password)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [name, email, contact_number, city, password]
            )
        transaction.commit()

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login_page')

    # GET request renders login page with optional messages
    return render(request, "login_page.html")


# ------------------- OTP FLOW -------------------

def send_otp(request):
    """
    Generates and emails a 6-digit OTP to the given email.
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if email exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT Email_id FROM client_details WHERE Email_id=%s", [email])
            if not cursor.fetchone():
                return JsonResponse({'status': 'error', 'message': 'Email not found!'})

        # Generate OTP
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['otp_email'] = email

        # Send OTP via email
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            '23012012001@gnu.ac.in',  # From email
            [email],
            fail_silently=False
        )

        return JsonResponse({'status': 'success', 'message': 'OTP sent successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def reset_password(request):
    """
    Handle reset password from popup on login page with OTP verification.
    """
    if request.method == 'POST':
        email = request.session.get('otp_email')
        session_otp = request.session.get('otp')
        input_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not all([email, session_otp]):
            messages.error(request, "OTP session expired. Please try again.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if str(input_otp) != str(session_otp):
            messages.error(request, "Invalid OTP!")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE client_details SET Password=%s WHERE Email_id=%s",
                [new_password, email]
            )
            transaction.commit()

        # Clear OTP from session
        request.session.pop('otp', None)
        request.session.pop('otp_email', None)

        messages.success(request, "Password reset successfully!")
        return redirect('login_page')

    return redirect('login_page')


# ------------------- DASHBOARD & LOGOUT -------------------

def client_dashboard(request):
    return render(request, 'client_dashboard.html')


def client_event_detail(request, event_id):
    # fetch one event by ID
    event = get_object_or_404(EventCategory, pk=event_id)
    return render(request, "client_event_detail_page.html", {"event": event})

def client_event_list_page(request):
    events = EventCategory.objects.all()
    return render(request, "client_event_list_page.html", {"events": events})


def event_detail(request, event_id):
    category = get_object_or_404(EventCategory, event_id=event_id)
    images = category.images.all()
    options = category.options.all()

    # Group options by type (Cake, Decoration, etc.)
    option_groups = {}
    for opt in options:
        option_groups.setdefault(opt.option_type, []).append(opt)

    return render(request, "event_detail.html", {
        "category": category,
        "images": images,
        "option_groups": option_groups,
    })

def client_event_detail(request, event_id):
    # Fetch the selected event
    event = get_object_or_404(EventCategory, pk=event_id)

    # Fetch all services for the event along with their options
    services = event.services.prefetch_related('options').all()

    # Prepare structured data for template
    service_data = []
    for service in services:
        service_data.append({
            "service_id": service.service_id,
            "service_name": service.service_name,
            "options": service.options.all(),
        })

    context = {
        "event": event,
        "services": service_data,
    }
    return render(request, "client_event_detail_page.html", context)


def select_packages(request):
    return redirect('client_dashboard')

def date_location(request):
    return redirect('client_dashboard')

def next_step(request):
    return redirect('client_dashboard')

def logout(request):
    auth_logout(request)
    if 'user' in request.session:
        del request.session['user']
    messages.success(request, "You have logged out.")
    return redirect('login_page')

