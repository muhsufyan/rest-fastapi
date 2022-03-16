def add(num1: int, num2: int):
    return num1 + num2
# untuk error saldo
class insufficientFunds(Exception):
    pass
# perhitungan transaksi buku tabungan
class BankAccount():
    # awal mula buka buku tabungan pasti depositnya 0 
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
    # amount adlh jumlah uang yg masuk ke rekening kita
    def deposit(self, amount):
        self.balance += amount
    # mengambil uang/transfer
    # def withdraw(self, amount):
    #     self.balance -= amount
    
    # kode pengambilan uang diatas tdk bnr karena akan menghslkan nilai -, tdk mungkin ada tabungan yg minus dlm transaksi
    # jd kita perbaiki
    def withdraw(self, amount):
        # jumlah penarikan saldo hrs lbh kcl dr saldo untuk mencegah minus
        if amount > self.balance:
            # raise Exception("Maaf transaksi tidak bisa, jumlah penarikan lbh besar dari saldo")
            raise insufficientFunds("Maaf transaksi tidak bisa, jumlah penarikan lbh besar dari saldo")  
        self.balance -= amount
    # investasi (bunga keuntungan)
    def collect_interest(self):
        self.balance *= 1.1