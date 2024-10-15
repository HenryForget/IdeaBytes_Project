from django.urls import path
from . import views
from .views import device_Options

urlpatterns = [
    # path('plot_general/', views.plot_general_view, name='plot_general'),
    path('threshold/', views.device_thresholds, name='device_thresholds'),
    # path('show/', views.show_graphs, name='show_graphs'),
    # path('devices/', device_Options, name='device_options'),
]