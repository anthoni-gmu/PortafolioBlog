from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from .models import BodyPost, SocialPost, SocialComment, Categories,Tags
from .forms import BodyPostForm, SocialCommentForm,EditPostForm,EditCommentForm,EditBodyPostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from accounts.models import Profile
from django.db.models import Count
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
User = get_user_model()
from django.db.models import Max



class HomeBlogView(View):
    def get(self, request, *args, **kwargs):
        post = SocialPost.objects.all()[:5]
        lastPost =SocialPost.objects.all().order_by('-create_on')[0]
        penultimatePost =SocialPost.objects.all().order_by('-create_on')[1]
        lastGrup =SocialPost.objects.all().order_by('-create_on')[2:5]
        
        categories = Categories.objects.all()
        coutCate = SocialPost.objects.values('category').annotate(
            Count('category')).order_by('category')
        mylist = zip(categories, coutCate)
        
        context = {
            'post':post,
            'lastPost':lastPost,
            'penultimatePost':penultimatePost,
            'lastGrup':lastGrup,
            'mylist':mylist
        }
        return render(request, 'blog/index.html', context)

    def post(self, request, *args, **kwargs):
        context = {
        }
        return render(request, 'blog/index.html', context)

class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        form = BodyPostForm()
        comments = SocialComment.objects.filter(
            post=post).order_by('-create_on')
        bodyposts = BodyPost.objects.filter(post=post).order_by('create_on')
        formComment = SocialCommentForm()

        categories = Categories.objects.all()
        coutCate = SocialPost.objects.values('category').annotate(
            Count('category')).order_by('category')
        mylist = zip(categories, coutCate)

        relacionPost = SocialPost.objects.all()[:5]

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'bodyposts': bodyposts,
            'formComment': formComment,
            'mylist': mylist,
            'relacionPost': relacionPost,

        }
        return render(request, 'pages/social/detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        form = BodyPostForm(request.POST, request.FILES)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        context = {
            'post': post,
            'form': form,
        }
        return redirect('social:post-detail', pk=pk)


class CategorySearch(View):
    def get(self, request, *args, **kwargs):
        
        query = self.request.GET.get('query')
        if query=="TODAS":
            category_list = SocialPost.objects.all()
        else:
            category_list = SocialPost.objects.filter(Q(category__name=query))
        page =request.GET.get('page',1)
        paginator =Paginator(category_list,6)
        try:
            categories_list=paginator.page(page)
        except PageNotAnInteger:
            categories_list = paginator.page(1)
        except EmptyPage:
            categories_list = paginator.page(paginator.num_pages)
        categories = Categories.objects.all()
        coutCate = SocialPost.objects.values('category').annotate(
            Count('category')).order_by('category')
        mylist = zip(categories, coutCate)
        
        post = SocialPost.objects.all()
        
        
        context = {
            'categories_list': categories_list,
            'query': query,
            'mylist':mylist,
            'post':post
        }
        return render(request, 'pages/social/search.html', context)


class TagSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        if query=="TODAS":
            tag_list = SocialPost.objects.all()
        else:
            tag_list = SocialPost.objects.filter(Q(label__name=query))
            
        page =request.GET.get('page',1)
        paginator =Paginator(tag_list,6)
        
        try:
            tags_list=paginator.page(page)
        except PageNotAnInteger:
            tags_list = paginator.page(1)
        except EmptyPage:
            tags_list = paginator.page(paginator.num_pages)
        
        
        tags = Tags.objects.all()
        coutTage = SocialPost.objects.values('label').annotate(
            Count('label')).order_by('label')
        mylist = zip(tags, coutTage)
        
        post = SocialPost.objects.all()
        context = {
            'tag_list': tags_list,
            'query': query,
            'mylist': mylist,
            'post': post,
        }
        return render(request, 'pages/social/search_tag.html', context)


@login_required
def EditPost(request, pk):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    logged_in_user = request.user
    post = SocialPost.objects.get(pk=pk)

    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.title = form.cleaned_data.get('title')
            post.description = form.cleaned_data.get('description')
            post.banner = form.cleaned_data.get('banner')
            category = form.cleaned_data.get('category')
            label=form.cleaned_data.get('label')
            
            for la in label:
                post.label.add(la)
            post.label.all()
                
            for cat in category:
                post.category.add(cat)
            post.category.all()
            
            post.status = form.cleaned_data.get('status')
            post.save()
            return redirect('users:profile', username=request.user.username)
        else:
            return redirect('home')
    else:
        formEditPost = EditPostForm(instance=post)
        post = SocialPost.objects.get(pk=pk)

    context = {
        'form': formEditPost,
        'post': post
    }
    return render(request, 'pages/social/edit.html', context)








class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SocialPost
    template_name = 'pages/social/delete.html'
    success_url = reverse_lazy('home') #mandar al perfil



    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SocialComment
    template_name = "pages/social/comment_delete.html"

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    
class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=post_pk)
        parent_comment = SocialComment.objects.get(pk=pk)
        formComment = SocialCommentForm(request.POST)
        if formComment.is_valid():
            new_comment = formComment.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()
        return redirect('social:post-detail', pk=post_pk)


class CommentFather(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        formComment = SocialCommentForm(request.POST)
        if formComment.is_valid():
            new_comment = formComment.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        return redirect('social:post-detail', pk=pk)


class AddBodyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        form = BodyPostForm(request.POST, request.FILES)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()

        return redirect('social:post-detail', pk=pk)





class CommentEditView(UpdateView):

    model = SocialComment
    form_class = EditCommentForm
    template_name = 'pages/social/comment_edit.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk': pk})
    

class EditBodyPostView(UpdateView):

    model = BodyPost
    form_class = EditBodyPostForm
    template_name = 'pages/social/editbodypost.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk': pk})

class BodyPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BodyPost
    template_name = "pages/social/body_delete.html"

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk': pk})

    def test_func(self):
        bodypost = self.get_object()
        return self.request.user == bodypost.post.author

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(
            Q(user__username__icontains=query))
        context = {
            'profile_list': profile_list,
        }
        return render(request, 'pages/social/search.html', context)
