from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


def user_directory_path(instance, filename):
    return 'users/socialpost/{0}'.format(filename)


def dm_directory_path(instance, filename):
    return 'users/messages/{0}'.format(filename)


class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


STATUS_OPTIONS = (
    ('PUBLISHED', 'PUBLISHED'),
    ('DRAF', 'DRAF'),
    ('PENDING','PENDING')
)

class SocialPost(models.Model):
    title = models.CharField(max_length=400, null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    banner = models.ImageField(
        default='users/user_default_bg.jpg', upload_to=user_directory_path)
    create_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='social_post_author')
    category = models.ManyToManyField(Categories)
    label = models.ManyToManyField(Tags)
    status = models.CharField(
        max_length=15, choices=STATUS_OPTIONS, default='DRAF')
    

    @property
    def get_comment_count(self):
        return self.socialcomment_set.all().count()
    



BODY_OPTIONS = (
    ('TITULO', 'TITULO'),
    ('SUBTITULO', 'SUBTITULO'),
    ('PARRAFO', 'PARRAFO'),
    ('IMAGEN', 'IMAGEN'),
    ('CODIGO', 'CODIGO'),
)


class BodyPost(models.Model):
    post = models.ForeignKey('SocialPost', on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=15, choices=BODY_OPTIONS, default='TITULO')
    create_on = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(
        blank=True, null=True, upload_to=user_directory_path)


class SocialComment(models.Model):
    comment = models.TextField()
    create_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='social_comment_author')
    post = models.ForeignKey('SocialPost', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return SocialComment.objects.filter(parent=self).order_by('-create_on').all()
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
      
   

class Image(models.Model):
    image = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)
