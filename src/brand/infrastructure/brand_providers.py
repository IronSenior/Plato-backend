from dependency_injector import containers, providers
from .repository.brand_repository import BrandRepository


class BrandProviders(containers.DeclarativeContainer):

    BRANDS = providers.Singleton(BrandRepository)
