
"""
INTO ABOUT assert : ketika assert pengembalikan nilai False maka akan error(testing ada yg salah/bug), tp jika True maka func yg diuji dianggap 
berhsl. misal assert 1==1 akan True tp ketika assert 1 == 2 akan error

1. kita import dulu class, func yg akan di uji (unit test)
2. buat skenario (bisa menggunakan pola table testing) sesuai dg logic yg dibangun pd controller
3. uji nilainya dg assert (untuk kasus yg equal atau ==)
4. run pengujian dg perintah "pytest" atau pytest -v
"""
import pytest
from app.calculations import add, BankAccount, insufficientFunds
# test biasa
# def test_add():
#     assert add(5, 3) == 8
# kita ingin menjalankan test dengan input yg berbeda" caranya dg decorator brkt
@pytest.mark.parametrize("num1, num2, expected",[
    # artinya 3 + 1 = 4
    (3, 1, 4),
    (4, 6, 10)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected
'''
# CARA 1 : INPUT SATU SATU
# uang awal 50
def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50
# uang awal 0 (nilai default)
def test_bank_default_amount():
    zero_bank_account = BankAccount()
    assert zero_bank_account.balance == 0
# ambil uang/transfer 20
def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    # menabung/uang masuk 20, tabungan awal 50
def test_deposite():
    bank_account = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70
# dpt keuntungan bunga, tabungan awal 50
def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    # bulatkan dg round
    assert round(bank_account.balance,6) == 55
'''
# CARA 2 : 
# set uang tabungan 0
@pytest.fixture
def zero_bank_account():
    print("set 0")
    return BankAccount()

# set uang awal ditabungan 50
@pytest.fixture
def bank_account():
    return BankAccount(50)

# uang awal 50
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50
# uang awal 0 (nilai default)
def test_bank_default_amount(zero_bank_account):
    print("konsumsi")
    assert zero_bank_account.balance == 0
# ambil uang/transfer 20
def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    # menabung/uang masuk 20, tabungan awal 50
def test_deposite(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70
# dpt keuntungan bunga, tabungan awal 50
def test_collect_interest(bank_account):
    bank_account.collect_interest()
    # bulatkan dg round
    assert round(bank_account.balance,6) == 55

# kita ingin menjalankan test dengan input yg berbeda" caranya dg decorator brkt
@pytest.mark.parametrize("deposit, withdraw, expected",[
    # artinya tambahkan 300 ke akun bank kita(deposit) lalu ambil uang 100 (withdraw), uang sehrsnya ada 200
    (300, 100, 200),
    (400, 300, 100)
])

def test_transaksi(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

 # test untuk kasus dimana jumlah penarikan saldo lbh bsr dari saldonya (ini tdk boleh terjd hrs error). expectednya bernilai Error
def test_insufficient_funds(bank_account):
    # with pytest.raises(Exception):
    with pytest.raises(insufficientFunds):
        bank_account.withdraw(100)