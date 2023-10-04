from database.db import Base, session_db
from sqlalchemy import Column, CheckConstraint, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates


class Group(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True)
    group_degree = Column(String)
    group_point = Column(String, nullable=False)
    group_number = Column(Integer, nullable=False)


class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = {"extend_existing": True}  # Add the extend_existing option
    id = Column(Integer, primary_key=True)
    ects_points = Column(Integer)
    grade_ects = Column(String(2))
    old_system_grade = Column(String)
    grade = Column(Integer)
    date_received = Column(Date)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    student = relationship("Student", back_populates="grades")

    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="grades")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column("teacher_id", Integer, primary_key=True)
    teacher_first_name = Column(String, nullable=False)
    teacher_last_name = Column(String, nullable=False)
    teacher_incumbency = Column(String, nullable=False)  # должность
    teacher_degree = Column(String)  # научная степень
    teacher_age = Column(
        Integer, CheckConstraint("teacher_age >= 18 AND teacher_age <= 90")
    )
    teacher_email = Column(String(100))
    teacher_phone_number = Column(String)
    subject_id = Column(Integer, ForeignKey("subjects.id"))


class Student(Base):
    __tablename__ = "students"
    id = Column("student_id", Integer, primary_key=True)
    student_first_name = Column(String, nullable=False)
    student_last_name = Column(String, nullable=False)
    student_age = Column(
        Integer, CheckConstraint("student_age >= 18 AND student_age <= 90")
    )
    student_birthday = Column(Date)
    student_email = Column(String(100))
    student_phone_number = Column(String)
    student_course = Column(String, nullable=False)

    # связь с таблицей groups
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    group = relationship("Group")

    grades = relationship("Grade", back_populates="student")

    @property
    def fullname(self):
        return f"{self.student_first_name} {self.student_last_name}"



class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(150), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"))
    grades = relationship("Grade", back_populates="subject")


if __name__ == "__main__":
    session = session_db()
    Base.metadata.create_all(session.bind)
    session.commit()
    session.close()
