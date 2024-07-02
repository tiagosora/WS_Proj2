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
        self.educatedAt = kwargs.get('educatedAt', '')
        self.residentOf = kwargs.get('residentOf', '')
        self.workLocation = kwargs.get('workLocation', '')
        self.wears = kwargs.get('wears', '')
        self.memberOf = kwargs.get('memberOf', '')
        self.relative = kwargs.get('relative', '')
        self.citizenship = kwargs.get('citizenship', '')
        self.image = kwargs.get('image', '')
        self.birthDate = kwargs.get('birthDate', '')
        self.birthPlace = kwargs.get('birthPlace', '')
        self.occupation = kwargs.get('occupation', '')
        self.title = kwargs.get('title', '')
        self.children = kwargs.get('children', '')
        self.father = kwargs.get('father', '')
        self.mother = kwargs.get('mother', '')
        self.spouse = kwargs.get('spouse', '')
        self.sibling = kwargs.get('sibling', '')
        self.deathDate = kwargs.get('deathDate', '')

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
            'patronus': self.patronus,
            'house': self.house,
            'educatedAt': self.educatedAt,
            'residentOf': self.residentOf,
            'workLocation': self.workLocation,
            'wears': self.wears,
            'memberOf': self.memberOf,
            'relative': self.relative,
            'citizenship': self.citizenship,
            'image': self.image,
            'birthDate': self.birthDate,
            'birthPlace': self.birthPlace,
            'occupation': self.occupation,
            'title': self.title,
            'children': self.children,
            'father': self.father,
            'mother': self.mother,
            'spouse': self.spouse,
            'sibling': self.sibling,
            'deathDate': self.deathDate
        }


class Skill:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('hasSkillName', '')
        self._type = kwargs.get('type', 'Skill')

    def __str__(self):
        return f"ID: {self.id}, \
            Name: {self.name}, \
            Type: {self._type}"

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
        self.partOf = kwargs.get('partOf', '')
        self.hasUse = kwargs.get('hasUse', '')
        self.causeOf = kwargs.get('causeOf', '')

    def __str__(self) -> str:
        return f"ID: {self.id}, \n\
            Effect: {self.effect}, \n\
            Incantation: {self.incantation}, \n\
            Light: {self.light}, \n\
            Name: {self.name}, \n \
            Type: {self.type}, \n \
            _type: {self._type}, \n \
            partOf: {self.partOf}, \n \
            hasUse: {self.hasUse}, \n \
            causeOf: {self.causeOf} \n"

    def info(self):
        return {
            'id': self.id,
            'effect': self.effect,
            'incantation': self.incantation,
            'light': self.light,
            'name': self.name,
            'type': self.type,
            '_type': self._type,
            'partOf': self.partOf,
            'hasUse': self.hasUse,
            'causeOf': self.causeOf
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
        self.participatedBy = kwargs.get('participatedBy', '')
        self.isTheStudyOf = kwargs.get('isTheStudyOf', '')
        
    def __str__(self) -> str:
        return f"ID: {self.id}, \n\
                Name: {self.name}, \n\
                Professor: {self.professor}, \n\
                Attending_year: {self.attending_year}, \n\
                Teaches_spell: {self.teaches_spell}, \n \
                Type: {self.type} \n \
                _type: {self._type} \n \
                participatedBy: {self.participatedBy} \n \
                isTheStudyOf: {self.isTheStudyOf} \n"

    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'attending_year': self.attending_year,
            'type': self.type,
            'professor': self.professor,
            'teaches_spell': self.teaches_spell,
            'participatedBy': self.participatedBy,
            'isTheStudyOf': self.isTheStudyOf,
            
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
        self.points = kwargs.get('hasPoints', '')
        self.star = kwargs.get('hasStarRating', 1)

    def __str__(self) -> str:
        return f"Is Learning: {self.is_learning}, \n\
                Learned: {self.learned}, \n\
                School: {self.school}, \n\
                School Year: {self.school_year}, \n\
                Wizard: {self.wizard}, \n\
                Type: {self.type} \n\
                Point: {self.points} \n"


class Professor:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', '')
        self.school = kwargs.get('teachesAtSchool', '')
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


class House:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', '')
        self.name = kwargs.get('hasHouseName', '')
        self.professor = kwargs.get('hasHouseProfessor', '')
        self.location = kwargs.get('hasLocation', '')
        self.symbol = kwargs.get('hasSymbol', '')
        self.type = kwargs.get('type', ':House')
        self.totalPoints = kwargs.get('hasTotalPoints', '')
        self.partOf = kwargs.get('partOf', '')
        self.namedAfter = kwargs.get('namedAfter', '')
        self.foundedBy = kwargs.get('foundedBy', '')
        self.coatOfArms = kwargs.get('coatOfArms', '')
        self.officialColor = kwargs.get('officialColor', '')
        self.hasParts = kwargs.get('hasParts', '')
        
    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'professor': self.professor,
            'location': self.location,
            'symbol': self.symbol,
            'totalPoints': self.totalPoints,
            'type': self.type,
            'totalPoints': self.totalPoints,
            'partOf': self.partOf,
            'namedAfter': self.namedAfter,
            'foundedBy': self.foundedBy,
            'coatOfArms': self.coatOfArms,
            'officialColor': self.officialColor,
            'hasParts': self.hasParts
        }
    