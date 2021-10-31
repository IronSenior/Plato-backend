from pathlib import Path
from mimetypes import guess_extension
import uuid
from typing import BinaryIO

IMAGE_SERVER_PATH = Path("/Users/jose/plato/plato/static/images/")


def saveMedia(media: BinaryIO) -> str:
    filePath = IMAGE_SERVER_PATH.joinpath(f"{uuid.uuid4()}.{guess_extension(media.name)}")
    media.save(filePath)
    return str(filePath)
