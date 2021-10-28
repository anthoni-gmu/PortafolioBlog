from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User=get_user_model()

def user_directory_path(instance,filename):
    return 'users/socialpost/{0}'.format(filename)

def dm_directory_path(instance,filename):
    return 'users/messages/{0}'.format(filename)

CATEGORIA_OPTIONS=(
    ('WEB','WEB'),
    ('ALGORITMOS','ALGORITMOS'),
    ('REDES','REDES'),
    ('SEGURIDAD','SEGURIDAD'),
    ('DESKTOP','DESKTOP'),
    ('LINUX','LINUX'),
)
class SocialPost(models.Model):
    title=models.CharField(max_length=400,null=True,blank=True) 
    description=models.CharField(max_length=400,null=True,blank=True)  
    banner=models.ImageField(default='users/user_default_bg.jpg',upload_to=user_directory_path)
    body=models.TextField()
    image=models.ManyToManyField('Image',blank=True)
    create_on = models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='social_post_author')
    category=models.CharField(max_length=15,choices=CATEGORIA_OPTIONS,default='ALGORITMOS')

    
class SocialComment(models.Model):
    comment =models.TextField() 
    create_on = models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='social_comment_author')
    post=models.ForeignKey('SocialPost',on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='+')
    
    @property
    def children(self):
        return SocialComment.objects.filter(parent=self).order_by('-create_on').all()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
class Image(models.Model):
    image=models.ImageField(upload_to=user_directory_path,blank=True,null=True)