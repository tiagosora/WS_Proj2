from django.db import models


# Create your models here.
class Wizard(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    house = models.ForeignKey('House', on_delete=models.SET_NULL, null=True)
    # Assuming there are references to spells and skills in the RDF
    spells = models.ManyToManyField('Spell')
    skills = models.ManyToManyField('Skill')

    def __str__(self):
        return self.name


class Spell(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=100)
    effect = models.TextField()

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField(max_length=255)
    founder = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Professor(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    # Link to the house they belong to or oversee
    house = models.ForeignKey('House', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.name
