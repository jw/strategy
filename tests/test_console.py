from strategy.console import console


def test_console(capsys):
    console.print("strategy")
    captured = capsys.readouterr()
    assert captured.out == "strategy\n"
    assert captured.err == ""
