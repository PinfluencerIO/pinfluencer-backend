from abc import ABC, abstractmethod

from src.common.object_result import ObjectResult
from src.common.result import Result
from src.contract.data_access_layer.createable_interface import CreatableInterface
from src.contract.data_access_layer.deleteable_interface import DeletableInterface
from src.contract.data_access_layer.readable_interface import ReadableInterface
from src.contract.data_access_layer.updatable_interface import UpdatableInterface
from src.domain.models.product_model import ProductModel


class ProductRepositoryInterface(CreatableInterface[ProductModel],
                                 ReadableInterface[ProductModel],
                                 UpdatableInterface[ProductModel],
                                 DeletableInterface[ProductModel],
                                 metaclass=ABC):
    @abstractmethod
    def read(self, id: str) -> ProductModel:
        pass

    @abstractmethod
    def readall(self) -> list[ProductModel]:
        pass

    @abstractmethod
    def update(self, data: ProductModel) -> Result:
        pass

    @abstractmethod
    def delete(self, id: str) -> Result:
        pass

    @abstractmethod
    def create(self, data: ProductModel) -> ObjectResult[str]:
        pass
