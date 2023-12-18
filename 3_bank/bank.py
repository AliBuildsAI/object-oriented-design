from typing import List, Set
import random
from abc import ABC, abstractmethod

class BankAccount:
    def __init__(self, customer_id: int, init_deposit: float) -> None:
        self._id = customer_id
        self._balance = init_deposit

    @property
    def customer_id(self) -> int:
        return self._id
    
    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        self._balance += amount
    
    def withdraw(self, amount: float) -> bool:
        if amount <= self._balance:
            self._balance -= amount
            return True
        return False


class Teller:
    def __init__(self, teller_id: int) -> None:
        self._id = teller_id
    
    @property
    def teller_id(self) -> int:
        return self._id

class Transaction(ABC):
    def __init__(self, customer_id, teller_id):
        self._customer_id = customer_id
        self._teller_id = teller_id

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @property 
    def teller_id(self) -> int:
        return self._teller_id

    @abstractmethod
    def get_transaction_description(self):
        pass

class Withdrawal(Transaction):
    def __init__(self, customer_id: int, teller_id: int, amount: float):
        self._amount = amount
        super().__init__(customer_id, teller_id)
    
    def get_transaction_description(self):
        return 'teller {} withdrew {}$ from account {}'.format(self.teller_id, self._amount, self.customer_id)

class Deposit(Transaction):
    def __init__(self, customer_id: int, teller_id: int, amount: float):
        self._amount = amount
        super().__init__(customer_id, teller_id)
    
    def get_transaction_description(self):
        return 'teller {} deposited {}$ from account {}'.format(self.teller_id, self._amount, self.customer_id)

class OpenAccount(Transaction):
    def __init__(self, customer_id: int, teller_id: int, init_deposit: float = 0):
        super().__init__(customer_id, teller_id)
        self._init_deposit = init_deposit
    
    def get_transaction_description(self):
        return 'teller {} opened account {} with initial deposit {}'.format(self.teller_id, self.customer_id, self._init_deposit)


class BankSystem:
    def __init__(self, accounts: List[BankAccount], transactions: List[Transaction]):
       self._accounts = accounts
       self._transactions = transactions   

    def open_account(self, customer_name: str, teller_id: int, init_deposit: float = 0):
        customer_id = len(self._accounts)
        account = BankAccount(customer_id, init_deposit), 
        transaction = OpenAccount(customer_id, teller_id, init_deposit)
        self._transactions.append(transaction)
        self._accounts.append(account)
        return customer_id

    def deposit(self, customer_id: int, teller_id: int, amount: float):
        account = self.get_account(customer_id)[0]
        print(account)
        account.deposit(amount)
        transaction = Deposit(customer_id, teller_id, amount)
        self._transactions.append(transaction)

    def withdraw(self, customer_id: int, teller_id: int, amount: float):
        account = self.get_account(customer_id)[0]
        if account.balance >= amount:
            account.withdraw(amount)
        else:
            raise Exception("Insufficient Fund!")
        transaction = Withdrawal(customer_id, teller_id, amount)
        self._transactions.append(transaction)    

    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions
    
    @property
    def accounts(self) -> List[BankAccount]:
        return self._accounts
    
    def get_account(self, customer_id: int) -> BankAccount:
        return self._accounts[customer_id]
    

                 
class BankBranch:
    def __init__(self, address: str, total_cash: float, bank_system: BankSystem, tellers: List[Teller] = []) -> None:
        self._total_cash = total_cash
        self._tellers = tellers
        self._bank_system = bank_system
        self._address = address
        
    def add_teller(self, teller: Teller) -> None:
        self._tellers.append(teller)

    def remove_teller(self, teller: Teller) -> bool:
        if teller in self._tellers:
            self._tellers.remove(teller)
            return True
        return False
    
    def assign_teller(self) -> Teller:
        teller_idx = random.randint(0, len(self._tellers)-1)
        return self._tellers[teller_idx]
    
    def open_account(self, customer_name: str, init_deposit: float = 0):
        if len(self._tellers) == 0:
            raise ValueError('Branch does not have any tellers')
        teller = self.assign_teller()
        return self._bank_system.open_account(customer_name, teller.teller_id)

    def withdraw(self, customer_id, amount):
        if len(self._tellers) == 0:
            raise ValueError('Branch does not have any tellers')
        teller = self.assign_teller()
        if amount <= self._total_cash:
            self._total_cash -= amount
            return self._bank_system.withdraw(customer_id, teller.teller_id, amount)
        else:
            raise ValueError("Branch does not have enough cash")

    def deposit(self, customer_id, amount):
        if len(self._tellers) == 0:
            raise ValueError('Branch does not have any tellers')
        teller = self.assign_teller()
        self._total_cash += amount
        return self._bank_system.deposit(customer_id, teller.teller_id, amount)
    def give_cash_to_hq(self, ratio):
        cash_to_collect = round(self._cash_on_hand * ratio)
        self._cash_on_hand -= cash_to_collect
        return cash_to_collect

class BankHQ:
    def __init__(self, branches: List[BankBranch], bank_system: BankSystem, total_cash: float) -> None:
        self._branches = branches
        self._bank_system = bank_system
        self._total_cash = total_cash

    def add_branch(self, address: str, initial_fund: int) -> None:
        branch = BankBranch(address, initial_fund, bank_system)
        self._branches.append(branch)
        return branch

    def collect_cash(self, ratio: float):
        for branch in self._branches:
            cash_collected = branch.give_cash_to_hq(ratio)
            self._total_cash += cash_collected
        
    def print_transactions(self):
        for transaction in self._bank_system.transactions:
            print(transaction.get_transaction_description())

if __name__ == '__main__':
    bank_system = BankSystem([], [])
    bank = BankHQ([], bank_system, 10000)

    branch1 = bank.add_branch('123 Main St', 1000)
    branch2 = bank.add_branch('456 Elm St', 1000)

    branch1.add_teller(Teller(1))
    branch1.add_teller(Teller(2))
    branch2.add_teller(Teller(3))
    branch2.add_teller(Teller(4))

    customer_id1 = branch1.open_account('John Doe')
    customer_id2 = branch1.open_account('Bob Smith')
    customer_id3 = branch2.open_account('Jane Doe')

    branch1.deposit(customer_id1, 100)
    branch1.deposit(customer_id2, 200)
    branch2.deposit(customer_id3, 300)

    branch1.withdraw(customer_id1, 50)
    """ Possible Output:
        Teller 1 opened account 0
        Teller 2 opened account 1
        Teller 3 opened account 2
        Teller 1 deposited 100 to account 0
        Teller 2 deposited 200 to account 1
        Teller 4 deposited 300 to account 2
        Teller 2 withdrew 50 from account 0
    """

    bank.print_transactions()