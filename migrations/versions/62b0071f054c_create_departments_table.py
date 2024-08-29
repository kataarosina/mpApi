"""Create Departments table

Revision ID: 62b0071f054c
Revises: 94697308060e
Create Date: 2024-06-19 05:22:07.519279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62b0071f054c'
down_revision: Union[str, None] = '94697308060e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
