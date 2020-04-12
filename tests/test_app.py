from .context import tableocr


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    tableocr.TableOcr.run()
    captured = capsys.readouterr()

    assert "Hello World..." in captured.out
