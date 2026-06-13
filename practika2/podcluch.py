from psycopg2 import connect,Error

class Connection:
    def __init__(self):
        self.con = None
        self.cur = None

        try:
            self.con = connect(
                host = 'localhost',
                user = 'postgres',
                password = 'postgres',
                dbname = 'uchet_sotrudnikov',
                port = '5433'
            )
            print('Подключение установлено')
            self.cur = self.con.cursor()
        except Error as e:
            print('Ошибка соединения')
            print(e)