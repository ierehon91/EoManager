from dataclasses import dataclass
from email.policy import default
from typing import List


class TicketStatus:
    """Статуса талона"""
    def __init__(self, db_name: str, frontend_name: str, frontend_color: str = '#FFFFFF', default: bool = False) -> None:
        self.db_name = db_name
        self.frontend_name = frontend_name
        self.frontend_color = frontend_color
        self.default = default

    def set_frontend_color(self, new_color: str) -> None:
        """Задаёт новый цвет статуса для отображения на сайте"""
        self.frontend_color = new_color

    def set_frontend_name(self, new_name: str) -> None:
        """Задаёт новое названия статуса для отображения на сайте"""
        self.frontend_name = new_name

    def set_default(self, default: bool) -> None:
        """Задаёт значение статуса по умолчанию"""
        self.default = default

class TicketStatuses:
    def __init__(self) -> None:
        self.statuses: List[TicketStatus] = []

    def get(self, db_name: str) -> TicketStatus:
        for status in self.statuses:
            if db_name == status.db_name:
                return status
        return TicketStatus(db_name=db_name, frontend_name=db_name)
    
    def get_dict(self, db_name: str) -> dict:
        status = self.get(db_name=db_name)
        return {
            'db_name': status.db_name,
            'frontend_name': status.frontend_name,
            'frontend_color': status.frontend_color,
            'default': status.default,
            }

    def get_all(self) -> list:
        all_statuses = []
        for status in self.statuses:
            all_statuses.append(self.get_dict(status.db_name))
        return all_statuses
            
    
    def add(self, db_name: str, frontend_name: str, frontend_color: str = '#FFFFFF', default: bool = False) -> TicketStatus:
        new_ticket_status = TicketStatus(db_name, frontend_name, default=default)
        if frontend_color:
            new_ticket_status.frontend_color = frontend_color
        self.statuses.append(new_ticket_status)
        return new_ticket_status


ticket_statuses = TicketStatuses()
ticket_statuses.add(db_name='CREATED', frontend_name='Создано', default=True)

ticket_statuses.add(db_name='WAIT_QUEUE', frontend_name='Ожидает вызова', frontend_color='#fae1ea', default=True)
ticket_statuses.add(db_name='PROPOSED', frontend_name='Предложена', default=True)
ticket_statuses.add(db_name='SERVING', frontend_name='Обслуживается', frontend_color='#e1faf4', default=True)
ticket_statuses.add(db_name='INVITED', frontend_name='Приглашается на приём', frontend_color='#caddfa', default=True)

ticket_statuses.add(db_name='POSTPROCESS', frontend_name='Постобработка', default=True)

ticket_statuses.add(db_name='CLOSED', frontend_name='Завершено', frontend_color='#72d68e')
ticket_statuses.add(db_name='CANCELLED', frontend_name='Отменена', frontend_color='#ed6f6f')

ticket_statuses.add(db_name='DEFERRED', frontend_name='Отложена')
ticket_statuses.add(db_name='CHANGED', frontend_name='Изменена')
