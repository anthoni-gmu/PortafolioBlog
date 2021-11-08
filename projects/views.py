from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.
class ProjectHomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'projects/projects.html', context)
