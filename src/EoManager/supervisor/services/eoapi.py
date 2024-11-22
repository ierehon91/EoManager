import requests


class EoApi:

    SERVER = ''
    PORT = ''
    EO_API_LOGIN = ''
    EO_API_PASSWORD = ''

    def __init__(self) -> None:
        self.session = requests.Session()

    def authorization(self) -> bool:
        """Авторизация в API ЭО"""
        pass

    def check_authorization(self) -> bool:
        """Проверяет на наличии авторизации для объекта сессии в API ЭО"""
        pass



class TicketsManager(EoApi):
    def __init__(self) -> None:
        super().__init__()

    def __create_request_ticket_list_url(self) -> str:
        """Формирует URL к API ЭО для получения списка талонов"""
        pass

    def get_tickets_list(self) -> dict:
        """Возвращает список талонов"""
        pass


class WindowsManager(EoApi):
    def __init__(self) -> None:
        super().__init__()

    def __create_request_windows_list_url(self) -> str:
        """Формирует URL к API ЭО для получения списка талонов"""
        pass

    def get_windows_list(self) -> dict:
        """Возвращает список талонов"""
        pass