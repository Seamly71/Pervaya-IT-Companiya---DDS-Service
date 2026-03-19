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
        max_length=DDS_STATUS_NAME_MAX_LENGTH,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'ДДС статус'
        verbose_name_plural = 'ДДС статусы'

    def __str__(self):
        return self.name


class DDSType(models.Model):
    name = models.CharField(
        unique=True,
        max_length=DDS_TYPE_NAME_MAX_LENGTH,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'ДДС тип'
        verbose_name_plural = 'ДДС типы'

    def __str__(self):
        return self.name


class DDSCategory(models.Model):
    name = models.CharField(
        unique=True,
        max_length=DDS_CATEGORY_NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    parent_type = models.ForeignKey(
        DDSType,
        on_delete=models.CASCADE,
        to_field='name',
        related_name='categories',
        verbose_name='Родительский тип'
    )

    class Meta:
        verbose_name = 'ДДС категория'
        verbose_name_plural = 'ДДС категории'

    def __str__(self):
        return self.name


class DDSSubcategory(models.Model):
    name = models.CharField(
        unique=True,
        max_length=DDS_SUBCATEGORY_NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    parent_category = models.ForeignKey(
        DDSCategory,
        on_delete=models.CASCADE,
        to_field='name',
        related_name='subcategories',
        verbose_name='Родительская категория'
    )

    class Meta:
        verbose_name = 'ДДС подкатегория'
        verbose_name_plural = 'ДДС подкатегории'

    def __str__(self):
        return self.name


class DDSEntry(models.Model):
    created_at = models.DateField(
        null=True,
        blank=True,
        default=now,
        verbose_name='Дата создания'
    )
    status = models.ForeignKey(
        DDSStatus,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        to_field='name',
        verbose_name='Статус'
    )
    type = models.ForeignKey(
        DDSType,
        on_delete=models.RESTRICT,
        to_field='name',
        verbose_name='Тип'
    )
    category = models.ForeignKey(
        DDSCategory,
        on_delete=models.RESTRICT,
        to_field='name',
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        DDSSubcategory,
        on_delete=models.RESTRICT,
        to_field='name',
        verbose_name='Подкатегория'
    )
    sum = models.DecimalField(
        max_digits=DDS_SUM_MAX_DIGITS,
        decimal_places=DDS_SUM_DECIMAL_PLACES,
        verbose_name='Сумма'
    )
    comment = models.TextField(
        blank=True,
        max_length=DDS_COMMENT_MAX_LENGTH,
        verbose_name='Комментарий'
    )

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        super().full_clean()

        if self.subcategory.parent_category != self.category:
            raise ValidationError(
                f'Подкатегория записи - {self.subcategory} '
                f'и ее категория - {self.category} не согласованы.'
            )
        if self.category.parent_type != self.type:
            raise ValidationError(
                f'Категория записи - {self.category} '
                f'и ее тип - {self.type} не согласованы.'
            )

    class Meta:
        default_related_name = 'entries'
        verbose_name = 'ДДС запись'
        verbose_name_plural = 'ДДС записи'

    def __str__(self):
        return f'{self.created_at}: {self.sum}'