import live


@live.once
def test_log():
    live.log('test')
