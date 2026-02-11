
import string
import random
try:
    from bank import Bank
except ImportError:
    # potential issue with streamlit import if not in streamlit env
    # Mocking streamlit to allow import
    import sys
    from unittest.mock import MagicMock
    sys.modules["streamlit"] = MagicMock()
    from bank import Bank

def test_account_generation():
    ids = set()
    for _ in range(100):
        acc_id = Bank.generate_account_number()
        assert len(acc_id) == 8, f"Length mistmatch: {len(acc_id)}"
        assert all(c in string.ascii_uppercase + string.digits for c in acc_id), f"Invalid char in {acc_id}"
        ids.add(acc_id)
    
    print(f"Generated {len(ids)} unique IDs successfully.")

if __name__ == "__main__":
    test_account_generation()
