from enum import Enum


class SocialNetwork(Enum):

    twitter = "twitter"
    linkedin = "linkedin"

    @staticmethod
    def fromString(socialNetwork: str):
        return SocialNetwork(socialNetwork)
