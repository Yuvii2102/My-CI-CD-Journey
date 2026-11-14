from app import add

def test_add():
    assert add(10, 20) == 30

def test_add_negative():
    assert add(-5, -5) == -10

def test_add_zero():
    assert add(10, 0) == 10
