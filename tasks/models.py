from django.db import models

# Create your models here.
class Task(models.Model):

    STATUS = (('Doing', 'Doing'), ('Done', 'Done'),)
    title = models.CharField(max_length=255)
    description = models.TextField()
    done = models.CharField(max_length=5,choices=STATUS)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title