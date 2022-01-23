from db_model import Student,engine
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()


class Student_Methods:

    #method for creating a new student
    @staticmethod
    def create_student(f_name, l_name,em,gend):
        new_student =Student(first_name=f_name,last_name=l_name,email = em,gender = gend)
        session.add(new_student)
        session.commit()

    #method for query all students
    @staticmethod
    def query_students():
        students = session.query(Student).all()
        lista_students = []
        for student in students:
            lista_students.append({"first name:":student.first_name, "last name: ":student.last_name,"email: ": student.email,"gender: ":student.gender})
        return lista_students
    #method for updating a student's data
    @staticmethod
    def update_student_by_id(student_id,f_name=None, l_name=None,student_email=None,student_gender=None):
        student = session.query(Student).filter(Student.id==student_id).first()
        if student !=None:

            if f_name!=None:
                student = session.query(Student).filter(Student.id==student_id).first()
                student.first_name = f_name
                session.commit()
                return {"Message":f'First name was succsefully changed for student with student id {student_id}'}
            if l_name!=None:
                student = session.query(Student).filter(Student.id==student_id).first()
                student.last_name = l_name
                session.commit()
                return {"Message":f'Last name was succsefully changed for student with student id {student_id}'}
            if student_email!=None:
                student = session.query(Student).filter(Student.id==student_id).first()
                student.email = student_email
                session.commit()
                return {"Message":f'Email was succsefully changed for student with student id {student_id}'}
            if student_gender!=None:
                student = session.query(Student).filter(Student.id==student_id).first()
                student.gender=student_gender
                session.commit()
                return {"Message":f'Gender was succsefully changed for student with student id {student_id}'}
        else:
            return {"Error":"Student with id you entered doesn't exist in our database"}

    # method for deleting students data
    @staticmethod
    def delete_student_by_id(student_id):
        try:
            student = session.query(Student).filter(Student.id==student_id).first()
            session.delete(student)
            session.commit()
        except:
            return {"Error":"Student with id you entered doesn't exist in our database"}
    
    
# Student_Methods.create_student("Jelena","Petrovic","jelena85@gmail.com","female")
# Student_Methods.update_student_by_id(2,"Milena",None,"milena@gmail.com",None)
# Student_Methods.delete_student_by_id(2)
# Student_Methods.query_students()