import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

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
    print """\
Title: %s
Description: %s
Max Grade: %s"""%(row[0], row[1], row[2])

def get_grades_by_projects(project_title):
    query = """SELECT project_title, grade, first_name, last_name FROM Grades INNER JOIN Students ON 
        (Students.github=Grades.student_github) WHERE project_title=?"""
    DB.execute(query, (project_title,))
    row = DB.fetchall()
    for i in range(len(row)):
        print """\
    ********
    Title: %s
    Grade: %s
    Name: %s %s"""%(row[i][0], row[i][1], row[i][2], row[i][3])

def add_new_grade(student_github, project_title, grade):
    query = """INSERT INTO Grades (student_github, project_title, grade) VALUES (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added a new grade to project"

def grades_for_student(student_github):
    query = """SELECT * FROM Grades WHERE student_github=?"""
    DB.execute(query, (student_github,))
    row = DB.fetchall()
    for i in range(len(row)):
        print "%s's grade for %s is %d" % (row[i][0], row[i][1], row[i][2])

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
