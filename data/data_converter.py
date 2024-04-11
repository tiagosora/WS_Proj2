import csv

def accounts():
    rdf = []
    csv_file = './original_db/Accounts.csv'
    with open(csv_file, 'r') as accounts_file:
        accounts_reader = csv.DictReader(accounts_file)
        for account_row in accounts_reader:
            account_id = account_row['Id']
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/accounts/{account_id}">')
            rdf.append(f'\t\t<hogwarts:id>{account_id}</hogwarts:id>')
            rdf.append('\t\t<hogwarts:_type>account</hogwarts:_type>')
            rdf.append(f'\t\t<hogwarts:number>{account_row["nmec"]}</hogwarts:number>')
            rdf.append(f'\t\t<hogwarts:password>{account_row["password"]}</hogwarts:password>')
            rdf.append(f'\t\t<hogwarts:wizard rdf:resource="http://hogwarts.edu/wizards/{account_row["wizardId"]}"/>')
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
        rdf.append('\t<rdf:Description rdf:about="http://hogwarts.edu/wizards/{id}">'.format(id=wizard_info['Id']))
        rdf.append('\t\t<hogwarts:id>{id}</hogwarts:id>'.format(id=wizard_info['Id']))
        rdf.append('\t\t<hogwarts:_type>wizard</hogwarts:_type>')
        if wizard_info['Name'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:name>{name}</hogwarts:name>'.format(name=wizard_info['Name']))
        if wizard_info['Gender'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:gender>{gender}</hogwarts:gender>'.format(gender=wizard_info['Gender']))
        if wizard_info['Species'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:species>{species}</hogwarts:species>'.format(species=wizard_info['Species']))
        if wizard_info['Blood-Type'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:blood-type>{blood}</hogwarts:blood-type>'.format(blood=wizard_info['Blood-Type']))
        if wizard_info['Eye Color'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:eye_color>{eye_color}</hogwarts:eye_color>'.format(eye_color=wizard_info['Eye Color']))
        if wizard_info['HouseId'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:house>{house}</hogwarts:house>'.format(house=wizard_info['HouseId']))
        if wizard_info['Wand'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:wand>{wand}</hogwarts:wand>'.format(wand=wizard_info['Wand']))
        if wizard_info['Patronus'] not in ["None", "none", ""]: rdf.append('\t\t<hogwarts:patronus>{patronus}</hogwarts:patronus>'.format(patronus=wizard_info['Patronus']))
        for skill_id in skills.get(wizard_id, []):
            rdf.append('\t\t<hogwarts:has_skill rdf:resource="http://hogwarts.edu/skills/{skill_id}"/>'.format(skill_id=skill_id))
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
            student_id = row['Id']
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/students/{student_id}">')
            rdf.append(f'\t\t<hogwarts:id>{student_id}</hogwarts:id>')
            rdf.append('\t\t<hogwarts:_type>student</hogwarts:_type>')
            rdf.append(f'\t\t<hogwarts:wizard rdf:resource="http://hogwarts.edu/wizards/{row["WizardId"]}"/>')
            rdf.append(f'\t\t<hogwarts:school rdf:resource="http://hogwarts.edu/schools/{row["SchoolId"]}"/>')
            rdf.append(f'\t\t<hogwarts:school_year>{row["SchoolYear"]}</hogwarts:school_year>')

            attending_courses = [course_id for course_id, course_info in courses.items() if course_info['year'] == int(row['SchoolYear'])]
            for course_id in attending_courses:
                rdf.append(f'\t\t<hogwarts:is_learning rdf:resource="http://hogwarts.edu/courses/{course_id}"/>')

            learned_courses = [course_id for course_id, course_info in courses.items() if course_info['year'] < int(row['SchoolYear'])]
            for course_id in learned_courses:
                rdf.append(f'\t\t<hogwarts:learned rdf:resource="http://hogwarts.edu/courses/{course_id}"/>')

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
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/spells/{spell_id}">')
            rdf.append(f'\t\t<hogwarts:id>{spell_id}</hogwarts:id>')
            rdf.append('\t\t<hogwarts:_type>spell</hogwarts:_type>')
            rdf.append(f'\t\t<hogwarts:name>{row["Name"]}</hogwarts:name>')
            rdf.append(f'\t\t<hogwarts:incantation>{row["Incantation"]}</hogwarts:incantation>')
            rdf.append(f'\t\t<hogwarts:type>{row["Type"]}</hogwarts:type>')
            rdf.append(f'\t\t<hogwarts:effect>{row["Effect"]}</hogwarts:effect>')
            if row['Light']:
                rdf.append(f'\t\t<hogwarts:light>{row["Light"]}</hogwarts:light>') 
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
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/skills/{skill_id}">')
            rdf.append(f'\t\t<hogwarts:id>{skill_id}</hogwarts:id>')
            rdf.append('\t\t<hogwarts:_type>skill</hogwarts:_type>')
            rdf.append(f'\t\t<hogwarts:name>{row["Name"]}</hogwarts:name>')
            rdf.append('\t</rdf:Description>')
    
    rdf.append("")
    return rdf

def school():
    csv_file = './original_db/School.csv'
    rdf = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rdf.append('\t<rdf:Description rdf:about="http://hogwarts.edu/schools/{id}">'.format(id=row['Id']))
            rdf.append('\t\t<hogwarts:id>{id}</hogwarts:id>'.format(id=row['Id']))
            rdf.append('\t\t<hogwarts:_type>school</hogwarts:_type>')
            rdf.append('\t\t<hogwarts:name>{name}</hogwarts:name>'.format(name=row['Name']))
            rdf.append('\t\t<hogwarts:location>{location}</hogwarts:location>'.format(location=row['Location']))
            rdf.append('\t\t<hogwarts:dateOfCreation>{date}</hogwarts:dateOfCreation>'.format(date=row['DateOfCreation']))
            rdf.append('\t\t<hogwarts:headmaster rdf:resource="http://hogwarts.edu/wizards/{headmaster}"/>'.format(headmaster=row['HeadmasterId']))
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
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/professors/{professor_id}">')
            rdf.append(f'\t\t<hogwarts:id>{professor_id}</hogwarts:id>')
            rdf.append('\t\t<hogwarts:_type>professor</hogwarts:_type>')
            rdf.append(f'\t\t<hogwarts:wizard rdf:resource="http://hogwarts.edu/wizards/{wizard_id}"/>')
            rdf.append(f'\t\t<hogwarts:school rdf:resource="http://hogwarts.edu/schools/{school_id}"/>')
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
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/houses/{house_id}">')
            rdf.append(f'\t\t<hogwarts:id>{house_id}</hogwarts:id>')
            rdf.append('\t\t<hogwarts:_type>house</hogwarts:_type>')
            rdf.append(f'\t\t<hogwarts:name>{row["Name"]}</hogwarts:name>')
            rdf.append(f'\t\t<hogwarts:symbol>{row["Symbol"]}</hogwarts:symbol>')
            rdf.append(f'\t\t<hogwarts:founder>{row["FounderId"]}</hogwarts:founder>')
            rdf.append(f'\t\t<hogwarts:location>{row["Location"]}</hogwarts:location>')
            rdf.append(f'\t\t<hogwarts:professorInCharge rdf:resource="http://hogwarts.edu/professors/{row["ProfessorInCharge"]}"/>')
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
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/headmasters/{headmaster_id}">')
            rdf.append(f'\t\t<hogwarts:id>{headmaster_id}</hogwarts:id>')
            rdf.append('\t\t<hogwarts:_type>headmaster</hogwarts:_type>')
            rdf.append(f'\t\t<hogwarts:wizard rdf:resource="http://hogwarts.edu/wizards/{wizard_id}"/>')
            rdf.append(f'\t\t<hogwarts:start_date>{start_date}</hogwarts:start_date>')
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
            rdf.append(f'\t<rdf:Description rdf:about="http://hogwarts.edu/courses/{course_id}">')
            rdf.append(f'\t\t<hogwarts:id>{course_id}</hogwarts:id>')
            rdf.append('\t\t<hogwarts:_type>course</hogwarts:_type>')
            rdf.append(f'\t\t<hogwarts:name>{course_row["Name"]}</hogwarts:name>')
            rdf.append(f'\t\t<hogwarts:type>{course_row["Type"]}</hogwarts:type>')
            rdf.append(f'\t\t<hogwarts:attending_year>{course_row["AttendingYear"]}</hogwarts:attending_year>')
            rdf.append(f'\t\t<hogwarts:professor rdf:resource="http://hogwarts.edu/professors/{course_row["ProfessorId"]}"/>')
            
            with open('./original_db/RelationCourseSpell.csv', 'r') as course_spell_file:
                course_spell_reader = csv.DictReader(course_spell_file)
                for course_spell_row in course_spell_reader:
                    if course_spell_row['CourseId'] == course_id:
                        spell_id = course_spell_row['SpellId']
                        rdf.append(f'\t\t<hogwarts:teaches_spell rdf:resource="http://hogwarts.edu/spells/{spell_id}"/>')
            
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
    
    with open('data_.rdf', 'w', encoding='utf-8-sig') as out_file:
        out_file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        out_file.write('<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:hogwarts="http://hogwarts.edu/ontology#">\n\n')
        out_file.write('\n'.join(rdf_data))
        out_file.write('</rdf:RDF>')