from commandbus import Command

class CreateUserCommand(Command):
    
    def __init__(self, userid: str, username: str,
                 usermail: str, password: str):
        self.__userId: str = userid
        self.__username: str = username
        self.__userMail: str = usermail
        self.__password: str = password
        
    @property
    def userId(self):
        return self.__userId
    
    @property
    def username(self):
        return self.__username
    
    @property
    def userMail(self):
        return self.__userMail

    @property
    def password(self):
        return self.__password
