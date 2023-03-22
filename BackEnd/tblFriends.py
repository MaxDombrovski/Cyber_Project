import sqlite3


class tblFriends(object):
    def __init__(self, tablename="tblFriends", id="Id", user_id1="User_Id1", user_id2="User_Id2"):
        self.__tablename = tablename
        self.__id = id
        self.__user_id1 = user_id1
        self.__user_id2 = user_id2

        conn = sqlite3.connect('game.db')
        strsql = f"CREATE TABLE IF NOT EXISTS {self.__tablename} ({self.__id} INTEGER PRIMARY KEY AUTOINCREMENT, "
        strsql += f"{self.__user_id1} INTEGER, "
        strsql += f"{self.__user_id2} INTEGER)"

        conn.execute(strsql)
        print("Table friends created")
        conn.commit()
        conn.close()

    def insert_friends(self, user1, user2):
        conn = sqlite3.connect('game.db')
        strsql = f"INSERT INTO {self.__tablename} ({self.__user_id1}, {self.__user_id2})"
        strsql += f"VALUES ('{str(user1)}', '{str(user2)}')"
        conn.execute(strsql)
        print('friends added')

        conn.commit()
        conn.close()


u = tblFriends()
