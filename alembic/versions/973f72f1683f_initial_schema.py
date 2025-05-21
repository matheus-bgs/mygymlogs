"""initial schema

Revision ID: 973f72f1683f
Revises: 
Create Date: 2025-05-18 10:16:25.652407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '973f72f1683f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

enum_type = sa.Enum("standard", "myoreps", "dropset", name="exercise_variation")

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True)
    )
    op.create_table(
        'workout_sessions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('notes', sa.Text)
    )
    op.create_table(
        'exercises',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.Text)
    )
    op.create_table(
        'session_exercises',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('session_id', sa.Integer, sa.ForeignKey('workout_sessions.id', ondelete='CASCADE')),
        sa.Column('exercise_id', sa.Integer, sa.ForeignKey('exercises.id', ondelete='RESTRICT')),
        sa.Column('order', sa.Integer, nullable=False)
    )
    op.create_table(
        'sets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('session_exercise_id', sa.Integer, sa.ForeignKey('session_exercises.id', ondelete='CASCADE')),
        sa.Column('set_number', sa.Integer, nullable=False),
        sa.Column('reps', sa.Integer, nullable=False),
        sa.Column('weight', sa.Numeric(6, 2), nullable=False),
        sa.Column('exercise_variation', enum_type, nullable=False, server_default='standard'),
        sa.Column('notes', sa.Text)
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS sets CASCADE;")
    op.execute("DROP TABLE IF EXISTS session_exercises CASCADE;")
    op.execute("DROP TABLE IF EXISTS exercises;")
    op.execute("DROP TABLE IF EXISTS workout_sessions CASCADE;")
    op.execute("DROP TABLE IF EXISTS users;")

