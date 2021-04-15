import sqlite3

from pavo_cristatus.repositories.sqlite_repository import SQLiteRepository
from pavo_cristatus.repositories.sqlite_repository.sqlite_repository import SQLiteRepository
from pavo_cristatus.dependency_injection.ploceidae_configurator import pavo_cristatus_dependency_wrapper

__all__ = ["SQLiteRepository"]

def database_connection(database_path):
    return sqlite3.connect(database_path)

pavo_cristatus_dependency_wrapper()(database_connection)
pavo_cristatus_dependency_wrapper(resolvable_name="sqlite_repository")(SQLiteRepository)
