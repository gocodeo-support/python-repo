import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        mock_cursor = mock.Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        yield {
            'connection': mock_connection,
            'cursor': mock_cursor,
            'connect': mock_connect
        }

@pytest.fixture
def mock_database_methods(mock_database_connection):
    mock_connection = mock_database_connection['connection']
    mock_cursor = mock_database_connection['cursor']

    mock_cursor.execute = mock.Mock()
    mock_cursor.fetchone = mock.Mock()
    mock_cursor.fetchall = mock.Mock()
    mock_connection.commit = mock.Mock()
    mock_connection.close = mock.Mock()

    yield {
        'execute': mock_cursor.execute,
        'fetchone': mock_cursor.fetchone,
        'fetchall': mock_cursor.fetchall,
        'commit': mock_connection.commit,
        'close': mock_connection.close
    }

# happy path - connect - Test that a connection to the database is established successfully
def test_connect_success(mock_database_connection):
    db_path = 'valid_db_path.db'
    db_conn = DatabaseConnection(db_path)
    db_conn.connect()
    mock_database_connection['connect'].assert_called_once_with(db_path)


# happy path - execute - Test that a query executes successfully without parameters
def test_execute_no_params(mock_database_methods):
    query = 'CREATE TABLE cart (id INTEGER)'
    db_conn = DatabaseConnection('valid_db_path.db')
    db_conn.connect()
    db_conn.execute(query)
    mock_database_methods['execute'].assert_called_once_with(query, [])


# happy path - execute - Test that a query executes successfully with parameters
def test_execute_with_params(mock_database_methods):
    query = 'INSERT INTO test (id) VALUES (?)'
    params = [1]
    db_conn = DatabaseConnection('valid_db_path.db')
    db_conn.connect()
    db_conn.execute(query, params)
    mock_database_methods['execute'].assert_called_once_with(query, params)


# happy path - fetchone - Test that fetchone returns the correct single record
def test_fetchone(mock_database_methods):
    query = 'SELECT id FROM test WHERE id = ?'
    params = [1]
    mock_database_methods['fetchone'].return_value = [1]
    db_conn = DatabaseConnection('valid_db_path.db')
    db_conn.connect()
    result = db_conn.fetchone(query, params)
    assert result == [1]
    mock_database_methods['fetchone'].assert_called_once_with(query, params)


# happy path - fetchall - Test that fetchall returns all records
def test_fetchall(mock_database_methods):
    query = 'SELECT id FROM test'
    mock_database_methods['fetchall'].return_value = [[1], [2], [3]]
    db_conn = DatabaseConnection('valid_db_path.db')
    db_conn.connect()
    results = db_conn.fetchall(query)
    assert results == [[1], [2], [3]]
    mock_database_methods['fetchall'].assert_called_once_with(query, [])


# happy path - close - Test that the database connection is closed successfully
def test_close_connection(mock_database_methods):
    db_conn = DatabaseConnection('valid_db_path.db')
    db_conn.connect()
    db_conn.close()
    mock_database_methods['close'].assert_called_once()


# edge case - execute - Test that executing a query on a closed connection raises an error
def test_execute_closed_connection(mock_database_methods):
    query = 'SELECT * FROM test'
    mock_database_methods['execute'].side_effect = sqlite3.OperationalError
    db_conn = DatabaseConnection('valid_db_path.db')
    with pytest.raises(sqlite3.OperationalError):
        db_conn.execute(query)


# edge case - fetchone - Test that fetchone on an empty table returns None
def test_fetchone_empty_table(mock_database_methods):
    query = 'SELECT * FROM test WHERE id = ?'
    params = [999]
    mock_database_methods['fetchone'].return_value = None
    db_conn = DatabaseConnection('valid_db_path.db')
    db_conn.connect()
    result = db_conn.fetchone(query, params)
    assert result is None
    mock_database_methods['fetchone'].assert_called_once_with(query, params)


# edge case - fetchall - Test that fetchall on an empty table returns an empty list
def test_fetchall_empty_table(mock_database_methods):
    query = 'SELECT * FROM test'
    mock_database_methods['fetchall'].return_value = []
    db_conn = DatabaseConnection('valid_db_path.db')
    db_conn.connect()
    results = db_conn.fetchall(query)
    assert results == []
    mock_database_methods['fetchall'].assert_called_once_with(query, [])


# edge case - commit - Test that commit on a closed connection raises an error
def test_commit_closed_connection(mock_database_methods):
    mock_database_methods['commit'].side_effect = sqlite3.OperationalError
    db_conn = DatabaseConnection('valid_db_path.db')
    with pytest.raises(sqlite3.OperationalError):
        db_conn.commit()


# edge case - connect - Test that connecting with an invalid path raises an error
def test_connect_invalid_path(mock_database_connection):
    db_path = 'invalid_path.db'
    mock_database_connection['connect'].side_effect = sqlite3.OperationalError
    db_conn = DatabaseConnection(db_path)
    with pytest.raises(sqlite3.OperationalError):
        db_conn.connect()


# edge case - add_item_to_cart_db - Test that adding an item to cart with invalid SQL raises an error
def test_add_item_invalid_sql(mock_database_methods):
    query = 'INSERT INTO invalid_table VALUES (?)'
    params = [1]
    mock_database_methods['execute'].side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        add_item_to_cart_db(query, params)


