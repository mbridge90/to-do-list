# Write your code here
from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

options = """
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""

days_of_week = ['Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday']


def add_task():
    print("Enter task")
    task = input()
    print("Enter deadline")
    deadline = input()
    year, month, day = deadline.split('-')
    deadline = datetime(int(year), int(month), int(day))
    new_row = Table(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def get_todays_tasks():
    today = datetime.today()
    print(f"\nToday {today.day} {today.strftime('%b')}:")
    rows = get_rows_by_date(today)
    print_rows(rows)


def get_all_tasks():
    print("\nAll tasks:")
    rows = session.query(Table).order_by(Table.deadline).all()
    if not rows:
        print("Nothing to do!")
    else:
        for i in (range(len(rows))):
            print(str(i + 1) + '.', rows[i].task + '.', rows[i].deadline.day, rows[i].deadline.strftime('%b'))


def get_weeks_tasks():
    for i in range(0, 7):
        date = datetime.today() + timedelta(days=i)
        rows = get_rows_by_date(date)
        print('\n' + days_of_week[date.weekday()], date.day, date.strftime('%b'))
        print_rows(rows)


def get_missed_tasks():
    today = datetime.today()
    print("Missed tasks:")
    rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
    if not rows:
        print("Nothing is missed!")
    else:
        for i in (range(len(rows))):
            print(str(i + 1) + '.', rows[i].task + '.', rows[i].deadline.day, rows[i].deadline.strftime('%b'))


def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    if not rows:
        print("Nothing to delete.")
    else:
        print("Choose the number of the task you want to delete:")
        for i in (range(len(rows))):
            print(str(i + 1) + '.', rows[i].task + '.', rows[i].deadline.day, rows[i].deadline.strftime('%b'))
        task_to_delete = int(input())
        if task_to_delete > len(rows):
            print("Invalid selection")
        else:
            session.delete(rows[task_to_delete - 1])
            session.commit()
            print("The task has been deleted!")




def get_rows_by_date(date):
    return session.query(Table).filter(Table.deadline == date.date()).all()


def print_rows(rows):
    if not rows:
        print("Nothing to do!")
    else:
        for j in (range(len(rows))):
            print(str(j + 1) + '.', rows[j].task)


def main():
    while True:
        print(options)

        choice = input()

        if choice == '1':
            get_todays_tasks()

        elif choice == '2':
            get_weeks_tasks()

        elif choice == '3':
            get_all_tasks()

        elif choice == '4':
            get_missed_tasks()

        elif choice == '5':
            add_task()

        elif choice == '6':
            delete_task()

        elif choice == '0':
            print("Bye!")
            exit()

        else:
            print("Invalid option. Please try again")

main()