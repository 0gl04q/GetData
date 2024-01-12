import flet as ft
from flet import Page

from functions import create_xlsx
import db


def main(page: Page):
    def btn_click(e):
        ''' Обработка нажатия на кнопку Отчет '''

        def check_input_text(text_field):
            ''' Валидатор полей '''
            if not text_field.value:
                text_field.error_text = f'Введите {text_field.label.lower()}'
                page.update()
                return False
            else:
                text_field.error_text = ''
            return True

        # Создаем кортеж полей
        fields = (drop_year, drop_region, drop_month, drop_typesc)

        # Проверяем все поля, если проверка проходит то создаем Excel
        if all(list(map(check_input_text, fields))):

            # Определяем id и имя региона
            region_id, region_name = regions[drop_region.value], drop_region.value

            # Создаем Excel
            create_xlsx(drop_year.value, drop_month.value, drop_typesc.value, region=(region_name, region_id))

            # Очищаем поля
            for field in fields:
                field.value = ''

            page.banner.open = True
            page.update()

    def close_banner(e):
        ''' Обработчик закрытия банера '''
        page.banner.open = False
        page.update()

    # Саздаем выпадающие списки
    drop_year = ft.Dropdown(
        label="Год",
        options=[ft.dropdown.Option(str(year)) for year in range(2021, 2015, -1)]
    )
    drop_month = ft.Dropdown(
        label="Месяц",
        options=[ft.dropdown.Option(str(month)) for month in range(1, 13)]
    )

    drop_typesc = ft.Dropdown(
        label="Тип",
        options=[ft.dropdown.Option('ХВС'), ft.dropdown.Option('ГВС')]
    )

    # Получаем словарь регионов Region: ID
    regions = dict(db.get_region())

    drop_region = ft.Dropdown(
        label="Регион",
        options=[ft.dropdown.Option(region) for region in regions]
    )

    # Задаем настройки страницы
    page.window_width = 650
    page.window_height = 500
    page.theme_mode = "dark"
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.FLOOD),
        leading_width=40,
        title=ft.Text("Выгрузка отчетов"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    page.banner = ft.Banner(
        bgcolor=ft.colors.GREEN,
        leading=ft.Icon(ft.icons.FITBIT, color=ft.colors.WHITE, size=40),
        content=ft.Text(
            "Отчет сохранен!"
        ),
        actions=[
            ft.ElevatedButton("Закрыть", on_click=close_banner, color=ft.colors.WHITE)
        ],

    )
    page.add(
        ft.ResponsiveRow(
            [ft.Column(col=6, controls=[drop_year, drop_month]),
             ft.Column(col=6, controls=[drop_typesc, drop_region])]
        ),
        ft.Row(
            controls=[ft.ElevatedButton("ОТЧЕТ", on_click=btn_click, width=300, color=ft.colors.WHITE)],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
