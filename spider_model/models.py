'''
# python3爬虫系统

# 关键字数据表
create table `spider_keyword`
(
    `sk_id` int(10) unsigned not null auto_increment comment '自增id',
    `sk_name` varchar(10) not null default '' comment '关键字名称',
    `sk_add_time` timestamp not null default current_timestamp comment '添加时间',
primary key (`sk_id`),
key `sk_name` (`sk_name`)
)engine=innodb default charset=utf8 comment '关键字数据表';

# 爬虫站点数据表
create table `spider_root`
(
    `sr_id` int(10) unsigned not null auto_increment comment '自增id',
    `sr_url` varchar(256) not null default '' comment '站点url',
    `sr_add_time` timestamp not null default current_timestamp comment '添加时间',
primary key (`sr_id`),
key `sr_url` (`sr_url`(20))
)engine=innodb default charset=utf8 comment '爬虫站点数据表';

# 爬虫网站数据表
create table `spider_web`
(
    `sw_id` int(10) unsigned not null auto_increment comment '自增id',
    `sw_sr_id` int(10) unsigned not null default '0' comment '站点id',
    `sw_title` varchar(256) not null default '' comment '网站标题',
    `sw_url` varchar(256) not null default '' comment '网站url',
    `sw_add_time` timestamp not null default current_timestamp comment '添加时间',
primary key (`sw_id`),
key `sw_sr_id` (`sw_sr_id`),
key `sw_url` (`sw_url`(20))
)engine=innodb default charset=utf8 comment '爬虫网站数据表';

# 关键字映射网站表
create table `spider_keyword_web`
(
    `skw_id` int(10) unsigned not null auto_increment comment '自增id',
    `skw_sk_id` int(10) unsigned not null default '0' comment '关键字id',
    `skw_sw_id` int(10) unsigned not null default '0' comment '网站id',
    `skw_add_time` timestamp not null default current_timestamp comment '添加时间',
primary key (`skw_id`),
key `keyword` (`skw_sk_id`, `skw_add_time`)
)engine=innodb default charset=utf8 comment '关键字映射网站表';
'''

from django.db import models


# Create your models here.
class Keyword(models.Model):
    class Meta:
        db_table = 'spider_keyword'
    id = models.IntegerField(db_column='sk_id', primary_key=True)
    name = models.CharField(db_column='sk_name', max_length=10)


class KeywordWeb(models.Model):
    class Meta:
        db_table = 'spider_keyword_web'
    id = models.IntegerField(db_column='skw_id', primary_key=True)
    sk_id = models.IntegerField(db_column='skw_sk_id')
    sw_id = models.IntegerField(db_column='skw_sw_id')
    add_time = models.DateTimeField(db_column='skw_add_time')


class Root(models.Model):
    class Meta:
        db_table = 'spider_root'
    id = models.IntegerField(db_column='sr_id', primary_key=True)
    url = models.CharField(db_column='sr_url', max_length=256)


class Web(models.Model):
    class Meta:
        db_table = 'spider_web'
    id = models.IntegerField(db_column='sw_id', primary_key=True)
    sr_id = models.IntegerField(db_column='sw_sr_id')
    title = models.CharField(db_column='sw_title', max_length=256)
    url = models.CharField(db_column='sw_url', max_length=256)
    add_time = models.DateTimeField(db_column='sw_add_time')
