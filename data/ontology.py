from owlready2 import *

# Create a new ontology
onto = get_ontology("http://hogwarts.edu/ontology.owl")

with onto:
    # Define classes
    class Account(Thing): pass
    class Wizard(Thing): pass
    class Student(Wizard): pass
    class BasicStudent(Student): pass
    class MediumStudent(Student): pass
    class AdvancedStudent(Student): pass
    class Professor(Wizard): pass
    class Headmaster(Wizard): pass
    class Spell(Thing): pass
    class Skill(Thing): pass
    class School(Thing): pass
    class House(Thing): pass
    class Course(Thing): pass

    # Define properties
    class hasMechanographicalNumber(DataProperty, FunctionalProperty):
        domain = [Account]
        range = [int]

    class hasPassword(DataProperty, FunctionalProperty):
        domain = [Account]
        range = [str]

    class hasWizard(DataProperty, FunctionalProperty):
        domain = [Account]
        range = [Wizard]
    class hasAccount(ObjectProperty, FunctionalProperty):
        domain = [Wizard]
        range = [Account]

    class hasName(DataProperty, FunctionalProperty):
        domain = [Wizard, Spell, Skill, School, House, Course]
        range = [str]

    class hasId(DataProperty, FunctionalProperty):
        domain = [Wizard, Spell, Skill, School, House, Course]

    class hasGender(DataProperty, FunctionalProperty):
        domain = [Wizard]
        range = [str]

    class hasSpecies(DataProperty, FunctionalProperty):
        domain = [Wizard]
        range = [str]

    class hasBloodType(DataProperty, FunctionalProperty):
        domain = [Wizard]
        range = [str]

    class hasEyeColor(DataProperty, FunctionalProperty):
        domain = [Wizard]
        range = [str]

    class belongsToHouse(ObjectProperty, FunctionalProperty):
        domain = [Wizard]
        range = [House]

    class hasWand(DataProperty, FunctionalProperty):
        domain = [Wizard]
        range = [str]

    class hasPatronus(DataProperty, FunctionalProperty):
        domain = [Wizard]
        range = [str]

    class hasSkill(ObjectProperty):
        domain = [Wizard]
        range = [Skill]

    class hasStudentId(DataProperty, FunctionalProperty):
        domain = [Student]
        range = [str]

    class belongsToSchool(ObjectProperty, FunctionalProperty):
        domain = [Student, Professor]
        range = [School]

    class hasSchoolYear(DataProperty, FunctionalProperty):
        domain = [Student]
        range = [int]

    class learnsCourse(ObjectProperty):
        domain = [Student]
        range = [Course]

    class hasLearnedCourse(ObjectProperty):
        domain = [Student]
        range = [Course]

    class teachesSpell(ObjectProperty):
        domain = [Course]
        range = [Spell]

    class hasProfessor(ObjectProperty, FunctionalProperty):
        domain = [Course]
        range = [Professor]

    class hasIncantation(DataProperty, FunctionalProperty):
        domain = [Spell]
        range = [str]

    class hasType(DataProperty, FunctionalProperty):
        domain = [Spell]
        range = [str]

    class hasEffect(DataProperty, FunctionalProperty):
        domain = [Spell]
        range = [str]

    class hasLight(DataProperty, FunctionalProperty):
        domain = [Spell]
        range = [str]

    class hasSkillName(DataProperty, FunctionalProperty):
        domain = [Skill]
        range = [str]



    class hasSchoolName(DataProperty, FunctionalProperty):
        domain = [School]
        range = [str]

    class hasLocation(DataProperty, FunctionalProperty):
        domain = [School, House]
        range = [str]

    class hasDateOfCreation(DataProperty, FunctionalProperty):
        domain = [School]
        range = [str]

    class hasHeadmaster(ObjectProperty, FunctionalProperty):
        domain = [School]
        range = [Headmaster]

    class hasHouseName(DataProperty, FunctionalProperty):
        domain = [House]
        range = [str]

    class hasSymbol(DataProperty, FunctionalProperty):
        domain = [House]
        range = [str]

    class hasFounder(DataProperty, FunctionalProperty):
        domain = [House]
        range = [int]

    class hasHouseProfessor(ObjectProperty, FunctionalProperty):
        domain = [House]
        range = [Professor]

    class hasStartDate(DataProperty, FunctionalProperty):
        domain = [Headmaster]
        range = [int]

    class hasCourseName(DataProperty, FunctionalProperty):
        domain = [Course]
        range = [str]

    class hasCourseType(DataProperty, FunctionalProperty):
        domain = [Course]
        range = [str]

    class hasAttendingYear(DataProperty, FunctionalProperty):
        domain = [Course]
        range = [int]

    class hasLevel(DataProperty):
        domain = [Student]
        range = [str]

# Save the ontology to a file
onto.save(file="ontology.owl", format="rdfxml")
