from django.forms import ModelForm

from dds.models import DDSType


class DDSTypeForm(ModelForm):

    class Meta:
        model = DDSType
        fields = (
            'name',
        )