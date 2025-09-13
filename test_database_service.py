#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pytest", "approvaltests"]
# ///

from parrot import verify_parrot, parrot
from database_service import DatabaseConnection, UserService
from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions
from unittest.mock import patch


def test_database_query_with_verify_parrot():
    """
    First, we record the DatabaseConnection.query method's behavior
    using verify_parrot. This creates our approved test double.
    """
    
    # Create a connected instance for testing
    db = DatabaseConnection("localhost", 5432, "admin", "secret123")
    db.connected = True  # Bypass actual connection for testing
    
    # Record various query behaviors
    verify_parrot(db.query, [
        ["SELECT * FROM users"],
        ["SELECT COUNT(*) FROM users"],
        ["SELECT * FROM products"],  # Empty result
        ["DROP TABLE users"],  # Error case
    ])


def test_user_service_with_parrot_stubbing_init():
    """
    Now we test UserService methods using the parrot as a test double.
    We stub the DatabaseConnection.__init__ to avoid real initialization,
    and use the parrot for the query method.
    """
    
    # Create a dummy instance to get the query method
    dummy_db = DatabaseConnection("", 0, "", "")
    dummy_db.connected = True
    
    # Stub __init__ to do nothing and connect to return True
    with patch.object(DatabaseConnection, '__init__', return_value=None):
        with patch.object(DatabaseConnection, 'connect', return_value=True):
            with parrot(dummy_db.query):
                # Now test UserService which creates DatabaseConnection internally
                service = UserService()
                
                # Test get_all_users
                users = service.get_all_users()
                assert users == [
                    {"id": 1, "name": "Alice"},
                    {"id": 2, "name": "Bob"}
                ]
                
                # Test get_user_count
                count = service.get_user_count()
                assert count == 2
                
                # Test dangerous_operation (should raise an error)
                try:
                    service.dangerous_operation()
                    assert False, "Should have raised an error"
                except Exception as e:
                    assert "DROP operations not allowed" in str(e)


def test_user_service_with_approval_testing():
    """
    Alternative approach: approval test the entire UserService behavior
    while using parrots for dependencies.
    """
    
    # Create a dummy instance to get the query method
    dummy_db = DatabaseConnection("", 0, "", "")
    dummy_db.connected = True
    
    with patch.object(DatabaseConnection, '__init__', return_value=None):
        with patch.object(DatabaseConnection, 'connect', return_value=True):
            with parrot(dummy_db.query):
                service = UserService()
                
                results = []
                
                # Test various operations
                results.append(f"All users: {service.get_all_users()}")
                results.append(f"User count: {service.get_user_count()}")
                
                try:
                    service.dangerous_operation()
                    results.append("Dangerous operation: succeeded")
                except Exception as e:
                    results.append(f"Dangerous operation: {e}")
                
                # Verify all results
                verify("\n".join(results), options=Options().inline(InlineOptions.automatic()))


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])