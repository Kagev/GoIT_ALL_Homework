from sqlalchemy import (
    create_engine,
    Column,
    CheckConstraint,
    Integer,
    String,
    Date,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship, declarative_base, validates

from generation_data import (
    data_groups_table,
    data_teacher_table,
    data_subjects_table,
    data_students_table,
    data_grade_table,
)
from main_menu import main_menu

DATABASE_URL = "postgresql://postgres:homework7@localhost:5432/postgres"

Base = declarative_base()
engine = create_engine(DATABASE_URL)


class Group(Base):
    __tablename__ = "groups"
    id = Column("group_id", Integer, primary_key=True)
    group_number = Column(String, nullable=False)
    group_degree = Column(String, nullable=False)
    group_point = Column(String, nullable=False)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column("teacher_id", Integer, primary_key=True)
    teacher_first_name = Column(String, nullable=False)
    teacher_last_name = Column(String, nullable=False)
    teacher_incumbency = Column(String, nullable=False)
    teacher_degree = Column(String)


class Student(Base):
    __tablename__ = "students"
    id = Column("student_id", Integer, primary_key=True)
    student_first_name = Column(String, nullable=False)
    student_last_name = Column(String, nullable=False)
    student_age = Column(
        Integer, CheckConstraint("student_age >= 18 AND student_age <= 90")
    )
    student_bday = Column(Date)
    student_email = Column(String)
    student_phonenumber = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))
    student_course = Column(Integer, nullable=False)
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

    @validates("student_email")
    def validate_email(self, key, email):
        # Replace this with your custom email validation logic
        if "@" not in email:
            raise ValueError("Invalid email format")
        return email

    # @validates('student_phonenumber')
    # def validate_phonenumber(self, key, phonenumber):
    #     # If the phone number does not start with a country code, add one
    #     if not phonenumber.startswith('+'):
    #         # Replace 'XX' with the actual country code you want to add
    #         country_code = '+38'
    #         phonenumber = country_code + phonenumber
    #
    #     # Replace this with your custom phone number validation logic
    #     if '@' in phonenumber or len(phonenumber) < 6:
    #         raise ValueError("Invalid phone format")
    #
    #     return phonenumber


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subject_name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    grade = Column(Integer, nullable=False)
    grade_ECTS = Column(String, nullable=False)
    ects_points = Column(Integer, nullable=False)
    old_system_grade = Column(String, nullable=False)
    date_received = Column(Date)
    student = relationship("Student", back_populates="grades")


Teacher.subjects = relationship(
    "Subject", order_by=Subject.id, back_populates="teacher"
)
Group.students = relationship("Student", order_by=Student.id, back_populates="group")
Student.grades = relationship("Grade", order_by=Grade.id, back_populates="student")

# Create the database tables
Base.metadata.create_all(engine)
