
class SqlPackageSetting(object):
    def __init__(self):
        self.__host = None
        self.__user = None
        self.__password = None
        self.__root = None
        self.__date_lookup = 'default'

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, root):
        self.__root = root

    @property
    def date_lookup(self):
        return self.__date_lookup

    @date_lookup.setter
    def date_lookup(self, date_lookup):
        self.date_lookup = date_lookup