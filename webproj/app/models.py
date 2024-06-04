# Create your models here.
class Wizard:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', '')
        self.name = kwargs.get('hasName', '')
        self.gender = kwargs.get('hasGender', '')
        self.species = kwargs.get('hasSpecies', '')
        self.blood_type = kwargs.get('hasBloodType', '')
        self.eye_color = kwargs.get('hasEyeColor', '')
        self.house = kwargs.get('belongsToHouse', '')
        self.wand = kwargs.get('hasWand', '')
        self.patronus = kwargs.get('hasPatronus', '')
        self.skills = kwargs.get('skills', [])
        self.spells = kwargs.get('spells', [])
        self.type = kwargs.get('type', 'Wizard')

    def __str__(self):
        return f"Wizard: {self.name}, house: {self.house}"

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
        self.name = kwargs.get('hasSkillName', '')
        self._type = kwargs.get('type', 'Skill')

    def __str__(self):
        return f"Skill: {self.name}"

    def info(self):  #TODO: pode dar erro no frontend
        return {
            'id': self.id,
            'name': self.name
        }


class Spell:  #TODO: fix to match
    def __init__(self, **kwargs):
        self.effect = kwargs.get('hasEffect', '')
        self.id = kwargs.get('id', '')
        self.incantation = kwargs.get('hasIncantation', '')
        self.light = kwargs.get('hasLight', '')
        self.name = kwargs.get('hasName', '')
        self.type = kwargs.get('hasType', '')
        self._type = kwargs.get('type', 'Spell')

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
        self.name = kwargs.get('hasCourseName', '')
        self.professor = kwargs.get('hasProfessor', '')
        self.attending_year = kwargs.get('hasAttendingYear', '')
        self.teaches_spell = kwargs.get('teaches_spell', [])
        self.type = kwargs.get('hasCourseType', '')
        self._type = kwargs.get('_type', 'Course')

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
        self.id = kwargs.get('id', '')
        self.is_learning = kwargs.get('is_learning', [])
        self.learned = kwargs.get('learned', [])
        self.school = kwargs.get('belongsToSchool', '')
        self.school_year = kwargs.get('hasSchoolYear', '')
        self.wizard = kwargs.get('hasAccount', '')
        self.type = kwargs.get('type', ':Student')

    def __str__(self) -> str:
        return f"Is Learning: {self.is_learning}, \n\
                Learned: {self.learned}, \n\
                School: {self.school}, \n\
                School Year: {self.school_year}, \n\
                Wizard: {self.wizard}, \n\
                Type: {self.type} \n"


class Professor:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', '')
        self.school = kwargs.get('belongsToSchool', '')
        self.wizard = kwargs.get('hasAccount', '')
        self.type = kwargs.get('type', 'Professor')

    def __str__(self) -> str:
        return f"School: {self.school}, \n\
                Wizard: {self.wizard}, \n\
                Type: {self.type} \n"


class WizardAccount:
    def __init__(self, nmec, wizard_id):
        self.nmec = nmec
        self.wizard_id = wizard_id

    @property
    def is_authenticated(self):
        return True
