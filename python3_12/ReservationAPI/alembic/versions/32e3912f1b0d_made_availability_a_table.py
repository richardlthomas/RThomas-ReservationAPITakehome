"""made Availability a table

Revision ID: 32e3912f1b0d
Revises: 907e76adab31
Create Date: 2024-12-05 02:50:20.272051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32e3912f1b0d'
down_revision: Union[str, None] = '907e76adab31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
