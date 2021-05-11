from ...domain.repository.brands import Brands
from ...domain.model.brand_id import BrandId
from ...domain.model.brand_name import BrandName
from ...domain.model.brand import Brand
from ...domain.model.brand_image import BrandImageUrl
from ....shared.domain.user_id import UserId
from ...domain.exceptions.brand_id_aready_registered import BrandIdAlreadyRegistered
from .create_brand_command import CreateBrandCommand
from commandbus import CommandHandler
from dependency_injector.wiring import inject, Provide


class CreateBrandHandler(CommandHandler):

    @inject
    def __init__(self, brands: Brands = Provide["BRANDS"]):
        self.brands: Brands = brands

    def handle(self, cmd: CreateBrandCommand):
        brandId = BrandId.fromString(cmd.id)
        if (type(self.brands.getById(brandId)) == Brand):
            raise BrandIdAlreadyRegistered("Brand Id already registered")

        brand = Brand.add(
            id=brandId,
            userId=UserId.fromString(cmd.userId),
            name=BrandName.fromString(cmd.name),
            image=BrandImageUrl.fromString(cmd.image)
        )
        self.brands.save(brand)
