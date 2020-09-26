from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Create database file
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def add_task(task, deadline=''):
    if deadline == '':
        new_task = Table(task=task)
    else:
        deadline = datetime.strptime(deadline, "%Y-%m-%d")
        new_task = Table(task=task, deadline=deadline)
    session.add(new_task)
    session.commit()


if __name__ == "__main__":
    # Create table in database
    Base.metadata.create_all(engine)

    # Access database
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Add task")
        print("0) Exit")
        user = input()

        if user == '1':
            today = datetime.today()
            day_month = today.strftime('%-d %b')

            get_row = session.query(Table).filter(Table.deadline == today.date()).all()

            print(f"\nToday {day_month}:")
            if len(get_row) == 0:
                print("Nothing to do!\n")
            else:
                for i, task in enumerate(get_row):
                    print(f"{i + 1}. {task}\n")
        elif user == '2':
            for i in range(7):
                # The day
                tday = datetime.today() + timedelta(days=i)
                day_month = tday.strftime('%A %-d %b')

                get_row = session.query(Table).filter(Table.deadline == tday.date()).all()

                print(f"\n{day_month}:")
                if len(get_row) == 0:
                    print("Nothing to do!")
                else:
                    for j, task in enumerate(get_row):
                        print(f"{j + 1}. {task}")
            print("")
        elif user == '3':
            get_row = session.query(Table).order_by(Table.deadline).all()

            print("\nAll tasks:")
            for i, task in enumerate(get_row):
                print(f"{i + 1}. {task}. {task.deadline.strftime('%-d %b')}")
            print("")
        elif user == '4':
            print('')
            tsk = input('Enter task\n')
            dl = input('Enter deadline\n')
            add_task(tsk, dl)
            print("The task has been added!\n")
        elif user == '0':
            print("\nBye!")
            break
