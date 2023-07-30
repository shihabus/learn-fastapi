import pytest
from app.bank_account import BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 55


@pytest.mark.parametrize(
    "deposited,withdrawn,expected",
    [
        (200, 100, 100),
        (1200, 200, 1000),
    ],
)
def test_bank_transaction(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected


def test_insufficient_fund(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
