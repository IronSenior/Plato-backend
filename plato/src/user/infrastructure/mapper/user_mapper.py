from ...application.user_dto import UserDTO
from ...domain.model.user import User


class UserMapper:

    @staticmethod
    def from_aggregate_to_dto(user: User) -> UserDTO:
        return UserDTO(
            userId=str(user.userId),
            usermail=user.usermail,
            password=user.password,
            username=user.username,
        )
