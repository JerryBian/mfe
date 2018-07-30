from package.sqlpackagesetting import SqlPackageSetting


class SqlPackage(object):
    def __init__(self, setting: SqlPackageSetting):
        self.__setting = setting
        self.__database = None
        self.__silent = False
        self.__files = []

    @property
    def setting(self):
        return self.__setting

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database):
        self.__database = database

    @property
    def silent(self):
        return self.__silent

    @silent.setter
    def silent(self, silent):
        self.__silent = silent

    @property
    def files(self):
        return self.__files
