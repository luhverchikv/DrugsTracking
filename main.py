# main.py
from loguru import logger
from sqlalchemy import select, func

from database.db import SessionLocal
from database.init_db import init_db
from database.models import Region, Drug, Pharmacy, Price


def main():
    logger.info("Инициализация базы данных...")
    init_db()

    with SessionLocal() as session:
        for model in (Region, Drug, Pharmacy, Price):
            count = session.scalar(select(func.count()).select_from(model))
            logger.info(f"{model.__tablename__}: {count} строк")

    # Следующие шаги:
    # create_pharmacies_103()  — парсер аптек
    # parse_prices()           — парсер цен по DRUGS × REGIONS


if __name__ == "__main__":
    main()
