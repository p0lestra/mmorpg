from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from board.forms import PostForm, ReplyForm
from board.models import Post, Reply


class PostsList(ListView):
    model = Post
    template_name = 'posts_template.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged'] = self.request.user.is_authenticated
        context['current_user'] = self.request.user
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail_template.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies_by_post_id = Reply.objects.filter(post=self.kwargs['pk']).order_by('-date_posted')
        context['is_logged'] = self.request.user.is_authenticated
        context['replys'] = replies_by_post_id
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create_template.html'
    context_object_name = 'post_create'
    success_url = '/posts/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_author = self.request.user
        post.save()
        return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post_edit'
    success_url = '/posts/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class ReplyAdd(CreateView):
    form_class = ReplyForm
    model = Reply

    template_name = 'reply_add.html'
    context_object_name = 'reply_create'

    success_url = '/posts/'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.post = get_object_or_404(Post, id=self.kwargs['pk'])
        form.save()
        return redirect('post', reply.post.pk)


class Replies(ListView):
    model = Reply
    template_name = 'replies.html'
    context_object_name = 'replies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies_to_author = Reply.objects.filter(post__post_author=self.request.user)
        context['replies_to_author'] = replies_to_author
        return context


def delete_reply(self, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    return redirect('/posts/')  # FIXME сделать переход на страницу отклика


def allow_reply(self, pk):
    reply = Reply.objects.get(id=pk)
    reply.is_allowed = True
    return redirect('/posts/')  # FIXME попробовать переход на пост


def delete_post(self, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/posts/')
