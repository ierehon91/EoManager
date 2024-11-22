from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required


@login_required
@require_GET
def tickets_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком талонов"""
    return render(request, 'supervisor/tickets_list.html')


@login_required
@require_GET
def fetch_tickets_list(request: HttpRequest) -> str:
    """JSON со списком талонов"""
    pass


@login_required
@require_GET
def ticket_detail(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """Страница с детальной информацией о талоне и его истории"""
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
