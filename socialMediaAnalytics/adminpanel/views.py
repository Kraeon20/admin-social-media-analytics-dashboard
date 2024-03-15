import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from dotenv import load_dotenv
from .utils import (get_facebook_follower_count,
                    get_facebook_total_post_likes, 
                    get_instagram_follower_count,
                    get_instagram_post_likes, 
                    get_twitter_follower_count,
                    get_twitter_post_likes)


load_dotenv()


page_id = os.environ.get('FACEBOOK_PAGE_ID')
access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')


@login_required
def dashboard(request):
    # total followers accross all platforms
    total_followers = (get_facebook_follower_count(page_id, access_token) +
                       get_twitter_follower_count() +
                       get_instagram_follower_count())
    
    # total likes accross all platforms
    total_likes = (get_facebook_total_post_likes(page_id, access_token) +
                   get_instagram_post_likes() +
                   get_twitter_post_likes())
    
    # Pass total_likes to the template context
    context = {
        'facebook_followers': get_facebook_follower_count(page_id, access_token),
        'instagram_followers': get_instagram_follower_count(),
        'twitter_followers': get_twitter_follower_count(),
        'facebook_likes': get_facebook_total_post_likes(page_id, access_token),
        'instagram_likes': get_instagram_post_likes(),
        'twitter_likes': get_twitter_post_likes(),
        'total_followers': total_followers,
        'total_likes': total_likes,
    }
    
    return render(request, 'dashboard.html', context)



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Handle invalid login
            pass
    return render(request, 'login.html')









def reset_authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User with the provided username does not exist.')
            return redirect('reset-auth')

        # Reset password
        user.set_password(password)
        user.save()

        messages.success(request, 'Authentication reset successfully.')
        return redirect('reset-auth')

    return render(request, 'reset_authentication.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')