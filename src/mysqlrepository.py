from package.sqlpackage import SqlPackage
from mysql.connector.connection import MySQLConnection


class MySqlRepository(object):
    @staticmethod
    def execute(sqlPackage: SqlPackage, sql: str):
        cnx: MySQLConnection = MySQLConnection(user=sqlPackage.setting.user, password=sqlPackage.setting.password,
                                               host=sqlPackage.setting.host,
                                               database=sqlPackage.database)

        cursor = cnx.cursor()
        for result in cursor.execute(sql, multi=True):
            pass

        cnx.commit()
        cursor.close()
        cnx.close()
