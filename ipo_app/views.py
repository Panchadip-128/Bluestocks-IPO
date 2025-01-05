from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model  # Use get_user_model to access the custom User model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import logging
from django.contrib.auth.decorators import login_required


from .models import IPO, Subscription, Transaction

logger = logging.getLogger(__name__)

# IPO List View
def list_ipos(request):
    ipos = IPO.objects.all()
    return render(request, 'list_ipos.html', {'ipos': ipos})


# Stock List View
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})


# Home View
def home(request):
    return render(request, 'list_ipos.html')


# Subscription View
def subscribe_to_ipo(request, ipo_id):
    ipo = get_object_or_404(IPO, pk=ipo_id)
    # Process the subscription logic here
    return render(request, 'subscribe.html', {'ipo': ipo})


# User Transactions View
def user_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions.html', {'transactions': transactions})


# Register View (User Authentication)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Login View (User Authentication)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'sgin.html', {'form': form})


from django.core.mail import BadHeaderError

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        logger.debug(f"Received email: {email}")  # Debugging statement

        try:
            # Look for user by email
            user = get_user_model().objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())  # Encoding user ID
            logger.debug(f"Generated UID: {uid}, Token: {token}")  # Debugging statement

            # Create the reset link
            reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
            logger.debug(f"Reset link: {reset_link}")  # Debugging statement

            # Send the reset email
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_link}',
                'panchadip128@gmail.com',  # Sender's email
                [user.email],  # Recipient's email
                fail_silently=False,
            )
            logger.info(f"Email sent successfully to {user.email}")  # Log email sent
            return redirect('password_reset_done')  # Redirect to the reset done page
        except get_user_model().DoesNotExist:
            logger.error("Email not found.")
            return render(request, 'forgot_pw.html', {'error': 'Email not found.'})
        except BadHeaderError:
            logger.error("Invalid header found.")  # Log invalid header error
            return render(request, 'forgot_pw.html', {'error': 'Invalid email header.'})
        except Exception as e:
            logger.error(f"Error: {e}")  # Log any other error
            return render(request, 'forgot_pw.html', {'error': 'Error sending email.'})

    return render(request, 'forgot_pw.html')


# Password Reset Confirm View
def password_reset_confirm_view(request, uidb64, token):
    try:
        # Decode the UID
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        raise Http404("Invalid link")

    # Check if the token is valid for this user
    if not default_token_generator.check_token(user, token):
        raise Http404("Invalid link")

    # Handle POST request to reset the password
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')  # Redirect to the password reset complete page
    else:
        form = SetPasswordForm(user)

    return render(request, 'password_reset_confirm.html', {'form': form})

def dashboard_view(request):
    logger.debug("Loading dashboard view")
    return render(request, 'dashboard.html')