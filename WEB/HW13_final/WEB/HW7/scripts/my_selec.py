from sqlalchemy import func, desc
from sqlalchemy.orm import query
from database.models import Student, Group, Subject, Teacher, Grade
from sqlalchemy import func, desc
from sqlalchemy.ext.asyncio import AsyncSession

Student.fullname = Student.student_first_name + " " + Student.student_last_name


def select_1(session: AsyncSession):
    query = (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )

    result = query.all()
    return result


def select_2(session, subject_id):
    query = (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )

    result = query.first()
    return result


def select_3(session, subject_id):
    query = (
        session.query(
            Group.group_number, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade, Group.group_id == Grade.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.group_number)
    )

    result = query.all()
    return result


def select_4(session):
    query = session.query(func.round(func.avg(Grade.grade), 2).label("avg_grade"))

    result = query.scalar()
    return result


def select_5(session, teacher_id):
    query = session.query(Subject.subject_name).filter(Subject.teacher_id == teacher_id)

    result = query.all()
    return result


def select_6(session, group_id):
    query = (
        session.query(func.concat(Student.student_first_name, " ", Student.student_last_name).label("fullname"))
        .join(Group, Student.group_id == Group.group_id)
        .filter(Group.group_id == group_id)
    )

    result = query.all()
    return result


def select_7(session, group_id, subject_id):
    query = (
        session.query(Student.fullname, Grade.grade, Grade.date_received)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
    )

    result = query.all()
    return result


def select_8(session, teacher_id):
    query = (
        session.query(func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.teacher_id == teacher_id)
    )

    result = query.scalar()
    return result


def select_9(session, student_id):
    query = (
        session.query(Subject.subject_name)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Grade.student_id == student_id)
    )

    result = query.all()
    return result


def select_10(session, student_id, teacher_id):
    query = (
        session.query(Subject.subject_name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Grade.student_id == student_id, Teacher.id == teacher_id)
    )

    result = query.all()
    return result
