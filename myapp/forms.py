from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import Photo , Comment , Profile

class SignUpForm(UserCreationForm): 
    email = forms.EmailField(required=True) 
    class Meta: 
        model = User 
        fields = ('username', 'email', 'password1', 'password2')

    
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Add a comment...'
            })
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'full_name', 'bio']  # Add any other fields you have

 # Add any other fields you have