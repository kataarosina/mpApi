import random
from decimal import Decimal
from datetime import date

test_types = ['income', 'expense', 'transfer']


def get_test_transactions(n: int, transaction_class) -> dict:
    return {
        t_id: gen_rand_transaction(transaction_class)
        for t_id in range(n)
    }


def gen_rand_transaction(transaction_class):
    return transaction_class(
        type=random.choice(test_types),
        amount=Decimal(f'{random.randint(0, 100)}.{random.randint(0, 100)}'),
        created=date.today()
    )
