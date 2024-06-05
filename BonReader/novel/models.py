from django.db import models
from django.conf import settings

# Create your models here.




class Novel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    genre = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    chapters_count = models.IntegerField(default=0)
    read = models.CharField(default='0', max_length=10000)
    title = models.CharField(max_length=50)
    synopsis = models.CharField(max_length=10000)
    author = models.CharField(max_length=50)
    language = models.CharField(max_length=20)
    lending_gender = models.CharField(max_length=30)
    views = models.IntegerField(default=0)
    chapters = models.IntegerField(default=0)
    ratings = models.IntegerField(default=0)
    star = models.IntegerField(default=0)
    age_range = models.IntegerField(default=5)
    tags = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='catalog/books/coverimages/')
    
    def add_new_chapter(self, title, text, capter):
        self.chapters_count+=1
        
    def add_read_chapters(self, chapters):
        self.chapters +=f',${chapters}'
    
    def edit_synopsis(self, synopsis):
        self.synopsis = synopsis
        
    def add_view(self):
        self.views +=1
        
    def modify_title(self, new_title):
        self,title = new_title
    
class Chapter(models.Model):
    chapters = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=20000000)
    un_save_text = models.CharField(max_length=1000000)
    date_modified = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)


class Shelf(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    novels = models.ManyToManyField(Novel, through='ReadingActivity')

class ReadingActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    current_chapter = models.IntegerField(default=0)
    last_read = models.DateTimeField(auto_now=True)
    hours_spent = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)