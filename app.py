from fastapi import FastAPI, Path
from db_model import Student_Db_Model, engine
from sqlalchemy.orm import sessionmaker
from schemas import StudentApiModel, UpdateStudent
import logging

# setting up a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("school_api.log")
logger.addHandler(file_handler)

formatter = logging.Formatter("%(asctime)s:%(created)f:%(levelname)s:%(message)s")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# create a database session object
Session = sessionmaker(bind=engine)
session = Session()


# fastapi object
app = FastAPI()


# root endpoint
@app.get("/")
def root():
    return {"Welcome": "to our school API"}


# fetch list of all students
@app.get("/api/students")
def query_students():
    students = session.query(Student_Db_Model).all()
    dict_students = {}
    for student in students:
        dict_students[student.id] = {
            "first name:": student.first_name,
            "last name: ": student.last_name,
            "email: ": student.email,
            "gender: ": student.gender,
        }
    session.close()
    logger.info("List of all students is fetched from the database")
    return dict_students


# fetch list of students with specific name
@app.get("/api/students/{student_name}")
def query_students_by_name(
    student_name: str = Path(None, description="Please enter student's name")
):
    try:

        students = session.query(Student_Db_Model).filter(
            Student_Db_Model.first_name == student_name
        )
        dict_students = {}
        for student in students:
            dict_students[student.id] = {
                "first name:": student.first_name,
                "last name: ": student.last_name,
                "email: ": student.email,
                "gender: ": student.gender,
            }

        logger.info(
            f"List of students with first name {student_name} is fetched fom the database"
        )
        return dict_students
    except Exception as e:
        logger.debug(str(e))
    finally:
        session.close()


# add new student
@app.post("/api/students")
def create_student(user: StudentApiModel):
    try:
        new_student = Student_Db_Model(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            gender=user.gender,
        )
        session.add(new_student)
        session.commit()
        logger.info(
            f"New student, {user.first_name} {user.last_name} is successfully added to our database"
        )
        return {"Message": "You successfully created a new student"}
    except Exception as e:
        logger.debug(str(e))
        return {"Message": "Error while creating a new entry for our database"}
    finally:
        session.close()


# delete student
@app.delete("/api/students/delete/{student_id}")
def delete_student_by_id(
    student_id: int = Path(None, description="Please enter student's name")
):
    try:
        student = (
            session.query(Student_Db_Model)
            .filter(Student_Db_Model.id == student_id)
            .first()
        )
        session.delete(student)
        session.commit()
        logger.info("Student removed successfully ")
        return {"Message": "Student removed successfully "}
    except Exception as e:
        logger.debug(
            f"Student with id {student_id} doesn't exist in our database, error {e}"
        )
        return {"Error": f"Student with id {student_id} doesn't exist in our database"}
    finally:
        session.close()


# update student
@app.put("/api/students/update/{student_id}")
def update_student(student_id: int, user: UpdateStudent):

    student = (
        session.query(Student_Db_Model)
        .filter(Student_Db_Model.id == student_id)
        .first()
    )
    if student != None:

        if user.first_name != None:
            try:
                student = (
                    session.query(Student_Db_Model)
                    .filter(Student_Db_Model.id == student_id)
                    .first()
                )
                student.first_name = user.first_name
                session.commit()
            except:
                session.rollback()
                session.close()
                logger.debug(
                    "First name entry must be string type and it's lenght must be between 1 and 25 characters"
                )
                return {
                    "Message": "First name entry must be string type and it's lenght must be between 1 and 25 characters"
                }

        if user.last_name != None:
            try:
                student = (
                    session.query(Student_Db_Model)
                    .filter(Student_Db_Model.id == student_id)
                    .first()
                )
                student.last_name = user.last_name
                session.commit()
            except:
                session.rollback()
                session.close()
                logger.debug(
                    "Last name entry must be string type and it's lenght must be between 1 and 25 characters"
                )
                return {
                    "Message": "Last name entry must be string type and it's lenght must be between 1 and 25 characters"
                }

        if user.email != None:
            if "@" and "." in user.email:
                student = (
                    session.query(Student_Db_Model)
                    .filter(Student_Db_Model.id == student_id)
                    .first()
                )
                student.email = user.email
                session.commit()
            else:
                session.rollback()
                session.close()
                logger.debug(
                    "Invalid email format, characters @ or . missing from your entry"
                )
                return {
                    "Message": "Invalid email format, characters @ or . missing from your entry"
                }

        if user.gender != None:
            if "male" or "female" in user.gender:
                student = (
                    session.query(Student_Db_Model)
                    .filter(Student_Db_Model.id == student_id)
                    .first()
                )
                student.gender = user.gender
                session.commit()
            else:
                logger.debug(
                    "Invalid entry, you can only insert two values (male or female)"
                )
                return {
                    "Message": "Invalid entry, you can only insert two values (male or female)"
                }

        session.close()
        logger.info(f"Student with id {student_id} data was successfully modified")
        return {
            "Message": f"Student with id {student_id} data was successfully modified"
        }
    else:
        session.rollback()
        session.close()
        logger.debug(f"Student with id {student_id} doesn't exist in our database")
        return {"Error": f"Student with id {student_id} doesn't exist in our database"}
