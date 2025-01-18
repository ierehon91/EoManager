import datetime
from typing import Union

import requests
from django.conf import settings
from django.http import HttpResponseServerError, HttpResponseForbidden
from django.http import HttpRequest
from django.contrib.auth.models import User

from supervisor.services.models.tickets_list import Content as TicketListContent
from supervisor.services.encoding.ticket_status import ticket_statuses


class RequestTicketsListParams:
    """Параметры для GET запроса получения списка талонов с сервера ЭО"""
    def __init__(
            self,
            date_from: datetime.date = datetime.date.today(),
            date_to: datetime.date = datetime.date.today(),
            division_id: int = 0,
            record_states: tuple[str] = tuple(),

            prerecord: bool = False,
            not_prerecord: bool = False,

            ) -> None:
        self.date_from = date_from
        self.date_to = date_to
        self.division_id = division_id
        self.record_states = record_states
        self.__create_record_type_param(prerecord, not_prerecord)

    def __create_record_type_param(self, prerecord: bool, not_prerecord: bool):
        if prerecord and not not_prerecord:
            self.record_type = True
        elif not prerecord and not_prerecord:
            self.record_type = False
        else:
            self.record_type = None

    def set_request_get_params(self, request: HttpRequest):
        try:
            date_param = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
        except Exception:
            date_param = datetime.date.today()

        try:
            division_param = int(request.GET['division'])
        except:
            division_param = 0

        try:
            prerecord = True if (request.GET['prerecord']) == 'true' else False
            not_prerecord = True if (request.GET['notprerecord']) == 'true' else False
        except Exception:
            prerecord = not_prerecord = False


        record_statuses = []
        statuses = ticket_statuses.get_all()
        for status in statuses:
            try:
                if request.GET[status['db_name']] == 'true':
                    record_statuses.append(status['db_name'])
            except Exception as _ex:
                print(_ex)
                continue

        self.date_from = date_param
        self.date_to = date_param
        self.division_id = division_param
        self.record_states = tuple(record_statuses)
        self.prerecord = prerecord
        self.not_prerecord = not_prerecord

    @staticmethod
    def check_division_access(user: User, division_id: int):
        if division_id in user.profile.divisions.values_list('division_id', flat=True):
            return True
        return False

    def get_url_params(self) -> list:
        """Формирует список параметров в формате для добавления в URL в виде параметров запроса"""
        params = []
        params.append(f'queueDateFrom={datetime.datetime.strftime(self.date_from, '%Y-%m-%d')}+00:00')
        params.append(f'queueDateTo={datetime.datetime.strftime(self.date_to, '%Y-%m-%d')}+23:59')
        params.append(f'divisionIds={self.division_id}')
        for record_state in self.record_states:
            params.append(f'recordState={record_state}')
        if self.record_type is not None:
            params.append(f'recordType=true') if self.record_type else params.append(f'recordType=false')
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
        

    def get_tickets_list(self, params: RequestTicketsListParams) -> str:
        """Возвращает список талонов для импорта на сайт"""
        self._check_authorization()
        tickets_response = self.session.get(url=self.__create_request_ticket_list_url(
            params=params.get_url_params(),
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
        pass
