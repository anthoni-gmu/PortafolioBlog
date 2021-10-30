from django.contrib import admin
from .models import BodyPost, Categories, SocialPost,SocialComment ,Image, Tags

admin.site.register(SocialPost)
admin.site.register(SocialComment)
admin.site.register(Image)
admin.site.register(BodyPost)
admin.site.register(Categories)
admin.site.register(Tags)



#min 30
