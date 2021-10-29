from django import forms
from .models import BodyPost, SocialPost, SocialComment

CATEGORIA_OPTIONS = (
    ('WEB', 'WEB'),
    ('ALGORITMOS', 'ALGORITMOS'),
    ('REDES', 'REDES'),
    ('SEGURIDAD', 'SEGURIDAD'),
    ('DESKTOP', 'DESKTOP'),
    ('LINUX', 'LINUX'),
)
BODY_OPTIONS = (
    ('TITULO', 'TITULO'),
    ('SUBTITULO', 'SUBTITULO'),
    ('PARRAFO', 'PARRAFO'),
    ('IMAGEN', 'IMAGEN'),
    ('CODIGO', 'CODIGO'),
)


class SocialPostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'rounded-lg border-transparent flex-1 appearance-none border border-gray-300 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 shadow-sm text-base focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent',
        'placeholder': 'Titulo'
    }), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'flex-1 appearance-none border border-gray-300 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent',
        'placeholder': 'Descripción',
        'rows': '2',
    }), required=True)

    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'flex-1 appearance-none border border-gray-300 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent',
        'rows': '3',
        'placeholder': 'contenido'
    }), required=True)

    banner = forms.ImageField(label='Banner Picture',
                              required=False, widget=forms.FileInput)

    image = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'relative dark:text-dark-txt dark:bg-dark-second cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500',
        'multiple': True
    }), required=False)

    category = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'block w-52 text-gray-700 py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
    }), choices=CATEGORIA_OPTIONS)

    class Meta:
        model = SocialPost
        fields = ['body', 'description', 'title',
                  'category', 'banner', 'image']


class BodyPostForm(forms.ModelForm):
    type = forms.ChoiceField( required=True,widget=forms.Select(attrs={
        'class': 'block w-52 text-gray-700 py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
    }), choices=BODY_OPTIONS)
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'flex-1 appearance-none border border-gray-300 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent',
        'rows': '3',
        'placeholder': 'contenido'
    }), required=False)
    imagen = forms.ImageField(label='Banner Picture',
                              required=False, widget=forms.FileInput)

    class Meta:
        model = BodyPost
        fields = ['type', 'body', 'imagen']


class SocialCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 dark:bg-dark-third dark:border-dark-third dark:text-dark-txt flex max-w-full sm:text-sm border-gray-300 rounded-md',
            'rows': '1',
            'placeholder': 'Comment Something...'
        }),
        required=True
    )

    class Meta:
        model = SocialComment
        fields = ['comment']
