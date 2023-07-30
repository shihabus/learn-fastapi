from app.bank_account import BankAccount


def test_bank_set_initial_amount():
    bank_account = BankAccount(20)
    assert bank_account.balance == 20


def test_bank_default_initial_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0


def test_deposit():
    bank_account = BankAccount(20)
    bank_account.deposit(20)
    assert bank_account.balance == 40


def test_withdraw():
    bank_account = BankAccount(20)
    bank_account.withdraw(20)
    assert bank_account.balance == 0


def test_collect_interest():
    bank_account = BankAccount(20)
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 22.0
