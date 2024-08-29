from decimal import Decimal

from sqlalchemy.sql import select

from core.database.session import DBSession
from transactions.models import TransactionType, TransactionCategory, Transaction
from accounts.models import Account
from currencies.models import Currency

"""
Топорненько всё это.
"""


print(f'Imports:\n'
      f'{DBSession}\n'
      f'{TransactionType} {TransactionCategory} {Transaction}\n'
      f'{Account}\n'
      f'{Currency}\n')


def cleanup():
    with DBSession() as db_session:
        if transactions := db_session.scalars(select(Transaction)).all():
            for t in transactions:
                print(f'Delete: {t} ...')
            [db_session.delete(t) for t in transactions]
            db_session.commit()
            print('Success.\n')
        if categories := db_session.scalars(select(TransactionCategory)).all():
            for tr_category in categories:
                print(f'Delete: {tr_category} ...')
            [db_session.delete(tr_category) for tr_category in categories]
            db_session.commit()
            print('Success.\n')
        if types := db_session.scalars(select(TransactionType)).all():
            for tr_type in types:
                print(f'Delete: {tr_type} ...')
            [db_session.delete(tr_type) for tr_type in types]
            db_session.commit()
            print('Success.\n')
        if accounts := db_session.scalars(select(Account)).all():
            for a in accounts:
                print(f'Delete: {a} ...')
            [db_session.delete(a) for a in accounts]
            db_session.commit()
            print('Success.\n')
        if currencies := db_session.scalars(select(Currency)).all():
            for c in currencies:
                print(f'Delete: {c} ...')
            [db_session.delete(c) for c in currencies]
            db_session.commit()
            print('Success.\n')


if __name__ == '__main__':
    choice = input('U want run cleanup? (It will delete all data.): ')
    if choice not in ['Y', 'y']:
        exit()
    cleanup()
    db_session = DBSession()
    try:
        # create test currency
        currency = Currency(
            name='Test currency',
            symbol='@',
            code='ASD',
        )
        db_session.add(currency)
        db_session.commit()

        # create test account
        account = Account(
            name='ASD account',
            description='ASD test account',
            currency=currency,
        )
        db_session.add(account)
        db_session.commit()

        # create test transactions types
        tr_type_income = TransactionType(name='income')
        tr_type_expense = TransactionType(name='expense')
        db_session.add(tr_type_income)
        db_session.add(tr_type_expense)
        db_session.commit()

        # create test categories
        tr_category_salary = TransactionCategory(name='salary', description='Come on, I deserve it.', type=tr_type_income)
        tr_category_present = TransactionCategory(name='present', description='Oh... thank you!', type=tr_type_income)
        tr_category_food = TransactionCategory(name='food', description='Om-nom-nom', type=tr_type_expense)
        tr_category_entertainment = TransactionCategory(name='entertainment', description='Enjoying', type=tr_type_expense)
        tr_category_other = TransactionCategory(name='other', description='', type=tr_type_expense)
        db_session.add(tr_category_salary)
        db_session.add(tr_category_present)
        db_session.add(tr_category_food)
        db_session.add(tr_category_entertainment)
        db_session.add(tr_category_other)
        db_session.commit()

        # create test transactions
        tr_income_salary = Transaction(
            account=account,
            type=tr_type_income,
            category=tr_category_salary,
            amount=Decimal('10.00'),
        )
        tr_income_present = Transaction(
            account=account,
            type=tr_type_income,
            category=tr_category_present,
            amount=Decimal('5.00'),
        )
        tr_expense_food = Transaction(
            account=account,
            type=tr_type_expense,
            category=tr_category_food,
            amount=Decimal('2.00'),
        )
        tr_expense_entertainment = Transaction(
            account=account,
            type=tr_type_expense,
            category=tr_category_entertainment,
            amount=Decimal('1.00'),
        )
        tr_expense_other = Transaction(
            account=account,
            type=tr_type_expense,
            category=tr_category_other,
            amount=Decimal('1.00'),
        )
        db_session.add(tr_income_salary)
        db_session.add(tr_income_present)
        db_session.add(tr_expense_food)
        db_session.add(tr_expense_entertainment)
        db_session.add(tr_expense_other)
        db_session.commit()
        for tr in [
            tr_income_salary,
            tr_income_present,
            tr_expense_food,
            tr_expense_entertainment,
            tr_expense_other,
        ]:
            print(f'Transaction #{tr.id} successfully created. [{tr}]')
    except Exception as e:
        print(e)
        db_session.rollback()
    finally:
        db_session.close()
