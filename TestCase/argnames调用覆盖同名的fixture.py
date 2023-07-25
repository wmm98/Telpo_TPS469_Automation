import pytest


@pytest.fixture()
def expected():
    return 2


@pytest.fixture()
def input():
    return 0


# Scenario1
@pytest.mark.parametrize('input', [(1)])
def test_sample(input, expected):
    print("\n")
    print("input的值是***" + str(input))
    print("expected的值是**" + str(expected))


# Scenario2
# argvalues参数来源于Excel文件
def read_excel():
    # 从数据库或者文件中读取设备的信息，这里简化为一个列表
    for dev in [1, 2, 4]:
        yield dev


@pytest.mark.parametrize('dev', read_excel())
def test_sample(dev):
    print("********* dev:" + str(dev))
    return dev



