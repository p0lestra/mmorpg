from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from board.forms import PostForm, ReplyForm
from board.models import Post, Reply


class PostsList(ListView):
    model = Post
    template_name = 'posts_template.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged'] = self.request.user.is_authenticated
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail_template.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged'] = self.request.user.is_authenticated
        replies_by_post_id = Reply.objects.filter(post=self.kwargs['pk']).order_by('-date_posted')
        
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

        return super().form_valid(form)
