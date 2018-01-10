# -*- coding: utf-8 -*-

from django.db.models import Count
from django.http import *
from django.shortcuts import render
from spider_model.models import *
import json
import jieba


def index(request):
    size = 50
    # 获取使用最多的前三个关键字
    key_count = KeywordWeb.objects.values('sk_id').annotate(count=Count('sk_id')).order_by('-count')[0:3]
    name = Keyword.objects.filter(id__in=[key['sk_id'] for key in key_count]).values('name')
    keyword = [key['name'] for key in name]
    #  取最新的50条新闻
    web = Web.objects.values('title', 'url').order_by('-add_time')[0:size]
    ret = {'web_list': list(web), 'keyword': ','.join(keyword), 'search': ''}
    return render(request, 'index.html', ret)


def search(request):
    size = 50
    request.encoding = 'utf-8'
    q = request.GET['q'].strip()
    key_count = KeywordWeb.objects.values('sk_id').annotate(count=Count('sk_id')).order_by('-count')[0:3]
    name = Keyword.objects.filter(id__in=[key['sk_id'] for key in key_count]).values('name')
    keyword = [key['name'] for key in name]
    if q == '':
        #  取最新的50条新闻
        web = Web.objects.values('title', 'url').order_by('-add_time')[0:size]
    else:
        seg_list = list(jieba.cut(q, cut_all=False))
        seg_list.append(q)
        name = Keyword.objects.filter(name__in=seg_list).values('id')
        key_id = [key['id'] for key in name]
        #  取最新的50条新闻
        web_id = KeywordWeb.objects.filter(sk_id__in=key_id).values('sw_id').order_by('-add_time')[0:size]
        web = Web.objects.values('title', 'url').filter(id__in=[k['sw_id'] for k in web_id])
    ret = {'web_list': list(web), 'keyword': ','.join(keyword), 'search': q}
    return render(request, 'index.html', ret)


def search_post(request):
    size = 50
    request.encoding = 'utf-8'
    q = request.POST['q'].strip()
    page = int(request.POST.get('p'))
    start = 0 if page <= 1 else (page - 1) * size
    end = start + size
    if q == '':
        #  取最新的50条新闻
        web = Web.objects.values('title', 'url').order_by('-add_time')[start:end]
    else:
        seg_list = list(jieba.cut(q, cut_all=False))
        seg_list.append(q)
        name = Keyword.objects.filter(name__in=seg_list).values('id')
        key_id = [key['id'] for key in name]
        #  取最新的50条新闻
        web_id = KeywordWeb.objects.filter(sk_id__in=key_id).values('sw_id').order_by('-add_time')[start:end]
        web = Web.objects.values('title', 'url').filter(id__in=[k['sw_id'] for k in web_id])
    ret = {'code': 200, 'msg': '', 'data': list(web)}
    return JsonResponse(ret)
