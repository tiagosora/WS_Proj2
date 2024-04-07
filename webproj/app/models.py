from django.db import models


# Create your models here.
class Wizard:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.gender = kwargs.get('gender')
        self.species = kwargs.get('species')
        self.blood_type = kwargs.get('blood_type')
        self.eye_color = kwargs.get('eye_color')
        self.house = kwargs.get('house')
        self.wand = kwargs.get('wand')
        self.patronus = kwargs.get('patronus')
        self.skills = kwargs.get('skills', [])
        self.spells = kwargs.get('spells', [])

    def __str__(self):
        return f"Wizard: {self.name}"


class Skill:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Skill: {self.name}"