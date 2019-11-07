from django.db import models


class Planet(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Sith(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recruit(models.Model):
    name = models.CharField(max_length=20)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    age = models.IntegerField(default=18, blank=False, null=False)
    email = models.EmailField(default='mdylll@mail.ru', max_length=50, primary_key=True)
    sith = models.ForeignKey(Sith, null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShadowHand(models.Model):
    order = 'order'
    recruit = models.ForeignKey(Recruit, null=True, blank=True, on_delete=models.CASCADE)
    question = models.CharField(max_length=30)
    answer = models.CharField(default=None, max_length=30)

    def __str__(self):
        return str(self.question) + ' ' + str(self.recruit)
