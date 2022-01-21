from django.db import models

class SavedPost(models.Model):
    post_title = models.CharField(max_length=150)
    number_upvotes = models.IntegerField()
    number_comments = models.IntegerField()
    post_link = models.URLField(max_length=200)

    def __str__(self):
        return self.post_title

class TopLevelComment(models.Model):
    parent_post = models.ForeignKey(
        SavedPost, on_delete=models.CASCADE
    )
    contents = models.TextField()
    number_upvotes = models.IntegerField()
