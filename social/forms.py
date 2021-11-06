from django import forms
from .models import BodyPost, SocialPost, SocialComment, Categories, Tags

BODY_OPTIONS = (
    ('TITULO', 'TITULO'),
    ('SUBTITULO', 'SUBTITULO'),
    ('PARRAFO', 'PARRAFO'),
    ('IMAGEN', 'IMAGEN'),
    ('CODIGO', 'CODIGO'),
)
STATUS_OPTIONS = (
    ('PUBLISHED', 'PUBLISHED'),
    ('DRAF', 'DRAF'),
    ('PENDING', 'PENDING')
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

    banner = forms.ImageField(label='Banner',
                              required=True, widget=forms.FileInput(attrs={'class': 'w-full text-center flex flex-col items-center justify-center items-center ', }))
    label = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)
    category = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)

    class Meta:
        model = SocialPost
        fields = ['label', 'description', 'title',
                  'category', 'banner', ]


class BodyPostForm(forms.ModelForm):
    type = forms.ChoiceField(required=True, widget=forms.Select(attrs={
        'class': 'block w-52 text-gray-700 py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
    }), choices=BODY_OPTIONS)
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'flex-1 appearance-none border border-gray-300 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent',
        'rows': '3',
        'placeholder': 'contenido'
    }), required=False)
    
    imagen = forms.ImageField(label='img',required=False,widget=forms.FileInput(attrs={'class': 'w-full text-center flex flex-col items-center justify-center items-center ', }))
    class Meta:
        model = BodyPost
        fields = ['type', 'body', 'imagen']


class SocialCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'shadow-sm focus:ring-green-500 focus:border-green-500 dark:bg-dark-third dark:border-dark-third dark:text-dark-txt flex max-w-full sm:text-sm border-gray-300 rounded-md',
            'placeholder': 'Escriba su comentario'
        }),
        required=True
    )

    class Meta:
        model = SocialComment
        fields = ['comment']


class EditPostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline',
        'placeholder': 'Nombre'
    }), required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline',
        'placeholder': 'Nombre'
    }), required=False)
    banner = forms.ImageField(label='Portada', required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline '
    }))
    
    category = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)
    label = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)
    status = forms.ChoiceField(required=True, widget=forms.Select(attrs={
        'class': 'block w-52 text-gray-700 py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500',
    }), choices=STATUS_OPTIONS)

    class Meta:
        model = SocialPost
        fields = ('description', 'title','label',
                  'category', 'banner','status',)

class EditCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-green-500 focus:bg-white focus:ring-2 focus:ring-green-200 h-32 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out',
            'placeholder': 'Edite su comentario'
        }),
        required=True
    )

    class Meta:
        model = SocialComment
        fields = ['comment']