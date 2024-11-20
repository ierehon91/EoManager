from django.urls import path
from . import views


app_name = 'supervisor'

urlpatterns = [
    path('', views.tickets_list, name='tickets_list'),
    path('tickets/get/', views.fetch_tickets_list, name='fetch_tickets_list'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:id>/history/', views.fetch_ticket_history, name='fetch_ticket_history'),
    path('windows/', views.windows_list, name='windows_list'),
    path('windows/get/', views.fetch_windows_list, name='fetch_windows_list'),
    path('prerecord-free/', views.free_time_tickets_list, name='free_time_tickets_list'),
    path('prerecord-free/get/', 
         views.fetch_free_time_tickets_list, 
         name='fetch_free_time_tickets_list'
         ),
]
