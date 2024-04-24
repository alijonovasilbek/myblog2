from django.db import models
from django.contrib.auth import  get_user_model
from django.urls import reverse
from  ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])






class Aricles(models.Model):
    title=models.CharField(max_length=255)
    summary=models.CharField(max_length=200,blank=True)
    body=RichTextField()
    photo=models.ImageField(upload_to='images/',blank=True)
    date=models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='articles')
    author=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )



    class Meta:
        ordering=['-date']
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail',args=[str(self.id)])


class Comment(models.Model):
    article=models.ForeignKey(Aricles,on_delete=models.CASCADE,related_name='comments')
    comment=models.CharField(max_length=150)
    author=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

    def get_obsolute_url(self):
        return reverse('article_list')


    class Meta:
        ordering=['-id']













