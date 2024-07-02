import csv
import random

def accounts():
    rdf = []
    csv_file = './original_db/Accounts.csv'
    with open(csv_file, 'r') as accounts_file:
        accounts_reader = csv.DictReader(accounts_file)
        for account_row in accounts_reader:
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#Account_{account_row['Id']}">')
            rdf.append(f'\t\t<hogwarts:hasAccount rdf:resource="http://hogwarts.edu/ontology.owl#Wizard_{account_row["wizardId"]}"/>')
            rdf.append(f'\t\t<hogwarts:hasMechanographicalNumber rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{account_row["nmec"]}</hogwarts:hasMechanographicalNumber>')
            rdf.append(f'\t\t<hogwarts:hasPassword>{account_row["password"]}</hogwarts:hasPassword>')
            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def wizards():
    
    csv_file = './original_db/Wizard.csv'
    skills_file = './original_db/RelationWizardSkill.csv'

    wizards = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            wizards[row['Id']] = row

    skills = {}
    with open(skills_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            wizard_id = row['WizardId']
            skill_id = row['SkillId']
            if wizard_id in skills:
                skills[wizard_id].append(skill_id)
            else:
                skills[wizard_id] = [skill_id]

    rdf = []
    for wizard_id, wizard_info in wizards.items():
        rdf.append('\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#Wizard_{id}">'.format(id=wizard_info['Id']))
        if wizard_info['Name'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:hasName>{name}</hogwarts:hasName>'.format(name=wizard_info['Name']))
        if wizard_info['Gender'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:hasGender>{gender}</hogwarts:hasGender>'.format(gender=wizard_info['Gender']))
        if wizard_info['Species'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:hasSpecies>{species}</hogwarts:hasSpecies>'.format(species=wizard_info['Species']))
        if wizard_info['Blood-Type'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:hasBloodType>{blood}</hogwarts:hasBloodType>'.format(blood=wizard_info['Blood-Type']))
        if wizard_info['Eye Color'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:hasEyeColor>{eye_color}</hogwarts:hasEyeColor>'.format(eye_color=wizard_info['Eye Color']))
        if wizard_info['HouseId'] not in ["None", "none", ""]: 
            rdf.append('\t\t<hogwarts:belongsToHouse rdf:resource="http://hogwarts.edu/ontology.owl#House_{house}"/>'.format(house=wizard_info['HouseId'])) 
        else: 
            rdf.append('\t\t<hogwarts:belongsToHouse rdf:resource="http://hogwarts.edu/ontology.owl#House_{house}"/>'.format(house=random.randint(1,4)))
        if wizard_info['Wand'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:hasWand>{wand}</hogwarts:hasWand>'.format(wand=wizard_info['Wand']))
        if wizard_info['Patronus'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:hasPatronus>{patronus}</hogwarts:hasPatronus>'.format(patronus=wizard_info['Patronus']))
        for skill_id in skills.get(wizard_id, []):
            rdf.append('\t\t<hogwarts:hasSkill rdf:resource="http://hogwarts.edu/ontology.owl#Skill_{skill_id}"/>'.format(skill_id=skill_id))
        rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def students():
    rdf = []
    csv_file = './original_db/Student.csv'
    courses_file = './original_db/Courses.csv'

    courses = {}
    with open(courses_file, 'r', encoding='utf-8') as courses_file:
        courses_reader = csv.DictReader(courses_file)
        for row in courses_reader:
            courses[row['Id']] = {'name': row['Name'], 'year': int(row['AttendingYear'])}

    with open(csv_file, 'r', encoding='utf-8') as students_file:
        students_reader = csv.DictReader(students_file)
        for row in students_reader:
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#Student_{row['Id']}">')
            rdf.append(f'\t\t<hogwarts:hasAccount rdf:resource="http://hogwarts.edu/ontology.owl#Wizard_{row["WizardId"]}"/>')
            rdf.append(f'\t\t<hogwarts:belongsToSchool rdf:resource="http://hogwarts.edu/ontology.owl#School_{row["SchoolId"]}"/>')
            rdf.append(f'\t\t<hogwarts:hasSchoolYear rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{row["SchoolYear"]}</hogwarts:hasSchoolYear>')
            rdf.append('\t\t<hogwarts:hasPoints rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{points}</hogwarts:hasPoints>'.format(points=random.randint(1,100)))

            attending_courses = [course_id for course_id, course_info in courses.items() if course_info['year'] == int(row['SchoolYear'])]
            for course_id in attending_courses:
                rdf.append(f'\t\t<hogwarts:learnsCourse rdf:resource="http://hogwarts.edu/ontology.owl#Course_{course_id}"/>')

            learned_courses = [course_id for course_id, course_info in courses.items() if course_info['year'] < int(row['SchoolYear'])]
            for course_id in learned_courses:
                rdf.append(f'\t\t<hogwarts:hasLearnedCourse rdf:resource="http://hogwarts.edu/ontology.owl#Course_{course_id}"/>')

            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def spells():
    rdf = []
    csv_file = './original_db/Spell.csv'
    
    with open(csv_file, 'r', encoding='utf-8-sig') as spells_file:
        spells_reader = csv.DictReader(spells_file)
        for row in spells_reader:
            spell_id = row['Id']
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#Spell_{spell_id}">')
            rdf.append(f'\t\t<hogwarts:hasName>{row["Name"]}</hogwarts:hasName>')
            rdf.append(f'\t\t<hogwarts:hasIncantation>{row["Incantation"]}</hogwarts:hasIncantation>')
            rdf.append(f'\t\t<hogwarts:hasType>{row["Type"]}</hogwarts:hasType>')
            rdf.append(f'\t\t<hogwarts:hasEffect>{row["Effect"]}</hogwarts:hasEffect>')
            if row['Light']:
                rdf.append(f'\t\t<hogwarts:hasLight>{row["Light"]}</hogwarts:hasLight>') 
            rdf.append('\t</rdf:Description>')
            
    rdf.append("")
    return rdf

def skills():
    rdf = []
    csv_file = './original_db/Skills.csv'
    
    with open(csv_file, 'r', encoding='utf-8') as skills_file:
        skills_reader = csv.DictReader(skills_file)
        for row in skills_reader:
            skill_id = row['Id']
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#Skill_{skill_id}">')
            rdf.append(f'\t\t<hogwarts:hasSkillName>{row["Name"]}</hogwarts:hasSkillName>')
            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def school():
    csv_file = './original_db/School.csv'
    rdf = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rdf.append('\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#School_{id}">'.format(id=row['Id']))
            rdf.append('\t\t<hogwarts:hasSchoolName>{name}</hogwarts:hasSchoolName>'.format(name=row['Name']))
            rdf.append('\t\t<hogwarts:hasLocation>{location}</hogwarts:hasLocation>'.format(location=row['Location']))
            rdf.append('\t\t<hogwarts:hasDateOfCreation>{date}</hogwarts:hasDateOfCreation>'.format(date=row['DateOfCreation']))
            rdf.append('\t\t<hogwarts:hasHeadmaster rdf:resource="http://hogwarts.edu/ontology.owl#Headmaster_{headmaster}"/>'.format(headmaster=row['HeadmasterId']))
            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def professors():
    rdf = []
    csv_file = './original_db/Professor.csv'
    
    with open(csv_file, 'r', encoding='utf-8') as professors_file:
        professors_reader = csv.DictReader(professors_file)
        for row in professors_reader:
            professor_id = row['Id']
            wizard_id = row['WizardId']
            school_id = row['SchoolId']
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#Professor_{professor_id}">')
            rdf.append(f'\t\t<hogwarts:hasAccount rdf:resource="http://hogwarts.edu/ontology.owl#Wizard_{wizard_id}"/>')
            rdf.append(f'\t\t<hogwarts:teachesAtSchool rdf:resource="http://hogwarts.edu/ontology.owl#School_{school_id}"/>')
            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def houses():
    rdf = []
    csv_file = './original_db/House.csv'

    with open(csv_file, 'r') as houses_file:
        houses_reader = csv.DictReader(houses_file)
        for row in houses_reader:
            house_id = row['Id']
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#House_{house_id}">')
            rdf.append(f'\t\t<hogwarts:hasHouseName>{row["Name"]}</hogwarts:hasHouseName>')
            rdf.append(f'\t\t<hogwarts:hasSymbol>{row["Symbol"]}</hogwarts:hasSymbol>')
            rdf.append(f'\t\t<hogwarts:hasFounder rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{row["FounderId"]}</hogwarts:hasFounder>')
            rdf.append(f'\t\t<hogwarts:hasLocation>{row["Location"]}</hogwarts:hasLocation>')
            rdf.append(f'\t\t<hogwarts:hasHouseProfessor rdf:resource="http://hogwarts.edu/ontology.owl#Professor_{row["ProfessorInCharge"]}"/>')
            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def headmaster():
    rdf = []
    csv_file = './original_db/Headmaster.csv'

    with open(csv_file, 'r') as headmasters_file:
        headmasters_reader = csv.DictReader(headmasters_file)
        for row in headmasters_reader:
            headmaster_id = row['Id']
            wizard_id = row['WizardId']
            start_date = row['Start_date']
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#Headmaster_{headmaster_id}">')
            rdf.append(f'\t\t<hogwarts:hasAccount rdf:resource="http://hogwarts.edu/ontology.owl#Wizard_{wizard_id}"/>')
            rdf.append(f'\t\t<hogwarts:hasStartDate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{start_date}</hogwarts:hasStartDate>')
            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def courses():
    rdf = []
    csv_file = './original_db/Courses.csv'

    with open(csv_file, 'r') as courses_file:
        courses_reader = csv.DictReader(courses_file)
        for course_row in courses_reader:
            course_id = course_row['Id']
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/ontology.owl#Course_{course_id}">')
            rdf.append(f'\t\t<hogwarts:hasCourseName>{course_row["Name"]}</hogwarts:hasCourseName>')
            rdf.append(f'\t\t<hogwarts:hasCourseType>{course_row["Type"]}</hogwarts:hasCourseType>')
            rdf.append(f'\t\t<hogwarts:hasAttendingYear rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{course_row["AttendingYear"]}</hogwarts:hasAttendingYear>')
            rdf.append(f'\t\t<hogwarts:hasProfessor rdf:resource="http://hogwarts.edu/ontology.owl#Professor_{course_row["ProfessorId"]}"/>')
            
            with open('./original_db/RelationCourseSpell.csv', 'r') as course_spell_file:
                course_spell_reader = csv.DictReader(course_spell_file)
                for course_spell_row in course_spell_reader:
                    if course_spell_row['CourseId'] == course_id:
                        spell_id = course_spell_row['SpellId']
                        rdf.append(f'\t\t<hogwarts:teachesSpell rdf:resource="http://hogwarts.edu/ontology.owl#Spell_{spell_id}"/>')
            
            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

if __name__ == "__main__":
    rdf_data = []
    rdf_data.extend(accounts())
    rdf_data.extend(wizards())
    rdf_data.extend(students())
    rdf_data.extend(spells())
    rdf_data.extend(skills())
    rdf_data.extend(school())
    rdf_data.extend(professors())
    rdf_data.extend(houses())
    rdf_data.extend(headmaster())
    rdf_data.extend(courses())
    
    with open('data.rdf', 'w', encoding='utf-8-sig') as out_file:
        out_file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        out_file.write('<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:hogwarts="http://hogwarts.edu/ontology.owl#">\n\n')
        out_file.write('\n'.join(rdf_data))
        out_file.write('</rdf:RDF>')