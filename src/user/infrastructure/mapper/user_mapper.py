from ...application.user_dto import UserDTO
from ...domain.model.user import User


class UserMapper:

    @staticmethod
    def from_aggregate_to_dto(user: User) -> UserDTO:
        return UserDTO(
            userid=user.userid,
            email=user.email,
            password=user.password,
            username=user.username,
        )
