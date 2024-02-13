"""Add transaction_date column to Accounting

Revision ID: a2b408d53d08
Revises: 
Create Date: 2024-02-13 15:18:56.940115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2b408d53d08'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounting', 'date',
               existing_type=sa.VARCHAR(),
               type_=sa.Date(),
               existing_nullable=True,
               postgresql_using="date::date")
    op.alter_column('accounting', 'transaction_date',
               existing_type=sa.VARCHAR(),
               type_=sa.Date(),
               existing_nullable=True,
               postgresql_using="transaction_date::date")
    op.alter_column('accounting', 'amount',
               existing_type=sa.VARCHAR(),
               type_=sa.Numeric(precision=10, scale=2),
               existing_nullable=True,
               postgresql_using="amount::numeric(10,2)")
    op.alter_column('expenses', 'amount',
               existing_type=sa.VARCHAR(),
               type_=sa.Numeric(precision=10, scale=2),
               existing_nullable=True,
               postgresql_using="amount::numeric(10,2)")
    op.alter_column('income', 'amount',
               existing_type=sa.VARCHAR(),
               type_=sa.Numeric(precision=10, scale=2),
               existing_nullable=True,
               postgresql_using="amount::numeric(10,2)")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('income', 'amount',
               existing_type=sa.Numeric(precision=10, scale=2),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('expenses', 'amount',
               existing_type=sa.Numeric(precision=10, scale=2),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('accounting', 'amount',
               existing_type=sa.Numeric(precision=10, scale=2),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('accounting', 'transaction_date',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('accounting', 'date',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###