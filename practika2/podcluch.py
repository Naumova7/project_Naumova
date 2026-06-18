from psycopg2 import connect,Error

class Connection:
    def __init__(self):
        self.con = None
        self.cur = None

        try:
            self.con = connect(
                host = 'localhost',
                user = 'postgres',
                password = 'Na221107',
                dbname = 'uchet_sotrudnikov',
                port = '5432'
            )
            self.con.autocommit = True
            print('Подключение установлено')
            self.cur = self.con.cursor()
        except Error as e:
            print('Ошибка соединения')
            print(e)

