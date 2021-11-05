from accounts.models import Profile
from django import forms
from django.contrib.auth.models import AbstractUser


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline',
        'placeholder': 'Nombre'
    }), required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline',
            'placeholder': 'Apellido'
        }), required=False
    )
    pinture = forms.ImageField(label='Foto de perfil', required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline '
    }))
    banner = forms.ImageField(label='Portada', required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline '
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline',
        'placeholder': 'Ubicación'
    }), max_length=25, required=False)
    url = forms.URLField(label='Website URL', widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight text-gray-700 borderrounded shadow appearance-none focus:outline-none focus:shadow-outline',
        'placeholder': 'Pagina web'
    }), max_length=60, required=False)
    bio = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight text-gray-700 borderrounded shadow appearance-none focus:outline-none focus:shadow-outline',
        'placeholder': 'biografia'

    }), max_length=260, required=False)
    birthday = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline',
        'placeholder': 'Cumpleaños'
    }), required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'pinture',
                  'banner', 'location', 'url', 'bio', 'birthday')
