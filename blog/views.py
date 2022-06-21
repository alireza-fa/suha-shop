from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from blog.models import Category, Post, PostComment
from .forms import CommentForm


@method_decorator(cache_page(timeout=900), name='dispatch')
class BlogListView(View):
    template_name = 'blog/blog_grid.html'
    model = Post

    def get(self, request):
        posts = self.model.objects.all()[:8]
        return render(request, self.template_name, {"posts": posts})


class BlogDetailView(View):
    template_name = 'blog/blog_detail.html'
    class_form = CommentForm

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, self.template_name, {"post": post, "form": self.class_form(), "comments": post.comments.filter(is_active=True)})

    def post(self, request, slug):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = get_object_or_404(Post, slug=slug)
            PostComment.objects.create(user=request.user, post=post, message=cd['body'])
            string = render_to_string('blog/ajax/blog_detail.html', {"form": self.class_form()})
            return JsonResponse(data={"status": 'ok', "data": string})
        string = render_to_string('blog/ajax/blog_detail.html', {"form": form})
        return JsonResponse(data={"data": string})


@method_decorator(cache_page(timeout=900), name='dispatch')
class BlogListCategoryView(View):
    template_name = 'blog/blog_list.html'

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        return render(request, self.template_name, {"category": category})
