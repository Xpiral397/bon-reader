from django import forms
from models import Novel, Chapaters


class NovelFrom(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ["user","image", "title",'language','genre', "length", "tags",'synopsis']

class ChapterForm(forms.ModelForm):
    class Meta:
        models = Chapaters
        fields = ['chapter', "title", "content", "un_saved_text", 'novel']