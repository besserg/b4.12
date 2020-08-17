import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer

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
    birthdate = sa.Column(sa.DATE)
    # Рост
    height = sa.Column(sa.REAL)


class Athlete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.DATE)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)


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


def find_athlete(a_height, a_birthdate, session):
    # ищем атлета с ростом, ближайшим к росту пользователя
    query = session.query(Athlete).filter(Athlete.height.isnot(None)).order_by(sa.func.abs(Athlete.height-a_height)).\
        limit(1)
    for inst in query:
        print('Атлет:', inst.name, 'Рост:', inst.height)
    # ищем атлета с датой рождения, ближайшим к дню рождения пользователя
    query = session.query(Athlete).order_by(
        sa.func.abs(sa.func.julianday(a_birthdate) - sa.func.julianday(Athlete.birthdate))).limit(1)
    for inst in query:
        print('Атлет:', inst.name, 'День рождения:', inst.birthdate, 'Разница в возрасте:', abs(a_birthdate - inst.birthdate))


def finduser(idu, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    # находим все записи в таблице User, у которых поле User.first_name совпадает с парарметром name
    qry = session.query(User).filter(User.id == idu)

    # подсчитываем количество таких записей в таблице с помощью метода .count()
    users_cnt = qry.count()
    # если количество пользователей = 1 (больше быть не может т.к. id уникальный),
    # выводим данные пользователя и атлетов, согласно условия задачи
    if users_cnt == 1:
        for inst in qry:
            print('Пользователь:', inst.first_name, inst.last_name, 'Рост:', inst.height, 'День рождения:', inst.birthdate)
            find_athlete(inst.height, inst.birthdate, session)
    # если кол-во найденый строк не равно 1, выводим сообщение об ошибке
    else:
        print('Пользователь с id = ' + idu + ' не найден!')


def main():
    userid = input('Введите id пользователя: ')
    sessions = connect_db()
    finduser(userid, sessions)


if __name__ == "__main__":
    main()