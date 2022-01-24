from fastapi import FastAPI,Path
from db_model import Student_Db_Model,engine
from sqlalchemy.orm import sessionmaker
from schemas import StudentApiModel, UpdateStudent


Session = sessionmaker(bind=engine)
session = Session()


#01 create fastapi object 
app=FastAPI()

# root endpoint
@app.get("/")
def root():
    return {"Welcome":"to our school API"}

#fetch list of all students
@app.get("/api/students")
def query_students():
    students = session.query(Student_Db_Model).all()
    dict_students = {}
    for student in students:
        dict_students[student.id]={ "first name:":student.first_name,
                                    "last name: ":student.last_name,
                                    "email: ": student.email,
                                    "gender: ":student.gender
                                    }
    return dict_students
# fetch list of students with specific name
@app.get("/api/students/{student_name}")
def query_students_by_name(student_name:str=Path(None,description="Please enter student's name")):
    students = session.query(Student_Db_Model).filter(Student_Db_Model.first_name==student_name)
    dict_students = {}
    for student in students:
        dict_students[student.id]={ "first name:":student.first_name,
                                    "last name: ":student.last_name,
                                    "email: ": student.email,
                                    "gender: ":student.gender
                                    }
    return dict_students

# add new student
@app.post("/api/students/")
def create_st(user:StudentApiModel):
    new_student =Student_Db_Model(  first_name=user.first_name,
                                    last_name=user.last_name,
                                    email = user.email,
                                    gender = user.gender
                                    )
    session.add(new_student)
    session.commit()
    return {"Message":"You successfully created a new student"}

# delete student
@app.delete("/api/students/{student_id}")
def delete_student_by_id(student_id:int=Path(None,description="Please enter student's name")):
        try:
            student = session.query(Student_Db_Model).filter(Student_Db_Model.id==student_id).first()
            session.delete(student)
            session.commit()
            return {"Message": "Student removed successfully "}
        except:
            return {"Error":"Student with id you entered doesn't exist in our database"}

# update student
@app.put("/api/students/{student_id}")
def update_student(student_id:int, user:UpdateStudent):
    
    student = session.query(Student_Db_Model).filter(Student_Db_Model.id==student_id).first()
    if student !=None:

        if user.first_name!=None:
            student = session.query(Student_Db_Model).filter(Student_Db_Model.id==student_id).first()
            student.first_name = user.first_name
            session.commit()
            
        if user.last_name!=None:
            student = session.query(Student_Db_Model).filter(Student_Db_Model.id==student_id).first()
            student.last_name = user.last_name
            session.commit()
            
        if user.email!=None:
            student = session.query(Student_Db_Model).filter(Student_Db_Model.id==student_id).first()
            student.email = user.email
            session.commit()
            
        if user.gender!=None:
            student = session.query(Student_Db_Model).filter(Student_Db_Model.id==student_id).first()
            student.gender=user.gender
            session.commit()
        return {"Message":"Student's data was successfully modified"}
    else:
        return {"Error":"Student with id you entered doesn't exist in our database"}

