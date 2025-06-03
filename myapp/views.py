from django.shortcuts import render, redirect , get_object_or_404
from .forms import SignUpForm , PhotoForm , CommentForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout , authenticate, login
from django.shortcuts import render
from.models import Photo  
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            user.email = form.cleaned_data.get('email')
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')





@login_required 
def profile_view(request):
    try:
        user_photos = Photo.objects.filter(user=request.user).order_by('-uploaded_at')
        total_likes = sum(photo.likes.count() for photo in user_photos)
        
        
        print(f"Found {user_photos.count()} photos for user {request.user.username}")
        for photo in user_photos:
            print(f"Photo {photo.id}: {photo.title} - {photo.image.url}")
        
        context = {
            'user_photos': user_photos,
            'total_likes': total_likes,
        }
        return render(request, 'profile.html', context)
        
    except Exception as e:
        print(f"Error in profile_view: {str(e)}")
        
        return render(request, 'profile.html', {
            'user_photos': [],
            'total_likes': 0,
            'error': 'Could not load photos'
        })


def custom_logout(request): 
    logout(request) 
    return redirect('login') 

def home(request):  
    latest_photos = Photo.objects.all().order_by('-uploaded_at')[:6]  
    return render(request, 'home.html', {'latest_photos': latest_photos})



def photos_by_tag(request, tag):
    photos = Photo.objects.filter(tags__icontains=tag)
    return render(request, 'photo_by_tag.html', {'photos': photos, 'tag': tag})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})


def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    tags = photo.tags.split(",") if photo.tags else []
    comments = photo.comments.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.photo = photo
            new_comment.user = request.user
            new_comment.save()
            return redirect('photo_detail', photo_id=photo.id)
    else:
        comment_form = CommentForm()
    
    context = {
        'photo': photo,
        'tags': tags,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': photo.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False,
    }
    return render(request, 'photo_detail.html', context)

@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if photo.likes.filter(id=request.user.id).exists():
        photo.likes.remove(request.user)
        liked = False
    else:
        photo.likes.add(request.user)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': photo.total_likes()
        })
    
    return redirect('photo_detail', photo_id=photo.id)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Photo
from .forms import ProfileForm, PhotoForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Replace with your profile view name
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})



@login_required
def edit_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Replace with your profile view name
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'edit_photo.html', {'form': form, 'photo': photo})

@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk, user=request.user)
    if request.method == 'POST':
        photo.delete()
        return redirect('profile')  # Replace with your profile view name
    return render(request, 'delete.html', {'photo': photo})
