import datetime

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required

from supervisor.services.eoapi import TicketsManager, RequestTicketsListParams
from supervisor.services.encoding.ticket_status import ticket_statuses
from supervisor.models import Division, Profile


@login_required
@require_GET
def tickets_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком талонов"""
    divisions = request.user.profile.divisions.values()
    return render(
        request, 'supervisor/tickets_list.html', context={
            'statuses': ticket_statuses.get_all(),
            'date': datetime.date.today().strftime('%Y-%m-%d'),
            'divisions': divisions
        }
    )


@login_required
# @require_GET
def fetch_tickets_list(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    """JSON со списком талонов"""
    api = TicketsManager()

    params = RequestTicketsListParams()
    params.set_request_get_params(request)

    result = api.get_tickets_list(params=params)
    if RequestTicketsListParams.check_division_access(request.user, params.division_id):
        return HttpResponse(result)
    return HttpResponseForbidden(
        f'Ошибка доступа. Пользователь {request.user.username} не добавлен в подразделение с ID: {params.division_id}'
    )


@login_required
def ticket_detail(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """Страница с детальной информацией о талоне и его истории"""
    print('GET', request)
    context = {'ticket_id': ticket_id}
    return render(request, 'supervisor/ticket_detail.html', context=context)


@login_required
@require_GET
def fetch_ticket_history(request: HttpRequest) -> str:
    """JSON с историей талона"""
    pass


@login_required
@require_GET
def windows_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком окон"""
    return render(request, 'supervisor/windows_list.html')


@login_required
@require_GET
def fetch_windows_list(request: HttpRequest) -> str:
    """JSON со списком окон"""
    pass


@login_required
@require_GET
def free_time_tickets_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком доступных для ПЗ услуг"""
    return render(request, 'supervisor/free_time_tickets_list.html')


@login_required
@require_GET
def fetch_free_time_tickets_list(request: HttpRequest) -> str:
    """JSON со списком доступных для ПЗ услуг"""
    pass
