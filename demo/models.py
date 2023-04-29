from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class STATUS(models.TextChoices):
    DRAFT = "0", _("Draft")
    PUBLISH = "1", _("Publish")
    ARCHIVE = "2", _("Archive")
#gettext_lazy: DRAFT를 사용하여 Django내에서 사용하는데 사용자에게는 "Draft"로 보여지고 data 저장은 "0"으로 된다.

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    #null=True는 null 허용,  blank=True는 form 에서 빈채로 저장되는 것을 허용

class Post(models.model):
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True) #unique=True는 값이 겹치지 않게 한다.
    slug = models.SlugField(max_length=200) #storing URL slugs in a relational database
    summary = models.CharField(max_length=200, nul=True, blank=True)
    content = models.TextField()
    status = models.Charield(max_length=1, choices=STATUS.choices, default=STATUS.DRAFT)
    image = models.ImageField(upload_to="post", default='post/sample.jpg')
    category = models.ManyToManyField(Category, related_name="posts")
    # related_name을 설정하면 category.post__set.all()로 특정 카테고리에 해당하는 post만 검색하던것을 category.posts.all() 형태로 사용가능하다.
    created_on = models.DateTimeField(auto_now_add=True)#insert시만 현재날짜로 갱신 아니면 null로 입력
    updated_on = models.DateTimeField(auto_now=True) #model이 save될때만다 현재 날짜로 갱신

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE) #related_name="comments"를 사용하면 query시 post.comments.all()처럼 사용가능
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    approved_comment = models.BolleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Like(models.Model):
    user = models.Foreignkey(User, related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)