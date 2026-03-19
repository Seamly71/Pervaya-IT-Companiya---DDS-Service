from django.urls import path, include

from dds.views import ddstype


app_name = 'dds'

dds_type_patterns = [
    path(
        'create/',
        ddstype.DDSTypeCreateView.as_view(),
        name='create_dds_type'
    ),
    # path('<int:type_id>/delete/'),
    # path('<int:type_id>/update/'),
    path(
        '',
        ddstype.DDSTypeListView.as_view(),
        name='list_dds_type'
    ),
]

urlpatterns = [
    path('type/', include(dds_type_patterns)),
]
