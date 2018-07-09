from threading import Lock
import mysql.connector



class _DataBase:
    def __connect(self):
#создание подключения к бд
        self.__db = mysql.connector.connect(host='localhost', database='tmp',
                                           user='root', password='')
        if self.__db.is_connected():
            self.__cursor = self.__db.cursor()

    def __init__(self):
        self.__connect()
#создание мьютекса
        self.__mutex = Lock()
#этого на паре не было, новый способ обращения к хранимым процедурам

#свойство, которое возвращает набор хранимок
    @property
    def Functions(self):
        return self.__functions

#### этого небыло на паре
    def decorate(self):
        def getFuncDecorator(storedFunction):
            def callProcedure(*args):
                self.__mutex.acquire()
                result = None
                try:

                    if not (self.__db.is_connected()):
                        self.__connect()

                    self.__cursor.callproc(storedFunction.__name__, args)
                    result = []

                    for item in self.__cursor.stored_results():
                        for item2 in item.fetchall():
                            result.append(item2)

                    self.__db.commit()

                finally:
                    self.__mutex.release()
                return result

            return callProcedure

        return getFuncDecorator
######

#функция, котороя принимает название хранимой процедуры и аргументы, которые она принимает
    def callFunction(self, nameFunction: str, *args):
#блокировка мьютекса
        self.__mutex.acquire()
        result = None
        try:
#проверка подключения, если не подключены, то востанавливаем соединение
            if not (self.__db.is_connected()):
                self.__connect()
#вызов хранимой процедуры
            self.__cursor.callproc(nameFunction, args)
            result = []
#получение результата вызова хранимой процедуры
            for item in self.__cursor.stored_results():
                for item2 in item.fetchall():
                    result.append(item2)
#коммит необходим, если мы добовляем что-то в бд, чтобы сохранить изменения
            self.__db.commit()

        finally:
#разблокирование мьютекса
            self.__mutex.release()
        return result


DataBase = _DataBase()