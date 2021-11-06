from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from .models import BodyPost, SocialPost, SocialComment, Categories
from .forms import BodyPostForm, SocialCommentForm,EditPostForm,EditCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from accounts.models import Profile
from django.db.models import Count
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage
User = get_user_model()


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
        
        
            
        
        p=Paginator(category_list,2)
        
        print('Numero de paginas')
        print(p.num_pages)
        
        page_num=request.GET.get('page',1)
        try:
            page=p.page(page_num)
        except EmptyPage:
            page=p.page(1)
        
        categories = Categories.objects.all()
        coutCate = SocialPost.objects.values('category').annotate(
            Count('category')).order_by('category')
        mylist = zip(categories, coutCate)
        
        
        
        post= SocialPost.objects.all()
        context = {
            'category_list': page,
            'query': query,
            'mylist':mylist,
            'post':post,
        }
        return render(request, 'pages/social/search.html', context)

class TagSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        tag_list = SocialPost.objects.filter(Q(label__name=query))
        context = {
            'tag_list': tag_list,
            'query': query
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
    # hacer que el editar sea seguro


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(
            Q(user__username__icontains=query))
        context = {
            'profile_list': profile_list,
        }
        return render(request, 'pages/social/search.html', context)
