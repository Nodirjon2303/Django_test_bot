from django.db import models

class Profile(models.Model):
    username = models.CharField(null=True, max_length=35)
    telegram_id = models.IntegerField(null=True, default=0)
    full_name = models.CharField(null=True, blank=True, max_length=150)
    status = models.CharField(max_length=19, default='user')

    def __str__(self):
        return self.full_name

class Test(models.Model):
    question = models.CharField(max_length=255, null=True)
    right = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    test = models.ForeignKey(null=True  ,to=Test, on_delete=models.CASCADE)
    var = models.CharField(max_length=120, null=True, blank=True)


    def __str__(self):
        return self.var

class Testing(models.Model):
    test = models.FileField(upload_to='test')