from dependency_injector import containers, providers
from .repository.brand_repository import BrandRepository
from .read_model.get_brand_service import GetBrandMongoService


class BrandProviders(containers.DeclarativeContainer):

    BRANDS = providers.Factory(BrandRepository)
    GET_BRAND_SERVICE = providers.Factory(GetBrandMongoService)
