from comment.serializers import CommentSerializer
from rest_framework import serializers
from article.models import Article, Avatar
from user_info.serializers import UserDescSerializer
from article.models import topic
from article.models import Tag

class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'

# 新增的序列化器
class TagSerializer(serializers.HyperlinkedModelSerializer):
    """标签序列化器"""

    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'
class topicSerializer(serializers.ModelSerializer):
    """分类的序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='topic-detail')

    class Meta:
        model = topic
        fields = '__all__'
        read_only_fields = ['created']

class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)

    """博文序列化器"""
    author = UserDescSerializer(read_only=True)
    
    # topic 的嵌套序列化字段
    topic = topicSerializer(read_only=True)

    # topic 的 id 字段，用于创建/更新 topic 外键
    topic_id = serializers.IntegerField(
        write_only=True,
        allow_null=True,
        required=False
        )

    # tag 字段
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )

    # 图片字段
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(
        write_only=True, 
        allow_null=True, 
        required=False
    )

    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_topic_id': 'topic with id {value} not exists.',
        'default': 'No more message here..'
    }

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'

        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(
            model=Avatar,
            value=value,
            message='incorrect_avatar_id'
        )

        return value

    def validate_topic_id(self, value):
        self.check_obj_exists_or_fail(
            model=topic,
            value=value,
            message='incorrect_topic_id'
        )

        return value
 
    # 覆写方法，如果输入的标签不存在则创建它
    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)

        return super().to_internal_value(data)
    


# 将父类改为 ArticleBaseSerializer
class ArticleSerializer(ArticleBaseSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body': {'write_only': True}}

# 注意继承的父类是 ArticleBaseSerializer
class ArticleDetailSerializer(ArticleBaseSerializer):
    # 渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()

    id = serializers.IntegerField(read_only=True)
    
    comments = CommentSerializer(many=True, read_only=True)

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'

class ArticletopicDetailSerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
        ]


class topicDetailSerializer(serializers.ModelSerializer):
    """分类详情"""
    articles = ArticletopicDetailSerializer(many=True, read_only=True)

    class Meta:
        model = topic
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]