from dataclasses import dataclass

import settings


@dataclass(frozen=True)
class Locale:
    name: str
    title: str


LOCALE_UA = Locale(name="ua", title="Українська")
LOCALE_EN = Locale(name="en", title="English")

LOCALES = [LOCALE_UA, LOCALE_EN]

locale_name_by_title = {locale.title: locale.name for locale in LOCALES}
locale_title_by_name = {locale.name: locale.title for locale in LOCALES}

ua_to_en = {
    "Новини": "News",
    "Опис": "Description",
    "Нотатки": "Notes",
    "Профіль": "Profile",
    "Нікнейм": "Nickname",
    "[Перелогінитись]": "[Relogin]",
    "Скін": "Skin",
    "[Вибрати]": "[Select]",
    "Не вибрано": "Not selected",
    "Загальні налаштування": "General settings",
    "Робоча папка": "Working directory",
    "Налаштування модпаку": "Modpack settings",
    "Мін. оперативки": "Min RAM",
    "Макс. оперативки": "Max RAM",
    "[Запуск]": "[Play]",
    "Некоректний логін (має бути від 3 символів, може містити лише цифри, букви і _)":
        "Invalid login (must be at least 3 symbols, can only contain letters, digits and _)",
    "Некоректний пароль (має бути від 4 символів, не може містити пробіл)":
        "Invalid password (must be at least 4 symbols, can't contain whitespace)",
    "Паролі не співпадають": "Passwords do not match",
    "Помилка": "Error",
    "Невірний пароль": "Wrong password",
    "Користувача не знайдено": "User not found",
    "Користувач вже існує": "User already exists",
    "Невідома помилка": "Unknown error",
    "Пароль": "Password",
    "[Увійти]": "[Log in]",
    "[Увійти з існуючим аккаунтом]": "[Log in with existing account]",
    "[Зареєструватись]": "[Register]",
    "Лог": "Log",
    "Мова": "Language",
}


def localize(string):
    return string if settings.locale == LOCALE_UA.name else ua_to_en[string]
