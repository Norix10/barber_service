"""rename appointments_id to assistance_id

Revision ID: 244119d9d777
Revises: a71ad9d209da
Create Date: 2026-01-08 14:29:27.660199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '244119d9d777'
down_revision: Union[str, Sequence[str], None] = 'a71ad9d209da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Створити нову таблицю assistances (якщо її ще немає)
    op.create_table(
        'assistances',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.UniqueConstraint('name'),
    )

    # 2. Додати нову колонку в appointments
    op.add_column('appointments', sa.Column('assistance_id', sa.Integer(), nullable=True))

    # 3. Створити новий FK
    op.create_foreign_key(
        'appointments_assistance_id_fkey',
        'appointments', 'assistances',
        ['assistance_id'], ['id'],
    )

    # 4. Заповнити assistance_id зі старого service_id (якщо потрібно)
    op.execute("UPDATE appointments SET assistance_id = service_id")

    # 5. Прибрати старий FK і колонку
    op.drop_constraint('appointments_service_id_fkey', 'appointments', type_='foreignkey')
    op.drop_column('appointments', 'service_id')

    # 6. Лише ТЕПЕР можна дропати services, якщо вона більше не потрібна
    op.drop_table('services')



def downgrade():
    # 1. Створити services назад (мінімально)
    op.create_table(
        'services',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.UniqueConstraint('name'),
    )

    # 2. Додати service_id
    op.add_column('appointments', sa.Column('service_id', sa.Integer(), nullable=True))

    # 3. FK назад
    op.create_foreign_key(
        'appointments_service_id_fkey',
        'appointments', 'services',
        ['service_id'], ['id'],
    )

    # 4. Повернути значення (якщо є логіка)
    op.execute("UPDATE appointments SET service_id = assistance_id")

    # 5. Прибрати новий FK і колонку
    op.drop_constraint('appointments_assistance_id_fkey', 'appointments', type_='foreignkey')
    op.drop_column('appointments', 'assistance_id')

    # 6. Дропнути assistances
    op.drop_table('assistances')
