from sqlalchemy import select

from core.exceptions import HTTP404
from core.database.session import DBSession
from transactions.models import Transaction, TransactionType, TransactionCategory


def is_category_belongs_type(tr_type: TransactionType, tr_category: TransactionCategory) -> bool:
    return tr_type.id == tr_category.type_id


def is_transaction_exists(db_session: DBSession, account_id, transaction_id: int) -> bool:
    stmt = select(Transaction).where(Transaction.account_id == account_id, Transaction.id == transaction_id)
    return db_session.execute(stmt).scalar() is not None


def get_account_transaction(db_session: DBSession, account_id, transaction_id: int) -> Transaction:
    stmt = select(Transaction).where(Transaction.account_id == account_id, Transaction.id == transaction_id)
    transaction = db_session.execute(stmt).scalar()
    if transaction is None:
        raise HTTP404(f'Transaction with id={transaction_id} does not exist. (In this account.)')
    return transaction
