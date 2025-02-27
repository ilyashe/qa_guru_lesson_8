"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product_book() -> Product:
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_toy() -> Product:
    return Product("toy", 1000, "This is a toy", 100)


@pytest.fixture
def cart() -> Cart:
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_equal(self, product_book):
        # TODO напишите проверки на метод check_quantity
        assert product_book.check_quantity(product_book.quantity)

    def test_product_check_quantity_more(self, product_book):
        # TODO напишите проверки на метод check_quantity
        assert not product_book.check_quantity(product_book.quantity + 1)

    def test_product_buy(self, product_book):
        # TODO напишите проверки на метод buy
        quantity_before = product_book.quantity
        buy_amount = 500
        product_book.buy(buy_amount)
        assert product_book.quantity == quantity_before - buy_amount

    def test_product_buy_more_than_available(self, product_book):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError, match='Недостаточно товара в наличии'):
            product_book.buy(product_book.quantity + 1)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_add_product_once(self, product_book, cart):
        buy_count = 50
        cart.add_product(product_book, buy_count)
        assert cart.products[product_book] == buy_count

    def test_cart_add_product_twice(self, product_book, cart):
        buy_count_1 = 50
        buy_count_2 = 3
        cart.add_product(product_book, buy_count_1)
        assert cart.products[product_book] == buy_count_1
        cart.add_product(product_book, buy_count_2)
        assert cart.products[product_book] == buy_count_1 + buy_count_2

    def test_cart_add_zero_product_(self, product_book, cart):
        buy_count = 0
        cart.add_product(product_book, buy_count)
        assert not cart.products

    def test_cart_add_two_products(self, product_book, product_toy, cart):
        buy_count_book = 50
        buy_count_toy = 40
        cart.add_product(product_book, buy_count_book)
        cart.add_product(product_toy, buy_count_toy)
        assert cart.products[product_book] == buy_count_book
        assert cart.products[product_toy] == buy_count_toy

    def test_cart_remove_product_with_remove_count_less(self, product_book, cart):
        buy_count = 50
        remove_count = buy_count - 1
        cart.add_product(product_book, buy_count)
        cart.remove_product(product_book, remove_count)
        assert cart.products[product_book] == buy_count - remove_count

    def test_cart_remove_product_without_remove_count(self, product_book, cart):
        buy_count = 50
        cart.add_product(product_book, buy_count)
        cart.remove_product(product_book)
        assert not cart.products

    def test_cart_remove_product_with_remove_count_over(self, product_book, cart):
        buy_count = 50
        cart.add_product(product_book, buy_count)
        cart.remove_product(product_book, buy_count + 1)
        assert not cart.products

    def test_cart_remove_one_of_two_products(self, product_book, product_toy, cart):
        buy_count = 50
        cart.add_product(product_book, buy_count)
        cart.add_product(product_toy, buy_count)
        cart.remove_product(product_book)
        assert product_book not in cart.products
        assert cart.products[product_toy] == buy_count

    def test_cart_remove_absent_product(self, product_book, product_toy, cart):
        buy_count = 50
        cart.add_product(product_toy, buy_count)
        cart.remove_product(product_book)
        assert product_book not in cart.products
        assert cart.products[product_toy] == buy_count

    def test_cart_remove_product_from_empty_card(self, product_book, cart):
        cart.remove_product(product_book)
        assert not cart.products

    def test_cart_clear(self, product_book, cart):
        buy_count = 50
        cart.add_product(product_book, buy_count)
        cart.clear()
        assert not cart.products

    def test_cart_empty_clear(self, product_book, cart):
        cart.clear()
        assert not cart.products

    def test_cart_get_total_price_one_product(self, product_book, cart):
        buy_count = 5
        cart.add_product(product_book, buy_count)
        assert cart.get_total_price() == product_book.price * buy_count

    def test_cart_get_total_price_two_products(self, product_book, product_toy, cart):
        buy_count_book = 5
        buy_count_toy = 10
        cart.add_product(product_book, buy_count_book)
        cart.add_product(product_toy, buy_count_toy)
        assert cart.get_total_price() == product_book.price * buy_count_book + product_toy.price * buy_count_toy

    def test_cart_get_total_price_empty(self, cart):
        assert cart.get_total_price() == 0

    def test_cart_buy(self, product_book, cart):
        buy_count = 5
        quantity_before = product_book.quantity
        cart.add_product(product_book, buy_count)
        cart.buy()
        assert product_book.quantity == quantity_before - buy_count
        assert not cart.products

    def test_cart_buy_two_products(self, product_book, product_toy, cart):
        buy_count = 5
        quantity_before_book = product_book.quantity
        quantity_before_toy = product_toy.quantity
        cart.add_product(product_book, buy_count)
        cart.add_product(product_toy, buy_count)
        cart.buy()
        assert product_book.quantity == quantity_before_book - buy_count
        assert product_toy.quantity == quantity_before_toy - buy_count
        assert not cart.products

    def test_cart_buy_more_than_available(self, product_book, cart):
        buy_count = product_book.quantity + 1
        quantity_before = product_book.quantity
        cart.add_product(product_book, buy_count)
        with pytest.raises(ValueError):
            cart.buy()
        assert product_book.quantity == quantity_before
        assert cart.products[product_book] == buy_count

    def test_cart_buy_more_than_available_one_of_two_products(self, product_book, product_toy, cart):
        buy_count_toy = product_toy.quantity + 1
        quantity_before_toy = product_toy.quantity
        quantity_before_book = product_book.quantity
        buy_count_book = 5
        cart.add_product(product_book, buy_count_book)
        cart.add_product(product_toy, buy_count_toy)
        with pytest.raises(ValueError):
            cart.buy()
        assert product_toy.quantity == quantity_before_toy
        assert product_book.quantity == quantity_before_book
        assert cart.products[product_toy] == buy_count_toy
        assert cart.products[product_book] == buy_count_book

    def test_cart_buy_empty(self, cart):
        with pytest.raises(ValueError, match='Корзина пустая'):
            cart.buy()
