import sympy
import math
import datetime
import mysql.connector
from DataBase import db

import logging
logging.basicConfig(filename="name.log", level=logging.INFO)
data = ''

curTime = datetime.datetime.now().timestamp()
try:
    handle = open("test.txt", "r")
    for line in handle:

        if len(line) != 0:
            data = line
            print(data)
            try:
                a = sympy.simplify(data)
                print(sympy.solve(a))
                try:
                    db.DataBase.callFunction('set_uravn', str(data), str(sympy.solve(a)))
                except:
                    pass
                finally:
                    db.DataBase.callFunction('set_logs', str(sympy.solve(a)), str(data), str(curTime))
            except:
                try:
                    db.DataBase.callFunction('set_uravn', str(data), "")
                except:
                    pass
                finally:
                    db.DataBase.callFunction('set_logs', "incorrect equalition", str(data), str(curTime))
            logging.info("\nlevelname: INFO message: equation: %s result: %s" % (data, a))

except Exception as error:
    print(str(error))

handle.close()