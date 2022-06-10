import pytest
from app.calculations import *


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,1,8),
    (12,4,16)
])
def test_add(num1, num2, expected):
    print("Testing Add Function")
    assert add(num1,num2) == expected


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_account(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance  == 30

def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance  == 70

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,6)  == 55

@pytest.mark.parametrize("deposit, withdraw, expected",[
    (100,50,50),
    (123,23,100),
    (43,25,18)
])
def test_transcations(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(100)

