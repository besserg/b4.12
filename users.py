import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DBPATH = 'sqlite:///sochi_athletes.sqlite3'
Base = declarative_base()


class User(Base):
    __tablename__ ="user"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    # Имя
    first_name = sa.Column(sa.TEXT)
    # Фамилия
    last_name = sa.Column(sa.TEXT)
    # Пол
    gender = sa.Column(sa.TEXT)
    # e-mail
    email = sa.Column(sa.TEXT)
    # День рождения
    birthdate = sa.Column(sa.TEXT)
    # Рост
    height = sa.Column(sa.REAL)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DBPATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    if input("Пол (М/Ж): ") in ('M', 'Male', 'М', 'Муж', 'Мужской'):
        gender = 'Male'
    elif input("Пол: ") in ('F', 'Female', 'Ж', 'Жен', 'Женский'):
        gender = 'Female'
    else:
        gender = ''
    email = input("e-mail: ")
    birthdate = input("День рождения (гггг-мм-дд): ")
    height = input("Рост: ")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Данные сохранены!")


if __name__ == "__main__":
    main()

