from dataclasses import dataclass
from typing import List


class TicketStatus:
    def __init__(self, db_name: str, frontend_name: str, frontend_color: str = '#FFFFFF') -> None:
        self.db_name = db_name
        self.frontend_name = frontend_name
        self.frontend_color = frontend_color
    

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
            }
            
    
    def add(self, db_name: str, frontend_name: str, frontend_color: str = '#FFFFFF') -> TicketStatus:
        new_ticket_status = TicketStatus(db_name, frontend_name)
        if frontend_color:
            new_ticket_status.frontend_color = frontend_color
        self.statuses.append(new_ticket_status)
        return new_ticket_status


ticket_statuses = TicketStatuses()
ticket_statuses.add(db_name='WAIT_QUEUE', frontend_name='Ожидает вызова')
ticket_statuses.add(db_name='SERVING', frontend_name='Обслуживается')
ticket_statuses.add(db_name='CLOSED', frontend_name='Завершено')
ticket_statuses.add(db_name='CREATED', frontend_name='Создано')
ticket_statuses.add(db_name='CANCELLED', frontend_name='Отменена')
ticket_statuses.add(db_name='POSTPROCESS', frontend_name='Постобработка')
ticket_statuses.add(db_name='PROPOSED', frontend_name='Предложена')
ticket_statuses.add(db_name='EMPLOYEE', frontend_name='Приглашается на приём')
ticket_statuses.add(db_name='INVITED', frontend_name='Приглашается на приём')
ticket_statuses.add(db_name='DEFERRED', frontend_name='Отложена')
ticket_statuses.add(db_name='CHANGED', frontend_name='Изменена')
