import datetime
from typing import Union

import requests
from django.conf import settings
from django.http import HttpResponseServerError

from supervisor.services.models.tickets_list import Content as TicketListContent


class RequestTicketsListParams:
    def __init__(
            self,
            date_from: datetime.date,
            date_to: datetime.date,
            record_states: tuple = tuple(),
            prerecord: bool = False,
            not_prerecord: bool = False,
            ) -> None:
        self.date_from = date_from
        self.date_to = date_to
        self.record_states = record_states
        if prerecord and not not_prerecord:
            self.record_type = True
        elif not prerecord and not_prerecord:
            self.record_type = False
        else:
            self.record_type = None

    def get_url_params(self) -> list:
        params = []
        params.append(f'queueDateFrom={datetime.datetime.strftime(self.date_from, '%Y-%m-%d')}+00:00')
        params.append(f'queueDateTo={datetime.datetime.strftime(self.date_to, '%Y-%m-%d')}+23:59')
        for record_state in self.record_states:
            params.append(f'recordState={record_state}')
        if record_state:
            params.append(f'recordType=true') if record_state else params.append(f'recordType=false')
        return params



class EoApi:

    EO_API_SERVER = settings.EO_API_SERVER
    EO_API_PORT = settings.EO_API_PORT
    EO_API_LOGIN = settings.EO_API_LOGIN
    EO_API_PASSWORD = settings.EO_API_PASSWORD
    EO_API_HOST = f'http://{EO_API_SERVER}:{EO_API_PORT}/elq_frontoffice/supervisor'

    def __init__(self) -> None:
        self.session = requests.Session()

    def __authorization(self) -> int:
        """Авторизация в API ЭО"""
        login_url = f'{self.EO_API_HOST}/loginProcess'
        login_data = {
            'username': f'{self.EO_API_LOGIN}',
            'password': f'{self.EO_API_PASSWORD}',
        }
        login_request = self.session.post(url=login_url, data=login_data)
        return login_request.status_code
    
    def __check_autorization_request(self) -> int:
        check_authorization_url = f'{self.EO_API_HOST}/currentEmployee'
        response_data = self.session.get(url=check_authorization_url, allow_redirects=False)
        return response_data.status_code

    def _check_authorization(self) -> Union[bool, HttpResponseServerError]:
        """Проверяет на наличии авторизации для объекта сессии в API ЭО"""
        status_code = self.__check_autorization_request()
        if status_code == 302:
            self.__authorization()
            status_code = self.__check_autorization_request()
            if status_code == 302:
                return HttpResponseServerError('EO API not authorazation')
        if status_code == 200:
            return True
        else:
            return HttpResponseServerError('EO API ERROR')
        

class TicketsManager(EoApi):
    def __init__(self) -> None:
        super().__init__()

    def __create_request_ticket_list_url(self, params: RequestTicketsListParams) -> str:
        """Формирует URL к API ЭО для получения списка талонов"""
        url = f'{self.EO_API_HOST}/appointments?page=0&pageSize=500'  # TODO: Добавить пагинацию
        for param in params:
            url+=f'&{param}'
        return url
        

    def get_tickets_list(self) -> str:
        """Возвращает список талонов"""
        self._check_authorization()
        params = RequestTicketsListParams(  # TODO: Добавить генерацию параметров на основе формы
            date_from=datetime.date(2024, 11, 23),
            date_to=datetime.date(2024, 11, 23),
            record_states=('SERVING', 'WAIT_QUEUE'),
        ).get_url_params()
        tickets_response = self.session.get(url=self.__create_request_ticket_list_url(
            params=params,
        ))
        return TicketListContent.parse_raw(tickets_response.text).json()


class WindowsManager(EoApi):
    def __init__(self) -> None:
        super().__init__()

    def __create_request_windows_list_url(self) -> str:
        """Формирует URL к API ЭО для получения списка талонов"""
        pass

    def get_windows_list(self) -> dict:
        """Возвращает список талонов"""
        self._check_authorization()
        windows_response = self.session.get(url=self.__create_request_windows_list_url())