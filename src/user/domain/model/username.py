class Username:
    
    class BadFormedUserName(Exception):
        pass
    
    def __init__(self, username: str):
        self.__checkUsernameLength(username)
        self.__checkUsernameSpaces(username)
        self.__username: str = username

    def __checkUsernameLength(self, username: str):
        if len(username) == 0:
            raise self.BadFormedUserName("Username cannot be empty")

    def __checkUsernameSpaces(self, username: str):
        if " " in username:
            raise self.BadFormedUserName("Username cannot have white spaces")
        
    @staticmethod 
    def fromString(username: str):
        return Username(username)
    
    @property
    def value(self):
        return self.__username