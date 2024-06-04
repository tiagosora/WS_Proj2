from owlready2 import get_ontology
from rdflib import Graph, Namespace, Literal

# Load the ontology
onto = get_ontology("ontology.owl").load()

# Define the namespace for the ontology
HOGWARTS = Namespace("http://hogwarts.edu/ontology#")

# Load RDF data
rdf_data_graph = Graph()
rdf_data_graph.parse('data_.rdf', format='xml')


def extract_id_bar(iri):
    return iri.split("/")[-1]

def extract_id_under(iri):
    return iri.split("_")[-1]

# Create instances for each type based on RDF data
def create_instances():
    # Create Skill instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("skill")):
        skill_id = rdf_data_graph.value(s, HOGWARTS.id)
        skill_name = rdf_data_graph.value(s, HOGWARTS.name)

        # Create a new Skill instance in the ontology
        new_skill = onto.Skill(f"Skill_{skill_id}")
        new_skill.hasSkillName = str(skill_name)

        print(f"Created Skill: {new_skill}")

    # Create Spell instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("spell")):
        spell_id = rdf_data_graph.value(s, HOGWARTS.id)
        spell_name = rdf_data_graph.value(s, HOGWARTS.name)
        spell_incantation = rdf_data_graph.value(s, HOGWARTS.incantation)
        spell_type = rdf_data_graph.value(s, HOGWARTS.type)
        spell_effect = rdf_data_graph.value(s, HOGWARTS.effect)
        spell_light = rdf_data_graph.value(s, HOGWARTS.light)

        # Create a new Spell instance in the ontology
        new_spell = onto.Spell(f"Spell_{spell_id}")
        new_spell.hasName = str(spell_name)
        new_spell.hasIncantation = str(spell_incantation)
        new_spell.hasType = str(spell_type)
        new_spell.hasEffect = str(spell_effect)
        new_spell.hasLight = str(spell_light)

        print(f"Created Spell: {new_spell}")

    # Create House instances without linking professors
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("house")):
        house_id = rdf_data_graph.value(s, HOGWARTS.id)
        house_name = rdf_data_graph.value(s, HOGWARTS.name)
        house_symbol = rdf_data_graph.value(s, HOGWARTS.symbol)
        house_location = rdf_data_graph.value(s, HOGWARTS.location)

        # Create a new House instance in the ontology
        new_house = onto.House(f"House_{house_id}")
        new_house.hasHouseName = str(house_name)
        new_house.hasSymbol = str(house_symbol)
        new_house.hasLocation = str(house_location)

        print(f"Created House: {new_house}")

    # Create Wizard instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("wizard")):
        wizard_id = rdf_data_graph.value(s, HOGWARTS.id)
        wizard_name = rdf_data_graph.value(s, HOGWARTS.name)
        wizard_gender = rdf_data_graph.value(s, HOGWARTS.gender)
        wizard_species = rdf_data_graph.value(s, HOGWARTS.species)
        wizard_blood_type = rdf_data_graph.value(s, HOGWARTS.blood_type)
        wizard_eye_color = rdf_data_graph.value(s, HOGWARTS.eye_color)
        wizard_house = rdf_data_graph.value(s, HOGWARTS.house)
        wizard_wand = rdf_data_graph.value(s, HOGWARTS.wand)
        wizard_patronus = rdf_data_graph.value(s, HOGWARTS.patronus)
        wizard_skills = rdf_data_graph.objects(s, HOGWARTS.has_skill)

        # Create a new Wizard instance in the ontology
        new_wizard = onto.Wizard(f"Wizard_{wizard_id}")
        new_wizard.hasName = str(wizard_name)
        new_wizard.hasGender = str(wizard_gender)
        new_wizard.hasSpecies = str(wizard_species)
        new_wizard.hasBloodType = str(wizard_blood_type)
        new_wizard.hasEyeColor = str(wizard_eye_color)
        new_wizard.hasWand = str(wizard_wand)
        new_wizard.hasPatronus = str(wizard_patronus)

        # Link the house to the wizard
        house_iri = f"http://hogwarts.edu/ontology.owl#House_{wizard_house}"
        for house_instance in onto.House.instances():
            if house_instance.iri == house_iri:
                new_wizard.belongsToHouse = house_instance
                break

        new_wizard.hasSkill = []

        for skill_iri in wizard_skills:
            for skill_instance in onto.Skill.instances():
                if skill_instance.iri[-2] == "_" and str(skill_iri)[-2] == "/":
                    if skill_instance.iri[-1] == str(skill_iri)[-1]:
                        new_wizard.hasSkill.append(skill_instance)
                if skill_instance.iri[-2:] == str(skill_iri)[-2:]:
                    new_wizard.hasSkill.append(skill_instance)

        print(f"Created Wizard: {new_wizard}")

    # Create Account instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("account")):
        account_id = rdf_data_graph.value(s, HOGWARTS.id)
        account_number = rdf_data_graph.value(s, HOGWARTS.number)
        account_password = rdf_data_graph.value(s, HOGWARTS.password)
        account_wizard = rdf_data_graph.value(s, HOGWARTS.wizard)

        # Create a new Account instance in the ontology
        new_account = onto.Account(f"Account_{account_id}")
        new_account.hasMechanographicalNumber = int(account_number)
        new_account.hasPassword = str(account_password)


        # Link the wizard to the account
        wizard_iri = str(account_wizard)
        for wizard_instance in onto.Wizard.instances():
            if wizard_instance.iri[-2] == "_" and str(wizard_iri)[-2] == "/":
                if wizard_instance.iri[-1] == str(wizard_iri)[-1]:
                    new_account.hasAccount = wizard_instance
                    break
            if wizard_instance.iri[-2:] == str(wizard_iri)[-2:]:
                new_account.hasAccount = wizard_instance
                break

        print(f"Created Account: {new_account}")

    # Create Headmaster instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("headmaster")):
        headmaster_id = rdf_data_graph.value(s, HOGWARTS.id)
        headmaster_wizard = rdf_data_graph.value(s, HOGWARTS.wizard)
        headmaster_start_date = rdf_data_graph.value(s, HOGWARTS.start_date)

        # Create a new Headmaster instance in the ontology
        new_headmaster = onto.Headmaster(f"Headmaster_{headmaster_id}")
        new_headmaster.hasStartDate = int(headmaster_start_date)

        # Link the wizard to the headmaster
        wizard_iri = str(headmaster_wizard)
        for wizard_instance in onto.Wizard.instances():
            if wizard_instance.iri[-2] == "_" and str(wizard_iri)[-2] == "/":
                if wizard_instance.iri[-1] == str(wizard_iri)[-1]:
                    new_headmaster.hasAccount = wizard_instance
                    break
            if wizard_instance.iri[-2:] == str(wizard_iri)[-2:]:
                new_headmaster.hasAccount = wizard_instance
                break

        print(f"Created Headmaster: {new_headmaster}")

    # Create School instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("school")):
        school_id = rdf_data_graph.value(s, HOGWARTS.id)
        school_name = rdf_data_graph.value(s, HOGWARTS.name)
        school_location = rdf_data_graph.value(s, HOGWARTS.location)
        school_date_of_creation = rdf_data_graph.value(s, HOGWARTS.dateOfCreation)
        school_headmaster = rdf_data_graph.value(s, HOGWARTS.headmaster)

        # Create a new School instance in the ontology
        new_school = onto.School(f"School_{school_id}")
        new_school.hasSchoolName = str(school_name)
        new_school.hasLocation = str(school_location)
        new_school.hasDateOfCreation = str(school_date_of_creation)

        # Link the headmaster to the school
        headmaster_iri = str(school_headmaster)
        for headmaster_instance in onto.Headmaster.instances():
            if headmaster_instance.hasAccount.iri[-2] == "_" and str(headmaster_iri)[-2] == "/":
                if headmaster_instance.hasAccount.iri[-1] == str(headmaster_iri)[-1]:
                    new_school.hasHeadmaster = headmaster_instance
                    break
            if headmaster_instance.hasAccount.iri[-2:] == str(headmaster_iri)[-2:]:
                new_school.hasHeadmaster = headmaster_instance
                break

        print(f"Created School: {new_school}")

    # Create Professor instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("professor")):
        professor_id = rdf_data_graph.value(s, HOGWARTS.id)
        professor_wizard = rdf_data_graph.value(s, HOGWARTS.wizard)
        professor_school = rdf_data_graph.value(s, HOGWARTS.school)

        # Create a new Professor instance in the ontology
        new_professor = onto.Professor(f"Professor_{professor_id}")

        # Link the wizard to the professor
        wizard_iri = str(professor_wizard)
        for wizard_instance in onto.Wizard.instances():
            if wizard_instance.iri[-2] == "_" and str(wizard_iri)[-2] == "/":
                if wizard_instance.iri[-1] == str(wizard_iri)[-1]:
                    new_professor.hasAccount = wizard_instance
                    break
            if wizard_instance.iri[-2:] == str(wizard_iri)[-2:]:
                new_professor.hasAccount = wizard_instance
                break

        # Link the school to the professor
        school_iri = str(professor_school)
        for school_instance in onto.School.instances():
            if school_instance.iri[-2] == "_" and str(school_iri)[-2] == "/":
                if school_instance.iri[-1] == str(school_iri)[-1]:
                    new_professor.belongsToSchool = school_instance
                    break
            if school_instance.iri[-2:] == str(school_iri)[-2:]:
                new_professor.belongsToSchool = school_instance
                break

        print(f"Created Professor: {new_professor}")

    # Update House instances to link professors
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("house")):
        house_professor_in_charge = rdf_data_graph.value(s, HOGWARTS.professorInCharge)
        house_founder = rdf_data_graph.value(s, HOGWARTS.founder)

        # Update the House instance in the ontology
        house_iri = str(s)
        professor_iri = str(house_professor_in_charge)
        for house_instance in onto.House.instances():
            if house_instance.iri[-2] == "_" and str(house_iri)[-2] == "/":
                if house_instance.iri[-1] == str(house_iri)[-1]:
                    for professor_instance in onto.Professor.instances():
                        if professor_instance.iri[-2] == "_" and str(professor_iri)[-2] == "/":
                            if professor_instance.iri[-1] == str(professor_iri)[-1]:
                                house_instance.hasHouseProfessor = professor_instance
                                break
                        if professor_instance.iri[-2:] == str(professor_iri)[-2:]:
                            house_instance.hasHouseProfessor = professor_instance
                            break
            if house_instance.iri[-2:] == str(house_iri)[-2:]:
                for professor_instance in onto.Professor.instances():
                    if professor_instance.iri[-2] == "_" and str(professor_iri)[-2] == "/":
                        if professor_instance.iri[-1] == str(professor_iri)[-1]:
                            house_instance.hasHouseProfessor = professor_instance
                            break
                    if professor_instance.iri[-2:] == str(professor_iri)[-2:]:
                        house_instance.hasHouseProfessor = professor_instance
                        break

                print(f"Updated House: {house_instance}")

    # Create Course instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("course")):
        course_id = rdf_data_graph.value(s, HOGWARTS.id)
        course_name = rdf_data_graph.value(s, HOGWARTS.name)
        course_type = rdf_data_graph.value(s, HOGWARTS.type)
        course_attending_year = rdf_data_graph.value(s, HOGWARTS.attending_year)
        course_professor = rdf_data_graph.value(s, HOGWARTS.professor)
        course_teaches_spell = rdf_data_graph.objects(s, HOGWARTS.teaches_spell)

        # Create a new Course instance in the ontology
        new_course = onto.Course(f"Course_{course_id}")
        new_course.hasCourseName = str(course_name)
        new_course.hasCourseType = str(course_type)
        new_course.hasAttendingYear = int(course_attending_year)

        # Link the professor to the course
        professor_iri = str(course_professor)
        for professor_instance in onto.Professor.instances():
            if professor_instance.iri[-2] == "_" and str(professor_iri)[-2] == "/":
                if professor_instance.iri[-1] == str(professor_iri)[-1]:
                    new_course.hasProfessor = professor_instance
                    break
            if professor_instance.iri[-2:] == str(professor_iri)[-2:]:
                new_course.hasProfessor = professor_instance
                break

        new_course.teachesSpell = []

        # Link the spells to the course
        for spell_iri in course_teaches_spell:
            for spell_instance in onto.Spell.instances():
                if extract_id_under(spell_instance.iri) == extract_id_bar(str(spell_iri)):
                    new_course.teachesSpell.append(spell_instance)
                    break
        print(f"Created Course: {new_course}")

    # Create Student instances
    for s in rdf_data_graph.subjects(HOGWARTS._type, Literal("student")):
        student_id = rdf_data_graph.value(s, HOGWARTS.id)
        student_wizard = rdf_data_graph.value(s, HOGWARTS.wizard)
        student_school = rdf_data_graph.value(s, HOGWARTS.school)
        student_school_year = rdf_data_graph.value(s, HOGWARTS.school_year)
        student_is_learning = rdf_data_graph.objects(s, HOGWARTS.is_learning)
        student_learned = rdf_data_graph.objects(s, HOGWARTS.learned)
        student_points = rdf_data_graph.value(s, HOGWARTS.has_points)

        # Create a new Student instance in the ontology
        new_student = onto.Student(f"Student_{student_id}")
        new_student.hasStudentId = str(student_id)
        new_student.hasSchoolYear = int(student_school_year)
        new_student.hasPoints = int(student_points)

        # Link the wizard to the student
        wizard_iri = str(student_wizard)
        for wizard_instance in onto.Wizard.instances():
            if extract_id_under(wizard_instance.iri) == extract_id_bar(wizard_iri):
                new_student.hasAccount = wizard_instance
                break

        # Link the school to the student
        school_iri = str(student_school)
        for school_instance in onto.School.instances():
            if extract_id_under(school_instance.iri) == extract_id_bar(school_iri):
                new_student.belongsToSchool = school_instance
                break

        # Link the courses the student is learning
        for course_iri in student_is_learning:
            for course_instance in onto.Course.instances():
                if extract_id_under(course_instance.iri) == extract_id_bar(course_iri):
                    new_student.learnsCourse.append(course_instance)

        # Link the courses the student has learned
        for course_iri in student_learned:
            for course_instance in onto.Course.instances():
                if extract_id_under(course_instance.iri) == extract_id_bar(course_iri):
                    new_student.hasLearnedCourse.append(course_instance)

        print(f"Created Student: {new_student}")


# Create instances
create_instances()

# Save the updated ontology
onto.save(file="updated_ontology.owl", format="rdfxml")
print("Ontology saved as 'updated_ontology.owl'")
