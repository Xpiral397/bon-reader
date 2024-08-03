from django.db import models
from django.conf import settings

# Create your models here.

class Chapter(models.Model):
    chapter = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, max_length=20000000)
    unsaved_text = models.TextField(null=True, max_length=1000000)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    novel = models.ForeignKey('Novel', on_delete=models.CASCADE)

    class Meta:
        ordering = ["chapter"]
        unique_together = ("chapter", "novel")

class UsersReder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chapter = models.IntegerField(default=0)

class Novel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    chapters_count = models.IntegerField(default=0)
    read = models.CharField(default=0, max_length=10000)
    users_reades = models.ManyToManyField(UsersReder, related_name="read_users")
    title = models.CharField(max_length=50)
    synopsis = models.CharField(max_length=10000)
    author = models.CharField(max_length=50)
    length = models.IntegerField(default=0)
    language = models.CharField(max_length=20)
    leading_gender = models.CharField(max_length=30)
    views = models.IntegerField(default=0)
    chapters = models.ManyToManyField(Chapter, related_name="chapters_table")
    ratings = models.IntegerField(default=0)
    star = models.IntegerField(default=0)
    age_range = models.IntegerField(default=5)
    tags = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="cover/", null=True, blank=True)

    def add_new_chapter(self, title):
        print(title, self.chapters_count)
        self.chapters_count += 1
        chapter = Chapter.objects.create(
            title=title,
            chapter=self.chapters_count,
            novel=self,  # Ensure that the chapter is linked to the novel
        )
        self.chapters.add(chapter)
        self.save()

    def add_readers(self, chapters, user):
        user_reader = UsersReder.objects.create(chapter=chapters, user=user)
        user_reader.save()

    def isCompleted(self):
        self.completed = True
        self.save()

    def setIsNotCompleted(self):
        self.completed = False
        self.save()

    def get_number_of_reader(self, id):
        return UsersReder.objects.filter(id=id).all().count()

    def edit_chapters(self, chapters, content, title):
        current = self.chapters.get(chapter=chapters)
        current.content = content
        current.title = title
        current.save()

    def edit_synopsis(self, synopsis):
        self.synopsis = synopsis
        self.save()

    def add_view(self):
        self.views += 1
        self.save()

    def modify_title(self, new_title):
        self.title = new_title
        self.save()

class Shelf(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    novels = models.ManyToManyField(Novel, through="ReadingActivity")

class ReadingActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    current_chapter = models.IntegerField(default=0)
    last_read = models.DateTimeField(auto_now=True)
    hours_spent = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
