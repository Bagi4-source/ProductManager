import logging
from import_export.resources import ModelResource
from django.contrib import admin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Products
from django import forms
from import_export.admin import ImportExportModelAdmin


class ProductsAdminForm(forms.ModelForm):
    spu_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'spu_id или ссылка'}), label="spuId / URL")
    override_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Замена названия'}), label="Название",
                                     required=False)
    override_brand = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Заменить бренда'}), label="Бренд",
                                     required=False)

    class Meta:
        model = Products
        fields = '__all__'


class ProductsResource(ModelResource):
    class Meta:
        model = Products
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("spu_id",)
        fields = ['spu_id', 'override_title', 'override_brand']


@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    resource_classes = [ProductsResource]
    form = ProductsAdminForm
    search_fields = ["spu_id", "override_title", "override_brand"]
    list_display = ("spu_id", "override_title", "override_brand", "create_time",)
    readonly_fields = ("create_time",)
    date_hierarchy = "create_time"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('spu_id',) + self.readonly_fields
        return self.readonly_fields
