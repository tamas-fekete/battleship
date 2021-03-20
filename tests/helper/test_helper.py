from helper import helper as hl

def test1_stringToCoordinate():
    assert hl.stringToCoordinate("b3") == 12

def test2_stringToCoordinate():
    assert hl.stringToCoordinate("a1") == 0