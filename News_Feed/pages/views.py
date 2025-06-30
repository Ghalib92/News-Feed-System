from django.shortcuts import render,redirect,get_object_or_404
from django .contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.models import  NewsPost
# Create your views here.
def home(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful! Welcome back.')
            return redirect('dashboard')  # Redirect to homepage or dashboard
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')

    return render(request, 'login.html')

 


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']   
        last_name = request.POST['last_name'] 
        username = request.POST['username'] 
        password1 = request.POST['password1'] 
        password2 = request.POST['password2']  # Fixed the typo
        email = request.POST['email']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')  # Redirect back to the signup page

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')  # Redirect to login page after successful signup

    return render(request, 'signup.html')  # Show signup form if request is not POST

@login_required
def dashboard(request):
    return render(request,'dashboard.html')





def logout(request):
    auth.logout(request)
    return redirect('login')

def posts(request):
    posts =  NewsPost.objects.all()
    return render(request, 'posts.html',{'posts':posts, 'post_count': posts.count()})



def category_posts(request, category_name):
    posts = NewsPost.objects.filter(category=category_name, is_published=True).order_by('-created_at')
    return render(request, 'category.html', {
        'posts': posts,
        'category': category_name.replace('_', ' ').title()
    })



def read_more(request, slug):
    post = get_object_or_404 (NewsPost, slug=slug)
    return render (request, 'read-more.html', {'post':post})

