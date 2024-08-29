from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from core.database.config import DBConfig
from core.database.models import Base

config = context.config

# INFO forward db config constants into alembic.ini
section = config.config_ini_section
config.set_section_option(section, 'DB_DRIVER', DBConfig.DB_DRIVER)
config.set_section_option(section, 'DB_HOST', DBConfig.DB_HOST)
config.set_section_option(section, 'DB_PORT', DBConfig.DB_PORT)
config.set_section_option(section, 'DB_USER', DBConfig.DB_USER)
config.set_section_option(section, 'DB_PASS', DBConfig.DB_PASS)
config.set_section_option(section, 'DB_NAME', DBConfig.DB_NAME)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Imports so that alembic can see the models.py.

from accounts.models import Account
from auth.models import User
from currencies.models import Currency
from transactions.models import TransactionType
from transactions.models import TransactionCategory
from transactions.models import Transaction
from departments.models import Department

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()