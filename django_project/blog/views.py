from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Tag
from .forms import PostForm
from .models import Post, Category
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

# Serve sw.js as JavaScript
@require_GET
@never_cache
def service_worker(request):
    # Read the static sw.js file and return it with correct content type
    sw_js = open('blog/static/blog/sw.js').read()
    return HttpResponse(sw_js, content_type='application/javascript')

# Offline page
def offline(request):
    return render(request, 'blog/offline.html')

def home(request):
    context = {
        'posts': Post.objects.all()  # Setting posts
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get category or tag from URL (used for filtering)
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')

        # Filter posts by selected category
        if category:
            queryset = queryset.filter(category__slug=category)

        # Filter posts by selected tag
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Send all categories to template for navigation/filtering
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm # Use custom form to allow tag typing

    def form_valid(self, form):
        # Automatically assign logged-in user as author
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm # Use same form for editing

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Only allow users to edit their OWN posts
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})