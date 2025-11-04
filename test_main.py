from main import adder

def test_answer_pos():
    assert adder(3) == 4

def test_answer_neg():
    assert adder(-1) == 0