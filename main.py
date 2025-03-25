from flet import Page, app, WEB_BROWSER
from src.view.app import ImprextaeApp
from src.utils.connection import close_connection


def main(page: Page):
    ImprextaeApp(page)


if __name__ == "__main__":
    try:
        app(target=main, assets_dir='assets', view=WEB_BROWSER)
    finally:
        close_connection()
