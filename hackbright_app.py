import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    student_dict = {}

    student_dict["first name"] = row[0]
    student_dict["last name"] = row[1]
    student_dict["github"] = row[2]

    print """\
    Student: %s %s
    Github account: %s"""%(student_dict["first name"], student_dict["last name"], student_dict["github"])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def add_a_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s %s" % (title, description, max_grade)

def get_projects_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title=?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    my_dict = {}

    my_dict["title"] = row[0]
    my_dict["description"] = row[1]
    my_dict["max grade"] = row[2]

    print """\
Title: %s
Description: %s
Max Grade: %s"""%(my_dict["title"], my_dict["description"], my_dict["max grade"])

def get_grades_by_projects(project_title):
    query = """SELECT project_title, grade, first_name, last_name FROM Grades INNER JOIN Students ON 
        (Students.github=Grades.student_github) WHERE project_title=?"""
    DB.execute(query, (project_title,))
    row = DB.fetchall()

    my_dict = {}

    for i in row:
        my_dict["first name"] = i[2]
        my_dict["last name"] = i[3]
        my_dict["project title"] = i[0]
        my_dict["grade"] = i[1]
        print """\
    ********
    Name: %s %s
    Title: %s
    Grade: %s"""%(my_dict["first name"], my_dict["last name"], my_dict["project title"], my_dict["grade"])

def add_new_grade(student_github, project_title, grade):
    query = """INSERT INTO Grades (student_github, project_title, grade) VALUES (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added a new grade to project"

def grades_for_student(first_name, last_name):
    query = """SELECT first_name, last_name, project_title, grade 
        FROM Grades 
        INNER JOIN Students ON (github=student_github) 
        WHERE first_name= ? AND last_name = ? """
    DB.execute(query, (first_name, last_name))
    my_dictionary = {}
    row = DB.fetchall()

    for i in row:
        my_dictionary["first name"] = i[0]
        my_dictionary["last name"] = i[1]
        my_dictionary["project title"] = i[2]
        my_dictionary["grade"] = i[3]
        print "%s %s's grade for %s is %d" % (my_dictionary["first name"], my_dictionary["last name"], my_dictionary["project title"], my_dictionary["grade"])

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(', ')
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_projects_by_title(*args)
        elif command == "new_project":
            add_a_project(*args)
        elif command == "project_grade":
            get_grades_by_projects(*args)
        elif command == "new_grade":
            add_new_grade(*args)
        elif command == "all_grades":
            grades_for_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()
