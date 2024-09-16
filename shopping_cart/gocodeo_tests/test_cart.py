import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart_instance = Cart(user_type='regular')
        yield cart_instance

@pytest.fixture
def item():
    return Item(item_id=1, price=50.0, name='Test Item', category='Electronics')

@pytest.fixture
def mock_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

# happy_path - test_add_item_success - Test that an item is successfully added to the cart
def test_add_item_success(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 50.0, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is successfully removed from the cart
def test_remove_item_success(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.remove_item(item.item_id)
    assert cart.items == []
    mock_db.assert_called()

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully in the cart
def test_update_item_quantity_success(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.update_item_quantity(item.item_id, 5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 50.0, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_db.assert_called()

# happy_path - test_calculate_total_price_success - Test that the total price is calculated correctly
def test_calculate_total_price_success(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    total_price = cart.calculate_total_price()
    assert total_price == 100.0
    mock_db.assert_called()

# happy_path - test_list_items_success - Test that items are listed correctly
def test_list_items_success(cart, item, mock_db, capsys):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == "Item: Test Item, Quantity: 2, Price per unit: 50.0\n"
    mock_db.assert_called()

# happy_path - test_empty_cart_success - Test that the cart is emptied successfully
def test_empty_cart_success(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called()

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_db):
    cart.add_item(2, 0, 50.0, 'Zero Quantity Item', 'Misc', 'guest')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 50.0, 'name': 'Zero Quantity Item', 'category': 'Misc', 'user_type': 'guest'}]
    mock_db.assert_called_once()

# edge_case - test_remove_item_not_in_cart - Test removing an item not in the cart
def test_remove_item_not_in_cart(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.remove_item(99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 50.0, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_db.assert_called()

# edge_case - test_update_item_quantity_not_in_cart - Test updating quantity for an item not in the cart
def test_update_item_quantity_not_in_cart(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.update_item_quantity(99, 3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 50.0, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_db.assert_called()

# edge_case - test_calculate_total_price_no_items - Test calculating total price with no items in the cart
def test_calculate_total_price_no_items(cart, mock_db):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0
    mock_db.assert_not_called()

# edge_case - test_list_items_empty_cart - Test listing items when cart is empty
def test_list_items_empty_cart(cart, mock_db, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ""
    mock_db.assert_not_called()

# edge_case - test_empty_cart_already_empty - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_db):
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called()

