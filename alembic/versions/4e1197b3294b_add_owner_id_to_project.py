"""Add owner_id to Project

Revision ID: 4e1197b3294b
Revises: ab055a30cbf6
Create Date: 2025-08-29 15:06:59.184041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e1197b3294b'
down_revision: Union[str, Sequence[str], None] = 'ab055a30cbf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ✅ Skip adding the column because it already exists
    # op.add_column('project', sa.Column('owner_id', sa.Integer(), nullable=True))

    # 1. Ensure existing projects are assigned an owner
    op.execute("UPDATE project SET owner_id = 1 WHERE owner_id IS NULL")

    # 2. Add the foreign key constraint (if not already created)
    op.create_foreign_key(
        "fk_project_owner", "project", "users", ["owner_id"], ["id"]
    )

    # 3. Enforce NOT NULL
    op.alter_column('project', 'owner_id', nullable=False)


def downgrade():
    op.drop_constraint("fk_project_owner", "project", type_="foreignkey")
    # If column already existed before this migration, don't drop it
    # op.drop_column("project", "owner_id")
