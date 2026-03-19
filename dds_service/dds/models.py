from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


DDS_STATUS_NAME_MAX_LENGTH = 50
DDS_TYPE_NAME_MAX_LENGTH = 50
DDS_CATEGORY_NAME_MAX_LENGTH = 50
DDS_SUBCATEGORY_NAME_MAX_LENGTH = 50
DDS_SUM_MAX_DIGITS = 11
DDS_SUM_DECIMAL_PLACES = 2
DDS_COMMENT_MAX_LENGTH = 2000


class DDSStatus(models.Model):
    name = models.CharField(
        unique=True,
        max_length=DDS_STATUS_NAME_MAX_LENGTH
    )


class DDSType(models.Model):
    name = models.CharField(
        unique=True,
        max_length=DDS_TYPE_NAME_MAX_LENGTH
    )


class DDSCategory(models.Model):
    name = models.CharField(
        unique=True,
        max_length=DDS_CATEGORY_NAME_MAX_LENGTH
    )
    parent_type = models.ForeignKey(
        DDSType,
        on_delete=models.CASCADE,
        to_field='name',
        related_name='categories'
    )


class DDSSubcategory(models.Model):
    name = models.CharField(
        unique=True,
        max_length=DDS_SUBCATEGORY_NAME_MAX_LENGTH
    )
    parent_category = models.ForeignKey(
        DDSCategory,
        on_delete=models.CASCADE,
        to_field='name',
        related_name='subcategories'
    )


class DDSEntry(models.Model):
    created_at = models.DateField(
        null=True,
        blank=True,
        default=now
    )
    status = models.ForeignKey(
        DDSStatus,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        to_field='name'
    )
    type = models.ForeignKey(
        DDSType,
        on_delete=models.RESTRICT,
        to_field='name'
    )
    category = models.ForeignKey(
        DDSCategory,
        on_delete=models.RESTRICT,
        to_field='name'
    )
    subcategory = models.ForeignKey(
        DDSSubcategory,
        on_delete=models.RESTRICT,
        to_field='name'
    )
    sum = models.DecimalField(
        max_digits=DDS_SUM_MAX_DIGITS,
        decimal_places=DDS_SUM_DECIMAL_PLACES
    )
    comment = models.TextField(
        blank=True,
        max_length=DDS_COMMENT_MAX_LENGTH
    )

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        super().full_clean()

        if self.subcategory.parent_category != self.category:
            raise ValidationError(
                f'Entries subcategory - {self.subcategory} '
                f'and category - {self.category} are not conforming.'
            )
        if self.category.parent_type != self.type:
            raise ValidationError(
                f'Entries category - {self.category} '
                f'and type - {self.type} are not conforming.'
            )

    class Meta:
        default_related_name = 'entries'