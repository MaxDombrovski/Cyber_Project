import sqlite3


class tblUser(object):
    def __init__(self,
                 tablename="tblUser", id="Id", name="Name", email="Email", password="Password",
                 appearance_id="Appearance_Id", gamescore_id="Gamescore_Id"):
        self.__tablename = tablename
        self.__id = id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__appearance_id = appearance_id
        self.__gamescore_id = gamescore_id

        conn = sqlite3.connect('game.db')
        strsql1 = f'CREATE TABLE IF NOT EXISTS {self.__tablename} ({self.__id} INTEGER PRIMARY KEY AUTOINCREMENT, '
        strsql1 += f'{self.__name} TEXT NOT NULL, '
        strsql1 += f'{self.__email} TEXT NOT NULL, '
        strsql1 += f'{self.__password} TEXT NOT NULL, '
        strsql1 += f'{self.__appearance_id} INTEGER NOT NULL, '
        strsql1 += f'{self.__gamescore_id} INTEGER NOT NULL)'

        conn.execute(strsql1)
        print('Table User Created')

        strsql2 = f"SELECT * FROM {self.__tablename} "
        strsql2 += "INNER JOIN tblAppearance "
        strsql2 += f"ON {self.__tablename}.{self.__appearance_id} = tblAppearance.Id"

        conn.execute(strsql2)
        print('Tables User and Appearance are Joined')

        conn.commit()
        conn.close()

    def insert_user(self, name, email, password, appearance_id, gamescore_id):
        conn = sqlite3.connect('game.db')
        strsql = f"INSERT INTO {self.__tablename} ({self.__name}, {self.__email}, {self.__password}, {self.__appearance_id}, {self.__gamescore_id})"
        strsql += f"VALUES ('{name}', '{email}', '{password}', '{str(appearance_id)}', '{str(gamescore_id)}')"
        conn.execute(strsql)
        print('user added')

        conn.commit()
        conn.close()

    def check_by_email_password(self, email, password):
        conn = sqlite3.connect('game.db')
        strsql = f"SELECT * FROM {self.__tablename} WHERE {self.__email} = '{email}' AND {self.__password} = '{password}'"
        row = conn.execute(strsql).fetchone()

        if row:
            conn.commit()
            conn.close()
            return True
        conn.commit()
        conn.close()
        return False

    def get_appearance_id_by_email(self, email):
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        strsql = f"SELECT {self.__appearance_id} FROM {self.__tablename} WHERE {self.__email} = '{email}'"

        return cursor.execute(strsql).fetchone()[0]


u = tblUser()
