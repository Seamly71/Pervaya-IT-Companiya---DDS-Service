from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from dds.models import DDSType
from dds.forms import DDSTypeForm


class DDSTypeMixin:
    model = DDSType
    pk_url_kwarg = 'type_id'
    success_url = reverse_lazy('dds:list_dds_type')


class DDSTypeFormMixin:
    form_class = DDSTypeForm


class DDSTypeCreateView(DDSTypeMixin, DDSTypeFormMixin, CreateView):
    template_name = 'dds_type/form.html'


class DDSTypeListView(DDSTypeMixin, ListView):
    template_name = 'dds_type/list.html'