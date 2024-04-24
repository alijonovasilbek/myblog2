from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
from .models import Aricles, Category
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


class ArticlesListView(ListView):
    model = Aricles
    template_name = "article_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Aricles.objects.all()
        context['categories'] = Category.objects.all()
        return context

    paginator_class = 3

    def get_queryset(self):
        if 'keyword' in self.request.GET:
             queryset = (Aricles.objects.filter(title__icontains=self.request.GET['keyword']) |
                    Aricles.objects.filter(summary__icontains=self.request.GET['keyword']) |
                    Aricles.objects.filter(body__icontains=self.request.GET['keyword']))
        else:
            queryset=Aricles.objects.all()
        if 'category' in self.request.GET:
            queryset= Aricles.objects.filter(categories=self.request.GET['category'])
        return queryset


class ArticleDetailView(DetailView):
    model = Aricles
    template_name = "article_detail.html"

    context_object_name = "article"


class ArticleDetailView1(DetailView):
    model = Aricles
    template_name = "add_comment_to_article.html"


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Aricles
    fields = ("title", "summary", "body", "photo")
    template_name = "article_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Aricles
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Aricles
    template_name = "article_new.html"
    fields = (
        "title",
        "summary",
        "body",
        "categories",
        "photo",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    #
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_superuser


from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


from django.urls import reverse_lazy


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "add_comment_to_article.html"

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.article_id = self.kwargs["pk"]
        form.instance.author = self.request.user
        return super().form_valid(form)
