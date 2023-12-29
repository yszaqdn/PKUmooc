from rest_framework import serializers
from forum.models import Forum, ForumSection, Post, Reply
from user_info.serializers import UserDescSerializer


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['name']
        read_only_fields = ['name']


class ForumSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumSection
        fields = ['name']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'author', 'created_at']

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['content', 'author', 'created_at']





class ForumSerializer(serializers.ModelSerializer):
    """分类的序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='forum')



        
class ForumSectionSerializer(serializers.HyperlinkedModelSerializer):
    forum = ForumSerializer()



    author = UserDescSerializer(read_only=True)
    # category 的嵌套序列化字段
    category = CategorySerializer(read_only=True)
    # category 的 id 字段，用于创建/更新 category 外键
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    # category_id 字段的验证器
    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError("Category with id {} not exists.".format(value))
        return value


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'
        read_only_fields = ['created']



class ReplySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'
        read_only_fields = ['created']