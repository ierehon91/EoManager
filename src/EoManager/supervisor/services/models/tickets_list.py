import time
from os.path import split

from pydantic import BaseModel, field_validator
from supervisor.services.encoding.ticket_status import ticket_statuses


class Service(BaseModel):
    id: int  # id услуги
    name: str  # название услуги
    prefix: str  # префикс услуги


class OperatorWindow(BaseModel):
    id: int  # id окна
    name: str  # номер окна


class Specialist(BaseModel):
    id: int
    lastname: str
    firstname: str
    middlename: str
    employeestate: str = None  # статус сотрудника в виде кода
    operatorwindow: OperatorWindow = None


class Ticket(BaseModel):
    id: int  # id талона
    ticketnumber: int  # порядковый номер талона
    ticketcode: str  # номер талона, например, РП3
    recordstate: dict  # статус талона в виде кода
    recorddate: str  # дата на который день запись в формате yyyy-mm-dd
    recordtime: str = None  # время на которое сделана запись в формате hh:mm:ss
    createdate: int  # дата когда был создан талон
    statedate: int  # ???
    fio: str = None  # ФИО заявителя
    phone: str = None  # телефон заявителя
    email: str = None  # email заявителя
    servicegroup: Service  # услуга на которую выдан талон
    isprerecord: bool  # true в случае предварительной записи, false в случае текущей
    prerecordEmployee: Specialist = None  # сотрудник на которого прикрепилась предварительная запись (только ПЗ)
    queueDate: str  # время записи в формате dd.mm.yyyy hh:mm (ПЗ на какое время) (ТЗ когда талон создан)
    actualDate: str = None  # фактические дата и время вызова на приём в формате dd.mm.yyyy hh:mm
    normative: str = ''  # время норматива по оказанию услуги
    actualServingTime: str = ''  # время обслуживания
    creationDate: str
    waitTime: dict = {'wait': '0 мин. 0 сек.', 'status': 'green'}  # время ожидания заявителя в очереди в формате
    waitTimeExpired: bool = False
    recordtimeString: str = None
    employee: Specialist = None
    appointmentWaitThreshold: str = None # Приоритет талона

    @field_validator('queueDate', mode='before')
    @classmethod
    def transform_queueDate(cls, raw: str) -> str:
        return raw.split()[1]

    @field_validator('recordstate', mode='before')
    @classmethod
    def encoding_status(cls, status: str) -> dict:
        return ticket_statuses.get_dict(db_name=status)

    @field_validator('actualServingTime', mode='before')
    @classmethod
    def convert_actualServingTime(cls, serving_time: int) -> str:
        return time.strftime('%H:%M:%S', time.gmtime(serving_time / 1000))

    @field_validator('normative', mode='before')
    @classmethod
    def convert_normative(cls, normative_int: int) -> str:
        return time.strftime('%H:%M:%S', time.gmtime(normative_int / 1000))

    @field_validator('waitTime', mode='before')
    @classmethod
    def convert_wait_time(cls, wait_time: str) -> dict:
        h, m, s = map(int, wait_time.split(':'))
        m = h * 60 if h > 0 else m
        status = 'green'
        if m >= 10:
            status = 'yellow'
        if m >= 15:
            status = 'red'
        return {'wait': f'{m} мин. {s} сек.', 'status': status}


class Content(BaseModel):
    content: list[Ticket]

    @field_validator('content', mode='after')
    @classmethod
    def sorted_content(cls, content: list) -> list:
        return sorted(content, key=lambda ticket: ticket.queueDate)
