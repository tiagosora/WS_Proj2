from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class Wizard:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name', '')
        self.gender = kwargs.get('gender', '')
        self.species = kwargs.get('species', '')
        self.blood_type = kwargs.get('blood-type', '')
        self.eye_color = kwargs.get('eye_color', '')
        self.house = kwargs.get('house', '')
        self.wand = kwargs.get('wand', '')
        self.patronus = kwargs.get('patronus', '')
        self.skills = kwargs.get('skills', [])
        self.spells = kwargs.get('spells', [])
        self.type = kwargs.get('_type', 'wizard')

    def __str__(self):
        return f"Wizard: {self.name}"
    
    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'species': self.species,
            'blood_type': self.blood_type,
            'eye_color': self.eye_color,
            'wand': self.wand,
            'patronus': self.patronus
        }


class Skill:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name', '')
        self._type = kwargs.get('_type', 'skill')

    def __str__(self):
        return f"Skill: {self.name}"
    
    def info(self):         #TODO: pode dar erro no frontend
        return {
            'id': self.id,
            'name': self.name
        }
    

class Spell:
    def __init__(self, **kwargs):
        self.effect = kwargs.get('effect', '')
        self.id = kwargs.get('id', '')
        self.incantation = kwargs.get('incantation', '')
        self.light = kwargs.get('light', '')
        self.name = kwargs.get('name', '')
        self.type = kwargs.get('type', '')
        
    def __str__(self) -> str:
        return f"ID: {self.id}, \n\
                Effect: {self.effect}, \n\
                Incantation: {self.incantation}, \n\
                Light: {self.light}, \n\
                Name: {self.name}, \n \
                Type: {self.type}, \n \
                Hogwarts_type: {self.hogwarts_type}, \n " 
    
    def info(self):
        return {
            'id': self.id,
            'effect': self.effect,
            'incantation': self.incantation,
            'light': self.light,
            'name': self.name,
            'type': self.type,
        }
    
class Course:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', '')
        self.name = kwargs.get('name', '')
        self.professor = kwargs.get('professor', '')
        self.attending_year = kwargs.get('attending_year', '')
        self.teaches_spell = kwargs.get('teaches_spell', [])
        self._type = kwargs.get('_type', 'course')
        self.type = kwargs.get('type', '')
        
    def __str__(self) -> str:
        return f"ID: {self.id}, \n\
                Name: {self.name}, \n\
                Professor: {self.professor}, \n\
                Attending_year: {self.attending_year}, \n\
                Teaches_spell: {self.teaches_spell}, \n \
                Type: {self.type} \n "
                
    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'attending_year': self.attending_year,
            'type': self.type
        }
        
    def info_no_id(self):
        return {
            'name': self.name,
            'attending_year': self.attending_year,
            'type': self.type
        }


class Student:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.is_learning = kwargs.get('is_learning', [])
        self.learned = kwargs.get('learned', [])
        self.school = kwargs.get('school', '')
        self.school_year = kwargs.get('school_year', '')
        self.wizard = kwargs.get('wizard', '')
        self.type = kwargs.get('_type', 'student')
    
    def __str__(self) -> str:
        return f"ID: {self.id}, \n\
                Is Learning: {self.is_learning}, \n\
                Learned: {self.learned}, \n\
                School: {self.school}, \n\
                School Year: {self.school_year}, \n\
                Wizard: {self.wizard}, \n\
                Type: {self.type} \n"
            

class Professor:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.school = kwargs.get('school', '')
        self.wizard = kwargs.get('wizard', '')
        self.type = kwargs.get('_type', 'professor')
    
    def __str__(self) -> str:
        return f"ID: {self.id}, \n\
                School: {self.school}, \n\
                Wizard: {self.wizard}, \n\
                Type: {self.type} \n"

# Define a simple custom user class
class WizardAccount:
    def __init__(self, nmec, wizard_id):
        self.nmec = nmec
        self.wizard_id = wizard_id

    @property
    def is_authenticated(self):
        return True

