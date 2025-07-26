from django.shortcuts import render,redirect,get_object_or_404
from django .contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.models import  NewsPost
# Create your views here.
def home(request):
    posts = NewsPost.objects.filter(is_published=True).order_by('-created_at')[:6]  # Get the latest 6 published posts
    return render(request, 'index.html', {'posts': posts})

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
    return redirect('home')

@login_required
def posts(request):
    posts =  NewsPost.objects.all()
    return render(request, 'posts.html',{'posts':posts, 'post_count': posts.count()})


@login_required
def category_posts(request, category_name):
    posts = NewsPost.objects.filter(category=category_name, is_published=True).order_by('-created_at')
    return render(request, 'category.html', {
        'posts': posts,
        'category': category_name.replace('_', ' ').title()
    })

from .models import NewsPost, Like, Comment, SavedPost
from django.http import JsonResponse

@login_required
def read_more(request, slug):
    post = get_object_or_404(NewsPost, slug=slug)
    comments = post.comments.all()
    likes_count = post.likes.count()
    is_liked = post.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    is_saved = post.saves.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'read-more.html', {
        'post': post,
        'comments': comments,
        'likes_count': likes_count,
        'is_liked': is_liked,
        'is_saved': is_saved,
    })

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(NewsPost, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})

@login_required
def toggle_save(request, post_id):
    post = get_object_or_404(NewsPost, id=post_id)
    saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        saved.delete()
        is_saved = False
    else:
        is_saved = True
    return JsonResponse({'saved': is_saved})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('comment')
        post = get_object_or_404(NewsPost, id=post_id)
        Comment.objects.create(user=request.user, post=post, text=text)
    return redirect('read_more', slug=post.slug)

@login_required
def liked_posts(request):
    liked_posts = NewsPost.objects.filter(likes__user=request.user)
    return render(request, 'liked-posts.html', {'posts': liked_posts})

@login_required
def saved_posts(request):
    saved_posts = NewsPost.objects.filter(saves__user=request.user)
    return render(request, 'saved-posts.html', {'posts': saved_posts})


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    
    return render(request, 'profile.html')



from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevent logout
            messages.success(request, "Password changed successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from .models import NewsPost, Like, SavedPost
from collections import Counter
from django.db.models import Count
import matplotlib.pyplot as plt
import os

def generate_analytics():
    users = User.objects.all()
    posts = NewsPost.objects.all()
    likes = Like.objects.select_related('post', 'user')
    saves = SavedPost.objects.select_related('post', 'user')

    now_time = now()
    past_24hrs = now_time - timedelta(hours=24)

    # Total & recent users
    total_users = users.count()
    new_users_24hrs = users.filter(date_joined__gte=past_24hrs).count()

    # Likes and Saves per post
    post_likes = Like.objects.values('post').annotate(total=Count('id')).order_by('-total')
    post_saves = SavedPost.objects.values('post').annotate(total=Count('id')).order_by('-total')

    most_liked_post = post_likes.first()
    least_liked_post = post_likes.last()
    most_saved_post = post_saves.first()
    least_saved_post = post_saves.last()

    # Category with most likes
    category_likes = Like.objects.values('post__category').annotate(total=Count('id')).order_by('-total')

    # Most active users
    top_likers = Like.objects.values('user__username').annotate(total=Count('id')).order_by('-total')
    top_savers = SavedPost.objects.values('user__username').annotate(total=Count('id')).order_by('-total')

    # Dormant users
    liked_users = Like.objects.values_list('user_id', flat=True)
    saved_users = SavedPost.objects.values_list('user_id', flat=True)
    active_users = set(list(liked_users) + list(saved_users))
    dormant_users = users.exclude(id__in=active_users)

    # Generate category bar chart
    top5 = category_likes[:5]
    categories = [item['post__category'] for item in top5]
    values = [item['total'] for item in top5]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, values, color='darkcyan')
    plt.title('Top 5 Categories by Likes')
    plt.ylabel('Likes')
    plt.xlabel('Category')
    chart_path = 'static/charts/category_likes.png'
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    plt.savefig(chart_path)
    plt.close()

    return {
        'total_users': total_users,
        'new_users_24hrs': new_users_24hrs,
        'most_liked_post': NewsPost.objects.get(id=most_liked_post['post']) if most_liked_post else None,
        'least_liked_post': NewsPost.objects.get(id=least_liked_post['post']) if least_liked_post else None,
        'most_saved_post': NewsPost.objects.get(id=most_saved_post['post']) if most_saved_post else None,
        'least_saved_post': NewsPost.objects.get(id=least_saved_post['post']) if least_saved_post else None,
        'category_with_most_likes': category_likes[0]['post__category'] if category_likes else None,
        'top_liker': top_likers[0]['user__username'] if top_likers else None,
        'top_saver': top_savers[0]['user__username'] if top_savers else None,
        'dormant_users_count': dormant_users.count(),
        'chart_path': '/' + chart_path
    }

def analytics_view(request):
    analytics = generate_analytics()
    return render(request, 'analytics.html', analytics)



