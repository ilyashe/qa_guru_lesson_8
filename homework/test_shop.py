"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1000)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(500)
        assert product.check_quantity(500)
        assert not product.check_quantity(501)

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError, match="Недостаточно товара в наличии"):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_add_product(self, product, cart):
        cart.add_product(product, 50)
        assert cart.products[product] == 50

        cart.add_product(product, 3)
        assert cart.products[product] == 53

    def test_cart_remove_product(self, product, cart):
        # remove_count < buy_count
        cart.add_product(product, 50)
        cart.remove_product(product, 20)
        assert cart.products[product] == 30

        # Без указания remove_count
        cart.remove_product(product)
        assert not cart.products

        # remove_count > buy_count
        cart.add_product(product, 3)
        cart.remove_product(product, 20)
        assert not cart.products

    def test_cart_clear(self, product, cart):
        cart.add_product(product, 50)
        cart.clear()
        assert not cart.products

    def test_cart_get_total_price(self, product, cart):
        cart.add_product(product, 5)
        assert cart.get_total_price() == 500

    def test_cart_buy(self, product, cart):
        cart.add_product(product, 5)
        cart.buy()
        assert product.check_quantity(995)
        assert not cart.products

    def test_cart_buy_more_than_available(self, product, cart):
        cart.add_product(product, 1005)
        with pytest.raises(ValueError):
            cart.buy()
        assert product.check_quantity(1000)
        assert cart.products[product] == 1005
