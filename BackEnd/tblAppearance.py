import sqlite3


class tblAppearance(object):
    def __init__(self,
                 tablename="tblAppearance", id="Id", hat="Hat", shirt="Shirt", pants="Pants",
                 shoes="Shoes", accessories="Accessories"):
        self.__tablename = tablename
        self.__id = id
        self.__hat = hat
        self.__shirt = shirt
        self.__pants = pants
        self.__shoes = shoes
        self.__accessories = accessories

        conn = sqlite3.connect('game.db')
        strsql = f'CREATE TABLE IF NOT EXISTS {self.__tablename} ({self.__id} INTEGER PRIMARY KEY AUTOINCREMENT, '
        strsql += f'{self.__hat} TEXT NOT NULL, '
        strsql += f'{self.__shirt} TEXT NOT NULL, '
        strsql += f'{self.__pants} TEXT NOT NULL, '
        strsql += f'{self.__shoes} TEXT NOT NULL, '
        strsql += f'{self.__accessories} TEXT NOT NULL)'

        conn.execute(strsql)
        print('Table Appearance Created')
        conn.commit()
        conn.close()

    # Function returns id of an inserted row. If it doesn't exist, function creates a new row and returns the last id
    def give_id_to_player(self, hat, shirt, pants, shoes, accessories):
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        strsql = f"SELECT * FROM {self.__tablename} WHERE {self.__hat} = '{hat}' AND {self.__shirt} = '{shirt}'"
        strsql += f"AND {self.__pants} = '{pants}' AND {self.__shoes} = '{shoes}' AND {self.__accessories} = '{accessories}'"
        row = cursor.execute(strsql).fetchone()

        if row:
            strsql = f"SELECT {self.__id} FROM {self.__tablename} WHERE {self.__hat} = '{hat}' AND {self.__shirt} = '{shirt}'"
            strsql += f"AND {self.__pants} = '{pants}' AND {self.__shoes} = '{shoes}' AND {self.__accessories} = '{accessories}'"
            cursor.execute(strsql)
            id = cursor.fetchone()[0]

            conn.commit()
            conn.close()
            return id
        self.insert_appearance(hat, shirt, pants, shoes, accessories)
        conn.commit()
        conn.close()
        return self.newid

    def insert_appearance(self, hat, shirt, pants, shoes, accessories):
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        strsql = f"INSERT INTO {self.__tablename} ({self.__hat}, {self.__shirt}, {self.__pants}, {self.__shoes}, {self.__accessories})"
        strsql += f"VALUES ('{hat}', '{shirt}', '{pants}', '{shoes}', '{accessories}')"
        cursor.execute(strsql)
        # grabs the id of inserted row (has to be placed here)
        self.newid = cursor.lastrowid

        print('appearance added')

        conn.commit()
        conn.close()

    def get_items_by_id(self, id):
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        strsql = f"SELECT * FROM {self.__tablename} WHERE {self.__id} = '{id}'"

        return cursor.execute(strsql).fetchone()

    def get_tablename(self):
        return self.__tablename


u = tblAppearance()
