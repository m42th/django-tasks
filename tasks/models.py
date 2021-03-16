from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
class Task(models.Model):

    STATUS = (('doing', 'doing'), ('done', 'done'),)
    title = models.CharField(max_length=255)
    description = models.TextField()
    done = models.CharField(max_length=5,choices=STATUS)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) #models.CASDADE deleta todos os dados quando o usuário deleta a conta
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title