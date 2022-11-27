from deeper import sum_as_string

def test_main():
    result = sum_as_string(2, 2)
    print(result)
    assert result == '4'