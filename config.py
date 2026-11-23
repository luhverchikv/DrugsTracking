# config.py
# config.py
"""Конфигурация парсера цен apteka.103.by (таблетка)."""

# Шаблон ссылки: {drug} — часть из DRUGS, {region} — ключ из REGIONS
URL_TEMPLATE = "https://apteka.103.by/{drug}/{region}/"

# slug региона в URL -> название для отчетов пользователю
REGIONS = {
    "minsk":          "Минск",
    "minsk-region":   "Минская область",
    "brest-region":   "Брестская область",
    "vitebsk-region": "Витебская область",
    "gomel-region":   "Гомельская область",
    "grodno-region":  "Гродненская область",
    "mogilev-region": "Могилёвская область",
    "oct":            "Октябрьский район (Минск)",
}

# Ключ = английское имя (оно же имя таблицы в БД).
# Правило именования: {препарат}{доза}_{кол-во таблеток}, дробная доза 2.5 -> 2_5
DRUGS = {
    "concor_cor2_5_30": {
        "name_ru":  "Конкор Кор 2.5 мг №30",
        "url_part": "konkor-kor/36759-tabletki-2.5-mg-n30/merk",
    },
    "concor5_30": {
        "name_ru":  "Конкор 5 мг №30",
        "url_part": "konkor/32717-tabletki-5-mg-n30/merk",
    },
    "concor5_50": {
        "name_ru":  "Конкор 5 мг №50",
        "url_part": "konkor/32835-tabletki-5-mg-n50/merk",
    },
    "concor10_30": {
        "name_ru":  "Конкор 10 мг №30",
        "url_part": "konkor/33111-tabletki-10-mg-n30/merk",
    },
    "concor10_50": {
        "name_ru":  "Конкор 10 мг №50",
        "url_part": "konkor/42262-tabletki-10-mg-n50/merk",
    },
}
