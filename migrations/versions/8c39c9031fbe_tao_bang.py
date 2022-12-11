"""tao bang

Revision ID: 8c39c9031fbe
Revises: 
Create Date: 2022-12-08 14:42:33.703560

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision = '8c39c9031fbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('spatial_ref_sys')
    op.add_column('cinemas', sa.Column(
        'district', sa.String(length=255), nullable=False))
    op.drop_index('idx_cinemas_geom', table_name='cinemas')
    op.alter_column('movies', 'actor',
                    existing_type=sa.TEXT(),
                    nullable=True)
    op.alter_column('movies', 'director',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=True)
    op.alter_column('movies', 'genre',
                    existing_type=sa.TEXT(),
                    nullable=True)
    op.alter_column('users', 'gender',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('users', 'phone_number',
                    existing_type=sa.VARCHAR(length=10),
                    nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone_number',
                    existing_type=sa.VARCHAR(length=10),
                    nullable=False)
    op.alter_column('users', 'gender',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('movies', 'genre',
                    existing_type=sa.TEXT(),
                    nullable=False)
    op.alter_column('movies', 'director',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=False)
    op.alter_column('movies', 'actor',
                    existing_type=sa.TEXT(),
                    nullable=False)
    # op.create_index('idx_cinemas_geom', 'cinemas', ['geom'], unique=False)
    op.drop_column('cinemas', 'district')
    op.create_table('spatial_ref_sys',
                    sa.Column('srid', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.Column('auth_name', sa.VARCHAR(length=256),
                              autoincrement=False, nullable=True),
                    sa.Column('auth_srid', sa.INTEGER(),
                              autoincrement=False, nullable=True),
                    sa.Column('srtext', sa.VARCHAR(length=2048),
                              autoincrement=False, nullable=True),
                    sa.Column('proj4text', sa.VARCHAR(length=2048),
                              autoincrement=False, nullable=True),
                    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)',
                                       name='spatial_ref_sys_srid_check'),
                    sa.PrimaryKeyConstraint(
                        'srid', name='spatial_ref_sys_pkey')
                    )
    # ### end Alembic commands ###