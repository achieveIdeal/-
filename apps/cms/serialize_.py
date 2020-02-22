from rest_framework import serializers
from news.models import Banner
class BannaerSerial(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id','priority','image_url','news_id']