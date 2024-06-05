from rest_framework import serializers
from .models import Novel, Chapter

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'novel', 'title', 'content', 'unsaved_text', 'date_modified', 'date_created']

class NovelSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Novel
        fields = ['id', 'user', 'title', 'synopsis', 'author', 'language', 'lending_gender', 'views', 'ratings', 'star', 'age_range', 'tags', 'image', 'chapters_count', 'read', 'chapters']

from rest_framework import serializers
from .models import Novel, Chapter

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'novel', 'title', 'content', 'unsaved_text', 'date_modified', 'date_created']

class NovelRankingSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Novel
        fields = [
            'id', 'user', 'title', 'synopsis', 'author', 'language', 'lending_gender', 
            'views', 'ratings', 'star', 'age_range', 'tags', 'image', 'chapters_count', 
            'read', 'chapters'
        ]
from rest_framework import serializers
from .models import Shelf, ReadingActivity, Novel


class ReadingActivitySerializer(serializers.ModelSerializer):
    novel = NovelSerializer()

    class Meta:
        model = ReadingActivity
        fields = '__all__'

class ShelfSerializer(serializers.ModelSerializer):
    novels = ReadingActivitySerializer(source='readingactivity_set', many=True)

    class Meta:
        model = Shelf
        fields = '__all__'
