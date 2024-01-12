import flet as ft
from flet import Page

from functions import create_xlsx
import db


def main(page: Page):
    def btn_click(e):
        def check_input_text(text_field):
            if not text_field.value:
                text_field.error_text = f'Введите {text_field.label.lower()}'
                page.update()
                return False
            else:
                text_field.error_text = ''
            return True

        fields = (drop_year, drop_region, drop_month, drop_typesc)

        if all(list(map(check_input_text, fields))):
            region_id = regions[drop_region.value]
            create_xlsx(drop_year.value, drop_month.value, drop_typesc.value, region_id)

            for field in fields:
                field.value = ''

            page.banner.open = True
            page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

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

    regions = dict(db.get_region())

    drop_region = ft.Dropdown(
        label="Регион",
        options=[ft.dropdown.Option(region) for region in regions]
    )

    page.window_width = 650
    page.window_height = 500

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
