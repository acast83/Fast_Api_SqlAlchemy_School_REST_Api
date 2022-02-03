from fastapi import FastAPI, Path, status, HTTPException
from db_model import Student_Db_Model, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from schemas import StudentApiModel, UpdateStudent
import logging
import re

reg_email_validation = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

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
    return {"Message": "Welcome to our school API"}


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


# fetch list of students with limit and offset
@app.get("/api/students/{offset_val},{limit_val}")
def query_students_with_limit_and_offset(
    offset_val: int = Path(None, description="please enter offset value"),
    limit_val: int = Path(None, description="Please enter limit value"),
):
    try:
        students = (
            session.query(Student_Db_Model).offset(offset_val).limit(limit_val).all()
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
            f"List of students is fetched from the database, offset is {offset_val}, limit is {limit_val}"
        )
        return dict_students
    except Exception as e:
        session.rollback()
        logger.debug(f"Error, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error, {str(e)}"
        )
    finally:
        session.close()


# fetch list of students with specific name
@app.get("/api/students/{student_name}")
def query_students_by_name(
    student_name: str = Path(None, description="Please enter student's name")
):
    if student_name.isalpha():
        try:

            students = session.query(Student_Db_Model).filter(
                func.lower(Student_Db_Model.first_name) == func.lower(student_name)
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error, ({str(e)})",
            )

        finally:
            session.close()
    else:
        logger.debug(f"Error, invalid first name input ({student_name})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error, invalid first name input {student_name}, please use only alphabetic values, character number between 1 and 25",
        )


# add new student
@app.post("/api/students")
def create_student(user: StudentApiModel):

    # input validation
    if user.first_name.isalpha() and 1 <= len(user.first_name) <= 25:
        if user.last_name.isalpha() and 1 <= len(user.last_name) <= 25:
            if re.fullmatch(reg_email_validation, user.email):

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
                    return {
                        "Message": f"New student, {user.first_name} {user.last_name} is successfully added to our database"
                    }
                except Exception as e:
                    logger.debug(str(e))
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Error, {str(e)}",
                    )
                finally:
                    session.close()

            else:
                logger.debug(f"Error, invalid email format")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid email format",
                )

        else:
            logger.debug(
                f"Error, invalid last name input {user.last_name}, please use only alphabetic values, character number between 1 and 25"
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error, invalid first name input {user.last_name}, please use only alphabetic values, character number between 1 and 25",
            )

    else:
        logger.debug(
            f"Error, invalid first name input {user.first_name}, please use only alphabetic values, character number between 1 and 25"
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error, invalid first name input {user.first_name}, please use only alphabetic values, character number between 1 and 25",
        )


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
        logger.info(f"Student with id {student_id} removed successfully ")
        return {"Message": f"Student with id {student_id} removed successfully "}

    except Exception as e:
        logger.debug(
            f"Student with id {student_id} doesn't exist in our database, error {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} doesn't exist in our database",
        )

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
            if user.first_name.isalpha() and 1 <= len(user.first_name) <= 25:

                try:
                    student = (
                        session.query(Student_Db_Model)
                        .filter(Student_Db_Model.id == student_id)
                        .first()
                    )
                    student.first_name = user.first_name
                    session.commit()

                except Exception as e:
                    session.rollback()
                    logger.debug(f"Error, {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Error, {str(e)}",
                    )
                finally:
                    session.close()

            else:
                logger.debug(
                    f"Error, invalid first name input {user.first_name}, please use only alphabetic characters"
                )
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Error, invalid first name input {user.first_name}, please use only alphabetic characters",
                )

        if user.last_name != None:
            if user.last_name.isalpha() and 1 <= len(user.last_name) <= 25:

                try:
                    student = (
                        session.query(Student_Db_Model)
                        .filter(Student_Db_Model.id == student_id)
                        .first()
                    )
                    student.last_name = user.last_name
                    session.commit()

                except Exception as e:
                    session.rollback()
                    logger.debug(f"Error, {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Error, {str(e)}",
                    )

                finally:
                    session.close()

            else:
                logger.debug(
                    f"Error, invalid last name input {user.last_name}, please use only alphabetic characters"
                )
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Error, invalid last name input {user.last_name}, please use only alphabetic characters",
                )

        if user.email != None:
            if re.fullmatch(reg_email_validation, user.email):
                try:
                    student = (
                        session.query(Student_Db_Model)
                        .filter(Student_Db_Model.id == student_id)
                        .first()
                    )
                    student.email = user.email
                    session.commit()

                except Exception as e:
                    session.rollback()
                    logger.debug(f"Error, {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Error, {str(e)}",
                    )

                finally:
                    session.close()

            else:
                logger.debug(f"Invalid email format ({user.email})")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid email format ({user.email})",
                )

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
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid entry ({user.gender}), you can only insert two values (male or female)",
                )

        session.close()
        logger.info(f"Student with id {student_id} data was successfully modified")
        return {
            "Message": f"Student with id {student_id} data was successfully modified"
        }

    else:
        session.rollback()
        session.close()
        logger.debug(f"Student with id {student_id} doesn't exist in our database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} doesn't exist in our database",
        )
