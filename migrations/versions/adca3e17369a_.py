"""empty message

Revision ID: adca3e17369a
Revises: 60d365482ee9
Create Date: 2021-05-22 23:01:13.143648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adca3e17369a'
down_revision = '60d365482ee9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_view',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('article', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article'], ['article.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('article', sa.Column('views', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'views')
    op.drop_table('article_view')
    # ### end Alembic commands ###