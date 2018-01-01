# -*- coding:utf-8 -*-

from django.db import models


class Author(models.Model):
    """
    博客作者模型
    """
    name = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.TextField()

    def __unicode__(self):
        return u'%s' % (self.name)

# what ??
class BlogManager(models.Model):
    """
        docstring for BlogManager

    """
    def title_count(self,keyword):
        return self.filter(caption__icontains=keyword).count()

    def tag_count(self,keyword):
        return self.filter(tags__icontains=keyword).count()

    def author_count(self,keyword):
        return self.filter(author__icontains=keyword).count()


class Tag(models.Model):
    """
    博客分类
    """
    tag_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    """
    若需要通过tag获取有哪些博文，这种多对多字段需要用tag.blog_set.all()这种方式。另外外键字段筛选也是如此。
    """

    def __unicode__(self):
        return u'%s' % (self.tag_name)

class Blog(models.Model):
    """
    博客
    """
    caption = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)  #日期，新增自动
    update_time = models.DateTimeField(auto_now=True)   #日期，修改自动更新
    #recommend = models.BooleanField(default=False)  #布尔字段，我用于标记是否是推荐博文

    # new object
    objects = models.Manager()
    count_objects = BlogManager()
    taglist = []

    def save(self,*args,**kwargs):
        super(Blog, self).save()
        for i in self.taglist:
            p, created = Tag.objects.get_or_create(tag_name=i)
            self.tags.add(p)

    def __unicode__(self):
        return u'%s %s %s' % (self.caption,self.author,self.publish_time)

    # 它用于定义一些Django模型类的行为特性
    class Meta:
        # 排序
        ordering = ['-publish_time']


class Weibo(models.Model):
    message = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    publish_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.message