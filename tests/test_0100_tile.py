import snake


def test_creation():
    t= snake.Tile(5,10,(255,0,0))
    assert t.draw