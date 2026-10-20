"""restringe valores de status

Revision ID: aed8ba6a703c
Revises: 5c8dbe41c2a7
Create Date: 2026-10-19 22:15:25.849650
"""
from alembic import op
import sqlalchemy as sa


revision = 'aed8ba6a703c'
down_revision = '5c8dbe41c2a7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint(
        "ck_arquivos_status", "arquivos", "status IN ('pendente', 'concluido')"
    )


def downgrade():
    op.drop_constraint("ck_arquivos_status", "arquivos", type_="check")
