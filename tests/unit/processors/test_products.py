import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters import FilterResponse, FilterInterface
from src.filters.valid_id_filters import LoadResourceById
from src.processors.products import ProcessPublicProducts, ProcessPublicGetProductBy, ProcessAuthenticatedGetProducts, \
    ProcessAuthenticatedGetProductById, ProcessAuthenticatedPostProduct, ProcessAuthenticatedPutProduct, \
    ProcessAuthenticatedDeleteProduct
from tests.unit import StubDataManager


def test_load_all_products_response_200():
    processor = ProcessPublicProducts(StubDataManager())
    processor.load_all_products = mock_response_from_db

    pinfluencer_response = processor.do_process({})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) is list


# @patch('src.filters.valid_id_filters.load_by_id')
def test_process_successful_public_get_product_by_id():
    load_resource = LoadResourceById(StubDataManager(), 'product')
    uuid_ = uuid.uuid4()
    processor = ProcessPublicGetProductBy(load_resource, StubDataManager())
    processor.load_product_from_cmd = mock_load_product
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'product_id': str(uuid_)}})
    assert pinfluencer_response.is_ok() is True


def test_process_unsuccessful_public_get_brand_by_id():
    load_resource = LoadResourceById(StubDataManager(), 'product')
    uuid_ = uuid.uuid4()
    processor = ProcessPublicGetProductBy(load_resource, StubDataManager())
    processor.load_product_from_cmd = mock_load_product_failed
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'product_id': str(uuid_)}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_authenticated_products():
    processor = ProcessAuthenticatedGetProducts(MockBrandAssociatedWithCognitoUser(),
                                                mock_by_id,
                                                StubDataManager())
    pinfluencer_response = processor.do_process({})
    assert pinfluencer_response.is_ok() is True


def test_process_authenticated_products_authentication_failed():
    processor = ProcessAuthenticatedGetProducts(MockBrandAssociatedWithCognitoUser(failed=True),
                                                mock_by_id,
                                                StubDataManager())
    pinfluencer_response = processor.do_process({})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 401


def test_process_authenticated_product_by_id():
    processor = ProcessAuthenticatedGetProductById(MockBrandAssociatedWithCognitoUser(),
                                                   mock_load_product_by_id_for_brand,
                                                   StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'product_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is True


def test_process_authenticated_product_by_id_failed_authentication():
    processor = ProcessAuthenticatedGetProductById(MockBrandAssociatedWithCognitoUser(failed=True),
                                                   mock_load_product_by_id_for_brand,
                                                   StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'product_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 401


def test_process_authenticated_product_by_id_404_not_found():
    processor = ProcessAuthenticatedGetProductById(MockBrandAssociatedWithCognitoUser(),
                                                   mock_not_found_product_by_id_for_brand,
                                                   StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'product_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_process_post_product():
    process = ProcessAuthenticatedPostProduct(MockBrandAssociatedWithCognitoUser(), MockValidation(),
                                              mock_write_new_product, StubDataManager())
    pinfluencer_response = process.do_process({})
    assert pinfluencer_response.is_ok() is True


def test_process_post_product_failed_authentication():
    process = ProcessAuthenticatedPostProduct(MockBrandAssociatedWithCognitoUser(failed=True),
                                              MockValidation(),
                                              mock_write_new_product, StubDataManager())
    pinfluencer_response = process.do_process({})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 401


def test_process_post_product_failed_validation():
    process = ProcessAuthenticatedPostProduct(MockBrandAssociatedWithCognitoUser(),
                                              MockValidation(failed=True),
                                              mock_write_new_product, StubDataManager())
    pinfluencer_response = process.do_process({})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_put_product():
    process = ProcessAuthenticatedPutProduct(MockBrandAssociatedWithCognitoUser(),
                                             MockValidation(),
                                             mock_update_product,
                                             StubDataManager())

    pinfluencer_response = process.do_process({'pathParameters': {'product_id': str(uuid.uuid4())},
                                               'body': ' {"name": "The DOM DOM product Ebert and Sons",'
                                                       '"description": "A description of the Mozambique Tasty",'
                                                       '"requirements": "deposit,Practical,transmitter,Specialist"}'})
    assert pinfluencer_response.is_ok() is True


def test_process_put_product_failed_authentication():
    process = ProcessAuthenticatedPutProduct(MockBrandAssociatedWithCognitoUser(failed=True),
                                             MockValidation(),
                                             mock_update_product,
                                             StubDataManager())

    pinfluencer_response = process.do_process({'pathParameters': {'product_id': str(uuid.uuid4())},
                                               'body': ' {"name": "The DOM DOM product Ebert and Sons",'
                                                       '"description": "A description of the Mozambique Tasty",'
                                                       '"requirements": "deposit,Practical,transmitter,Specialist"}'})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 401


def test_process_put_product_failed_validation():
    process = ProcessAuthenticatedPutProduct(MockBrandAssociatedWithCognitoUser(),
                                             MockValidation(failed=True),
                                             mock_update_product,
                                             StubDataManager())

    pinfluencer_response = process.do_process({'pathParameters': {'product_id': str(uuid.uuid4())},
                                               'body': ' {"name": "The DOM DOM product Ebert and Sons",'
                                                       '"description": "A description of the Mozambique Tasty",'
                                                       '"requirements": "deposit,Practical,transmitter,Specialist"}'})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_delete_product():
    process = ProcessAuthenticatedDeleteProduct(MockBrandAssociatedWithCognitoUser(),
                                                mock_delete_product,
                                                StubDataManager())

    pinfluencer_response = process.do_process({'pathParameters': {'product_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is True


def test_process_delete_product_failed_authentication():
    process = ProcessAuthenticatedDeleteProduct(MockBrandAssociatedWithCognitoUser(failed=True),
                                                mock_delete_product,
                                                StubDataManager())

    pinfluencer_response = process.do_process({'pathParameters': {'product_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 401


class MockValidation(FilterInterface):
    def __init__(self, failed=False) -> None:
        super().__init__()
        self.failed = failed

    def do_filter(self, event: dict) -> FilterResponse:
        if self.failed:
            return FilterResponse('', 400, {})
        else:
            return FilterResponse('', 200, mock_response_from_db()[0].as_dict())


class MockBrandAssociatedWithCognitoUser(FilterInterface):

    def __init__(self, failed=False) -> None:
        super().__init__()
        self.failed = failed

    def do_filter(self, event: dict) -> FilterResponse:
        if self.failed:
            return FilterResponse('', 401, {})
        else:
            return FilterResponse('', 200, Brand().as_dict())


def mock_load_product(event):
    return FilterResponse('', 200, mock_response_from_db()[0])


def mock_delete_product(brand_id, product_id, data_manager):
    return FilterResponse('', 200, mock_response_from_db()[0])


def mock_load_product_failed(event):
    return FilterResponse('', 400, {})


def mock_load_product_by_id_for_brand(product_id, brand, data_manager):
    product = Product()
    brand = Brand()
    brand.id = str(uuid.uuid4())
    product.brand = brand
    return product


def mock_not_found_product_by_id_for_brand(product_id, brand, data_manager):
    return None


def mock_write_new_product(payload, brand_id, data_manager):
    return mock_response_from_db()[0]


def mock_update_product(brand_id, product_id, payload, data_manager):
    return mock_response_from_db()[0]


def mock_by_id(id, data_manager):
    return mock_response_from_db()


def mock_response_from_db():
    brand = Brand()
    product1 = Product()
    product1.brand = brand
    product2 = Product()
    product2.brand = brand
    return [product1, product2]
