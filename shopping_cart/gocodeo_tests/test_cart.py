

# happy path - add_item - Test that item is added to the cart successfully with valid inputs
def test_add_item_success(mocker):
    mock_add_item_to_cart_db = mocker.patch('shopping_cart.database.add_item_to_cart_db')
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# happy path - remove_item - Test that item is removed from the cart successfully
def test_remove_item_success(mocker):
    mock_add_item_to_cart_db = mocker.patch('shopping_cart.database.add_item_to_cart_db')
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that item quantity is updated successfully
def test_update_item_quantity(mocker):
    mock_add_item_to_cart_db = mocker.patch('shopping_cart.database.add_item_to_cart_db')
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price(mocker):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0


# happy path - empty_cart - Test that cart is emptied successfully
def test_empty_cart(mocker):
    mock_add_item_to_cart_db = mocker.patch('shopping_cart.database.add_item_to_cart_db')
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


# edge case - add_item - Test that adding item with zero quantity does not add item
def test_add_item_zero_quantity(mocker):
    mock_add_item_to_cart_db = mocker.patch('shopping_cart.database.add_item_to_cart_db')
    cart = Cart(user_type='regular')
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()


# edge case - remove_item - Test that removing non-existent item does not affect cart
def test_remove_non_existent_item(mocker):
    mock_add_item_to_cart_db = mocker.patch('shopping_cart.database.add_item_to_cart_db')
    cart = Cart(user_type='regular')
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 99")


# edge case - update_item_quantity - Test that updating quantity of non-existent item does not affect cart
def test_update_quantity_non_existent_item(mocker):
    mock_add_item_to_cart_db = mocker.patch('shopping_cart.database.add_item_to_cart_db')
    cart = Cart(user_type='regular')
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 3 WHERE item_id = 99")


# edge case - calculate_total_price - Test that calculate total price on empty cart returns zero
def test_calculate_total_price_empty_cart(mocker):
    cart = Cart(user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - empty_cart - Test that emptying an already empty cart does not cause errors
def test_empty_already_empty_cart(mocker):
    mock_add_item_to_cart_db = mocker.patch('shopping_cart.database.add_item_to_cart_db')
    cart = Cart(user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


# edge case - add_item - Test that adding an item with 0 quantity raises an error
def test_add_item_zero_quantity_error(mocker):
    cart = Cart(user_type='guest')
    with pytest.raises(ValueError, match='Quantity must be greater than zero'):
        cart.add_item(item_id=3, quantity=0, price=20.0, name='Orange', category='Citrus', user_type='guest')


