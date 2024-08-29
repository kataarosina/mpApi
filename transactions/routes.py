from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.sql import select, update

from accounts.utils import get_user_account
from auth.models import User
from auth.utils import get_current_active_user
from core.database.session import DBSession
from core.database.session import create_db_session
from core.exceptions import HTTP404
from transactions.dtos import TransactionCreateDTO, TransactionUpdateDTO
from transactions.dtos import TransactionRelDTO, TransactionTypeRelDTO, TransactionCategoryRelDTO
from transactions.models import Transaction, TransactionType, TransactionCategory
from transactions.utils import is_category_belongs_type, get_account_transaction, is_transaction_exists

transactions_router = APIRouter(
    prefix='/accounts/{account_id}/transactions',
    tags=['transactions'],
    responses={404: {'description': 'Not found'}},
)
types_router = APIRouter(
    prefix='/transactions/types',
    tags=['transactions_types'],
    responses={404: {'description': 'Not found'}},
)
categories_router = APIRouter(
    prefix='/transactions/categories',
    tags=['transactions_categories'],
    responses={404: {'description': 'Not found'}},
)


########################################################
#            Transactions types routes                 #
########################################################

# Стоит мне тут вписать в сигнатуру функции current_user: Annotated[User, Depends(get_current_active_user)]
# роут тут же станет требовать наличие токена (вернее он будет требовать пользователя, которого будет получать через
# токен которого будет требовать). Т.е. будет необходимо обладать токеном (быть залогиненым)
@types_router.get('/', response_model=list[TransactionTypeRelDTO])
async def get_types(db_session: DBSession = Depends(create_db_session)) -> list[TransactionType]:
    tr_types = db_session.scalars(select(TransactionType)).all()
    return tr_types


@types_router.get('/{type_id}', response_model=TransactionTypeRelDTO)
async def get_type(type_id: int, db_session: DBSession = Depends(create_db_session)) -> TransactionType | dict:
    tr_type = db_session.get(TransactionType, type_id)
    if tr_type is None:
        raise HTTP404(f'Transaction type #{type_id} not found.')
    return tr_type


@types_router.get('/{type_id}/categories', response_model=list[TransactionCategoryRelDTO])
async def get_type_categories(type_id: int, db_session: DBSession = Depends(create_db_session)) -> TransactionCategory:
    stmt = select(TransactionCategory).where(TransactionCategory.type_id == type_id)
    categories = db_session.scalars(stmt).all()
    return categories


########################################################
#          Transactions categories routes              #
########################################################

@categories_router.get('/', response_model=list[TransactionCategoryRelDTO])
async def get_categories(db_session: DBSession = Depends(create_db_session)) -> list[TransactionCategory]:
    tr_categories = db_session.scalars(select(TransactionCategory)).all()
    return tr_categories


@categories_router.get('/{category_id}', response_model=TransactionCategoryRelDTO)
async def get_category(category_id: int,
                       db_session: DBSession = Depends(create_db_session)) -> TransactionCategory | dict:
    category = db_session.get(TransactionCategory, category_id)
    if category is None:
        raise HTTP404(f'Transaction category #{category_id} not found.')
    return category


########################################################
#               Transactions routes                    #
########################################################

@transactions_router.get('/', response_model=list[TransactionRelDTO])
async def get_transactions(
        account_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db_session: DBSession = Depends(create_db_session)
) -> list[Transaction]:
    account = get_user_account(db_session, current_user, account_id)
    stmt = select(Transaction).where(Transaction.account_id == account.id)
    transactions = db_session.scalars(stmt).all()
    return transactions


@transactions_router.get('/{transaction_id}', response_model=TransactionRelDTO)
async def get_transaction(account_id: int,
                          transaction_id: int,
                          current_user: Annotated[User, Depends(get_current_active_user)],
                          db_session: DBSession = Depends(create_db_session)) -> Transaction | dict:
    account = get_user_account(db_session, current_user, account_id)
    transaction = get_account_transaction(db_session, account.id, transaction_id)
    return transaction


@transactions_router.post('/', response_model=TransactionRelDTO)
async def create_transaction(
        account_id: int,
        data_dto: TransactionCreateDTO,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db_session: DBSession = Depends(create_db_session)
) -> Transaction:
    account = get_user_account(db_session, current_user, account_id)

    if (tr_type := db_session.get(TransactionType, data_dto.type_id)) is None:
        raise HTTP404(f'There is no type with id={data_dto.type_id}')
    if (category := db_session.get(TransactionCategory, data_dto.category_id)) is None:
        raise HTTP404(f'There is no category with id={data_dto.category_id}')
    is_category_belongs_type(tr_type, category)

    data = data_dto.model_dump()
    data['account_id'] = account.id

    try:
        new_transaction = Transaction(**data)
        db_session.add(new_transaction)
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error in try to create transaction.'
                   f'\nDetails: {e}'
        )
    else:
        db_session.commit()
        return new_transaction


# TODO add account check
@transactions_router.put('/{transaction_id}', response_model=TransactionRelDTO)
async def update_transaction(
        account_id: int,
        transaction_id: int,
        data_dto: TransactionUpdateDTO,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db_session: DBSession = Depends(create_db_session)
) -> Transaction:
    account = get_user_account(db_session, current_user, account_id)

    if (tr_type := db_session.get(TransactionType, data_dto.type_id)) is None:
        raise HTTP404(f'There is no type with id={data_dto.type_id}')
    if (category := db_session.get(TransactionCategory, data_dto.category_id)) is None:
        raise HTTP404(f'There is no category with id={data_dto.category_id}')
    # is_category_belongs_type_or_404?
    if not is_category_belongs_type(tr_type, category):
        raise HTTP404(f'Category <{category.name}> does not belong to type <{tr_type.name}>')  # TODO 404 or other?
    # is_transaction_exists_or_404?
    if not is_transaction_exists(db_session, account.id, transaction_id):
        raise HTTP404(f'Transaction with id={transaction_id} does not exist. (In this account.)')

    try:
        stmt = update(Transaction).where(
            Transaction.account_id == account.id,
            Transaction.id == transaction_id
        ).values(**data_dto.model_dump())
        db_session.execute(stmt)
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Something went wrong when updating.'
                   f'\nDetails: {e}'
        )
    else:
        db_session.commit()
        return db_session.get(Transaction, transaction_id)  # TODO Fix this. Ugly.


# TODO add account check
@transactions_router.delete('/{transaction_id}')
async def delete_transaction(
        account_id: int,
        transaction_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db_session: DBSession = Depends(create_db_session)
) -> dict:
    account = get_user_account(db_session, current_user, account_id)
    transaction = get_account_transaction(db_session, account.id, transaction_id)

    try:
        db_session.delete(transaction)
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error in try to delete transaction.'
                   f'\nDetails: {e}'
        )
    else:
        db_session.commit()
        return {'status': 'OK', 'message': f'Transaction with id={transaction_id} successfully deleted.'}
