from django.contrib import admin
from .models import BodyPost, SocialPost,SocialComment ,Image

admin.site.register(SocialPost)
admin.site.register(SocialComment)
admin.site.register(Image)
admin.site.register(BodyPost)


#min 30
