from __future__ import annotations
from logging.config import fileConfig
from typing import Any, cast

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.db import Base            # declarative Base
import app.models  # noqa: F401    # ensures the model classes are imported

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    section = config.get_section(config.config_ini_section)
    if section is None:
        raise RuntimeError("Alembic config section not found")
    section_any = cast(dict[str, Any], section)

    connectable = engine_from_config(
        section_any,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,  
            compare_type=True,              
            compare_server_default=True,     
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
