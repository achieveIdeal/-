from rest_framework import serializers
from news.models import *


class BannerSerialize(serializers.ModelSerializer):
    '''轮播图序列化'''
    news_id = serializers.IntegerField(source='news.id')
    news_title = serializers.CharField(source='news.title')
    class Meta:
        model = Banner
        fields = ['image_url','priority','news_id','news_title']


class NewsSerialize(serializers.ModelSerializer):
    '''新闻序列化'''
    author = serializers.CharField(source='author.username')
    create_time = serializers.SerializerMethodField()
    tag = serializers.CharField(source='tag.name')
    content = serializers.CharField()

    def get_create_time(self,news):
        create_time = news.create_time
        return create_time


    class Meta:
        model = News
        exclude = ['is_delete','update_time']

class TagSerialize(serializers.Serializer):
    '''新闻分类序列化'''
    name = serializers.CharField()
    id = serializers.IntegerField(source='pk')

class CommentSerialize(serializers.Serializer):
    author_name = serializers.CharField(source='author.username')
    content = serializers.CharField()
    create_time = serializers.CharField()

class HotNewsSerialize(serializers.Serializer):
    news_title = serializers.CharField(source='news.title')
    news_image_url = serializers.CharField(source='news.image_url')
    news_id = serializers.IntegerField(source='news.id')