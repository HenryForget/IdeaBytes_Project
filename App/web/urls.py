from django.urls import path
from .webapp import views

urlpatterns = [
    # path('plot_general/', views.plot_general_view, name='plot_general'),
    path('threshold/', views.device_thresholds, name='device_thresholds'),
    # path('show/', views.show_graphs, name='show_graphs'),

]
