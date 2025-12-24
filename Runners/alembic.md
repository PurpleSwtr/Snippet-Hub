# Новая миграция
alembic revision --autogenerate -m "add_new_column"

# Применить миграцию
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Посмотреть историю
alembic history

# Текущая версия
alembic current