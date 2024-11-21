from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, URLForm
import pyshorteners
from .models import Profile
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import user_passes_test
import random
import string


def signuppage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'index.html', {'form': form})


def loginpage(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login/')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signup')
    context = {
        'user': request.user
    }
    return render(request, 'logout.html', context)


def generate_shortlink(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def redirect_shortlink(request, shortlink):
    record = get_object_or_404(Profile, shortlink=shortlink)
    return redirect(record.link)

@login_required(login_url='/login/')
def linkshort(request):
    username = request.user.username
    email = request.user.email

    short_url = None
    urltext = None

    if request.method == 'POST':
        form = URLForm(request.POST)
        if 'submitbutton' in request.POST:
            if form.is_valid():
                original_url = form.cleaned_data['original_url']
                title = form.cleaned_data['title']
                if Profile.objects.filter(user=request.user).count() >= 5:
                    urltext = 'You can only have up to 5 records.'
                else:
                    shortlink = generate_shortlink()
                    while Profile.objects.filter(shortlink=shortlink).exists():
                        shortlink = generate_shortlink()
                    Profile.objects.create(user=request.user, shortlink=shortlink, link=original_url, title=title)
                    short_url = request.build_absolute_uri(f"/{shortlink}")
                    urltext = 'Your shortened URL is: '
                form = URLForm(initial={'original_url': original_url, 'title': title})
                form.fields['original_url'].widget.attrs['readonly'] = 'readonly'
                form.fields['title'].widget.attrs['readonly'] = 'readonly'
                return render(request, 'home.html', {'username': username, 'email': email, 'form': form, 'short_url': short_url, 'urltext': urltext})
        if 'resetbutton' in request.POST:
            form = URLForm()
            short_url = None
            urltext = None
    else:
        form = URLForm()
    return render(request, 'home.html', {'username': username, 'email': email, 'form': form, 'short_url': short_url, 'urltext': urltext})


@login_required(login_url='/login/')
def dashboard(request):
    username = request.user.username
    email = request.user.email
    query = request.GET.get('query', '')
    records = Profile.objects.filter(user=request.user)
    if query:
        records = records.filter(link__icontains=query) | records.filter(title__icontains=query)
    paginator = Paginator(records.order_by('-created_at'), 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for record in page_obj.object_list:
        record.time = record.created_at.strftime('%d %b %Y, %I:%M%p')
        record.short_url = request.build_absolute_uri(f"/{record.shortlink}")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'records': [
                {
                    'title': record.title,
                    'shortlink': record.short_url,
                    'link': record.link,
                    'time': record.time
                } for record in page_obj.object_list
            ]
        })
    return render(request, 'dashboard.html', {'username': username, 'email': email, 'records': records, 'page_obj': page_obj})


def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin, login_url='/login/')
def aboutus(request):
    username = request.user.username
    email = request.user.email
    return render(request, 'aboutus.html', {'username': username, 'email': email})


@login_required(login_url='/login/')
def aboutus(request):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
    else:
        username = None
    return render(request, 'aboutus.html', {'username': username, 'email': email})


@login_required(login_url='/login/')
def edit_record(request, username, id):
    record = get_object_or_404(Profile, id=id, user__username=username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=record)
        if form.is_valid():
            link = form.cleaned_data.get('link')
            shortlink = generate_shortlink()
            while Profile.objects.filter(shortlink=shortlink).exists():
                shortlink = generate_shortlink()
            record.shortlink = shortlink
            form.save()      
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=record)

    return render(request, 'edit_record.html', {'username': username, 'form': form})


@login_required(login_url='/login/')
def delete_record(request, id):
    if request.method == 'DELETE':
        record = get_object_or_404(Profile, id=id, user=request.user)
        if record.user == request.user:
            record.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=400)
