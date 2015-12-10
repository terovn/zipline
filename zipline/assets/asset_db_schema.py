import sqlalchemy as sa


def generate_asset_db_metadata(bind=None):
    metadata = sa.MetaData(bind=bind)
    _version_table_schema(metadata)
    _equities_table_schema(metadata)
    _futures_exchanges_schema(metadata)
    _futures_root_symbols_schema(metadata)
    _futures_contracts_schema(metadata)
    _asset_router_schema(metadata)
    return metadata


# A list of the names of all tables in the assets db
asset_db_table_names = ['version_info', 'equities', 'futures_exchanges',
                        'futures_root_symbols', 'futures_contracts',
                        'asset_router']


def _equities_table_schema(metadata):
    return sa.Table(
        'equities',
        metadata,
        sa.Column(
            'sid',
            sa.Integer,
            unique=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column('symbol', sa.Text),
        sa.Column('company_symbol', sa.Text, index=True),
        sa.Column('share_class_symbol', sa.Text),
        sa.Column('fuzzy_symbol', sa.Text, index=True),
        sa.Column('asset_name', sa.Text),
        sa.Column('start_date', sa.Integer, default=0, nullable=False),
        sa.Column('end_date', sa.Integer, nullable=False),
        sa.Column('first_traded', sa.Integer, nullable=False),
        sa.Column('exchange', sa.Text),
    )


def _futures_exchanges_schema(metadata):
    return sa.Table(
        'futures_exchanges',
        metadata,
        sa.Column(
            'exchange',
            sa.Text,
            unique=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column('timezone', sa.Text),
    )


def _futures_root_symbols_schema(metadata):
    return sa.Table(
        'futures_root_symbols',
        metadata,
        sa.Column(
            'root_symbol',
            sa.Text,
            unique=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column('root_symbol_id', sa.Integer),
        sa.Column('sector', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column(
            'exchange',
            sa.Text,
            sa.ForeignKey('futures_exchanges.exchange'),
        ),
    )


def _futures_contracts_schema(metadata):
    return sa.Table(
        'futures_contracts',
        metadata,
        sa.Column(
            'sid',
            sa.Integer,
            unique=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column('symbol', sa.Text, unique=True, index=True),
        sa.Column(
            'root_symbol',
            sa.Text,
            sa.ForeignKey('futures_root_symbols.root_symbol'),
            index=True
        ),
        sa.Column('asset_name', sa.Text),
        sa.Column('start_date', sa.Integer, default=0, nullable=False),
        sa.Column('end_date', sa.Integer, nullable=False),
        sa.Column('first_traded', sa.Integer, nullable=False),
        sa.Column(
            'exchange',
            sa.Text,
            sa.ForeignKey('futures_exchanges.exchange'),
        ),
        sa.Column('notice_date', sa.Integer, nullable=False),
        sa.Column('expiration_date', sa.Integer, nullable=False),
        sa.Column('auto_close_date', sa.Integer, nullable=False),
        sa.Column('multiplier', sa.Float),
        sa.Column('tick_size', sa.Float),
    )


def _asset_router_schema(metadata):
    return sa.Table(
        'asset_router',
        metadata,
        sa.Column(
            'sid',
            sa.Integer,
            unique=True,
            nullable=False,
            primary_key=True),
        sa.Column('asset_type', sa.Text),
    )


def _version_table_schema(metadata):
    return sa.Table(
        'version_info',
        metadata,
        sa.Column(
            'id',
            sa.Integer,
            unique=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column(
            'version',
            sa.Integer,
            unique=True,
            nullable=False,
        ),
        # This constraint ensures a single entry in this table
        sa.CheckConstraint('id <= 1'),
    )
