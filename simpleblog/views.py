#!/usr/bin/python
# -*- coding:utf -*-

from django.shortcuts import render_to_response, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.context_processors import csrf    # 手工导入并使用处理器来生成CSRF token
from models import Tag
from models import Author
from models import Blog
from models import Weibo
from forms import BlogForm
from forms import TagForm


def blog_list(request):
    blogs = Blog.objects.order_by('-id')
    tags = Tag.objects.all()
    weibos = Weibo.objects.order_by('-publish_time')[:5]
    return render(request, "simpleblog/blog_list.html", {"blogs": blogs,"tags": tags,"weibos": weibos})


def blog_filter(request, id=''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()
    return render(request, "simpleblog/blog_filter.html", {"blogs": blogs, "tag": tag, "tags": tags})


def blog_search(request):
    tags = Tag.objects.all()
    if "search" in request.GET:
        search = request.GET['search']
        blogs = Blog.objects.filter(caption__icontains=search)  #caption__icontains 类似like
        return render(request, 'simpleblog/blog_filter.html', {"blogs": blogs, "tags": tags})
    else:
        blogs = Blog.objects.order_by('-id')
        return render(request, "simpleblog/blog_list.html", {"blogs": blogs, "tags": tags})


def blog_show(request,id=''):
    try:
        blog = Blog.objects.get(id=id)
        tags = Tag.objects.all()
    except Blog.DoesNotExist:
        raise Http404
    return render(request, "simpleblog/blog_show.html", {"blog": blog, "tags": tags})


def blog_show_comment(request,id=''):
    blog = Blog.objects.get(id=id)
    return render(request, 'simpleblog/blog_comments_show.html', {"blog": blog})



def blog_del(request, id=''):
    try:
        blog = Blog.objects.get(id=id)
    except Exception:
        raise Http404
    if blog:
        blog.delete()
        return HttpResponseRedirect("/simpleblog/bloglist/")
    blogs = Blog.objects.all()
    return render(request, "simpleblog/blog_list.html",{"blogs": blogs})


def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)       # request.POST：将接收到的数据通过BlogForm验证
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():      # 验证请求的内容和Form里面的是否验证通过。通过是True，否则False。
            cd = form.cleaned_data                  # cleaned_data类型是字典，里面是提交成功后的信息
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            for taglist in tagname.split():
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            author = Author.objects.get(id=1)
            content = cd['content']
            blog = Blog(caption=title, author=author, content=content)
            blog.save()
            for taglist in tagname.split():
                blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                blog.save()
            id = Blog.objects.order_by('-id')[0].id
            return HttpResponseRedirect('/simpleblog/blog/%s' % id)
    else:
        form = BlogForm()
        tag = TagForm()
        return render(request, 'simpleblog/blog_add.html', {'form': form, 'tag': tag})


def show_weibo(request):
    weibos = Weibo.objects.order_by('-publish_time')[:6]
    return render(request, 'simpleblog/blog_twitter.html',{"weibos": weibos})


def add_weibo(request):
    # c = {}
    # c.update(csrf(request))     # 手工导入并使用处理器来生成CSRF token; django1.8之后，调用render便可以自动将csrf_token添加至上下文中
    if request.method == 'POST':
        message = request.POST['twitter']
        author = Author.objects.get(id=1)
        message = Weibo(message=message,author=author)
        message.save()
        weibos = Weibo.objects.order_by('-publish_time')[:5]
        return render(request, "simpleblog/blog_twitter.html", {"weibos": weibos})
    else:
        return HttpResponse("add weibo by get")


def blog_update(request, id=""):
    id = id
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            tagnamelist = tagname.split()
            for taglist in tagnamelist:
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            content = cd['content']
            blog = Blog.objects.get(id=id)
            if blog:
                blog.caption = title
                blog.content = content
                blog.save()
                for taglist in tagnamelist:
                    blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                    blog.save()
                tags = blog.tags.all()
                for tagname in tags:
                    tagname = unicode(str(tagname), "utf-8")
                    if tagname not in tagnamelist:
                        notag = blog.tags.get(tag_name=tagname)
                        blog.tags.remove(notag)
            else:
                blog = Blog(caption=blog.caption, content=blog.content)
                blog.save()
            return HttpResponseRedirect('/simpleblog/blog/%s' % id)
    else:
        try:
            blog = Blog.objects.get(id=id)
        except Exception:
            raise Http404
        form = BlogForm(initial={'caption': blog.caption, 'content': blog.content}, auto_id=False)  #initial 初始化
        tags = blog.tags.all()
        if tags:
            taginit = ''
            for x in tags:
                taginit += str(x) + ' '
            tag = TagForm(initial={'tag_name': taginit})
        else:
            tag = TagForm()
        return render(request, "simpleblog/blog_add.html", {'blog': blog, 'form': form, 'id': id, 'tag': tag})