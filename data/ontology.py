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
    class hasMechanographicalNumber(Account >> int): pass
    class hasAccount(Wizard >> Account): pass
    class hasName(Wizard >> str): pass
    class hasGender(Wizard >> str): pass
    class hasSpecies(Wizard >> str): pass
    class hasBloodType(Wizard >> str): pass
    class hasEyeColor(Wizard >> str): pass
    class belongsToHouse(Wizard >> House): pass
    class hasWand(Wizard >> str): pass
    class hasPatronus(Wizard >> str): pass
    class hasStudentId(Student >> str): pass
    class belongsToSchool(Student >> School): pass
    class hasSchoolYear(Student >> int): pass
    class learnsCourse(Student >> Course): pass
    class hasLearnedCourse(Student >> Course): pass
    class teachesSpell(Course >> Spell): pass
    class hasProfessor(Course >> Professor): pass
    class hasName(Spell >> str): pass
    class hasIncantation(Spell >> str): pass
    class hasType(Spell >> str): pass
    class hasEffect(Spell >> str): pass
    class hasLight(Spell >> str): pass
    class hasSkillName(Skill >> str): pass
    class hasSchoolName(School >> str): pass
    class hasLocation(School >> str): pass
    class hasDateOfCreation(School >> str): pass
    class hasHeadmaster(School >> Headmaster): pass
    class hasHouseName(House >> str): pass
    class hasSymbol(House >> str): pass
    class hasFounder(House >> int): pass
    class hasHouseLocation(House >> str): pass
    class hasHouseProfessor(House >> Professor): pass
    class hasStartDate(Headmaster >> int): pass
    class hasCourseName(Course >> str): pass
    class hasCourseType(Course >> str): pass
    class hasAttendingYear(Course >> int): pass


    # Define constraints
    hasMechanographicalNumber.domain = [Account]
    hasMechanographicalNumber.range = [int]
    hasMechanographicalNumber.only(int)
    hasMechanographicalNumber.some(int)
    hasMechanographicalNumber.exactly(1, int)

    hasAccount.domain = [Wizard]
    hasAccount.range = [Account]
    hasAccount.exactly(1, Account)

    hasName.domain = [Wizard, Spell, Skill, School, House, Course]
    hasName.range = [str]
    hasName.exactly(1, str)

    hasGender.domain = [Wizard]
    hasGender.range = [str]
    hasGender.exactly(1, str)

    hasSpecies.domain = [Wizard]
    hasSpecies.range = [str]
    hasSpecies.exactly(1, str)

    hasBloodType.domain = [Wizard]
    hasBloodType.range = [str]
    hasBloodType.exactly(1, str)

    hasEyeColor.domain = [Wizard]
    hasEyeColor.range = [str]
    hasEyeColor.exactly(1, str)

    belongsToHouse.domain = [Wizard]
    belongsToHouse.range = [House]
    belongsToHouse.exactly(1, House)

    hasWand.domain = [Wizard]
    hasWand.range = [str]
    hasWand.exactly(1, str)

    hasPatronus.domain = [Wizard]
    hasPatronus.range = [str]
    hasPatronus.exactly(1, str)

    hasStudentId.domain = [Student]
    hasStudentId.range = [str]
    hasStudentId.exactly(1, str)

    belongsToSchool.domain = [Student, Professor]
    belongsToSchool.range = [School]
    belongsToSchool.exactly(1, School)

    hasSchoolYear.domain = [Student]
    hasSchoolYear.range = [int]
    hasSchoolYear.exactly(1, int)

    learnsCourse.domain = [Student]
    learnsCourse.range = [Course]

    hasLearnedCourse.domain = [Student]
    hasLearnedCourse.range = [Course]

    teachesSpell.domain = [Course]
    teachesSpell.range = [Spell]

    hasProfessor.domain = [Course]
    hasProfessor.range = [Professor]
    hasProfessor.exactly(1, Professor)

    hasIncantation.domain = [Spell]
    hasIncantation.range = [str]
    hasIncantation.exactly(1, str)

    hasType.domain = [Spell]
    hasType.range = [str]
    hasType.exactly(1, str)

    hasEffect.domain = [Spell]
    hasEffect.range = [str]
    hasEffect.exactly(1, str)

    hasLight.domain = [Spell]
    hasLight.range = [str]
    hasLight.exactly(1, str)

    hasSkillName.domain = [Skill]
    hasSkillName.range = [str]
    hasSkillName.exactly(1, str)

    hasSchoolName.domain = [School]
    hasSchoolName.range = [str]
    hasSchoolName.exactly(1, str)

    hasLocation.domain = [School, House]
    hasLocation.range = [str]
    hasLocation.exactly(1, str)

    hasDateOfCreation.domain = [School]
    hasDateOfCreation.range = [str]
    hasDateOfCreation.exactly(1, str)

    hasHeadmaster.domain = [School]
    hasHeadmaster.range = [Headmaster]
    hasHeadmaster.exactly(1, Headmaster)

    hasHouseName.domain = [House]
    hasHouseName.range = [str]
    hasHouseName.exactly(1, str)

    hasSymbol.domain = [House]
    hasSymbol.range = [str]
    hasSymbol.exactly(1, str)

    hasFounder.domain = [House]
    hasFounder.range = [int]
    hasFounder.exactly(1, int)

    hasHouseProfessor.domain = [House]
    hasHouseProfessor.range = [Professor]
    hasHouseProfessor.exactly(1, Professor)

    hasStartDate.domain = [Headmaster]
    hasStartDate.range = [int]
    hasStartDate.exactly(1, int)

    hasCourseName.domain = [Course]
    hasCourseName.range = [str]
    hasCourseName.exactly(1, str)

    hasCourseType.domain = [Course]
    hasCourseType.range = [str]
    hasCourseType.exactly(1, str)

    hasAttendingYear.domain = [Course]
    hasAttendingYear.range = [int]
    hasAttendingYear.exactly(1, int)

# Save the ontology to a file
onto.save(file="ontology.owl", format="rdfxml")
