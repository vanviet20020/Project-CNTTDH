"""trường không quan trọng có thể null

Revision ID: 1f3a99f596d0
Revises: d2b239dfb970
Create Date: 2022-11-29 20:41:13.333514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f3a99f596d0'
down_revision = 'd2b239dfb970'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('spatial_ref_sys')
    op.add_column('cinemas', sa.Column('district', sa.String(length=255), nullable=False))
    op.alter_column('movies', 'director',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('movies', 'actor',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('movies', 'genre',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    op.alter_column('users', 'gender',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'gender',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    op.alter_column('movies', 'genre',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('movies', 'actor',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('movies', 'director',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.drop_column('cinemas', 'district')
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    # ### end Alembic commands ###
