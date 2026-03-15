from django.contrib import admin
from .models import *
from django.utils.html import format_html


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False

    readonly_fields = [field.name for field in OrderItem._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    inlines = [OrderItemInline]
    fields = [field.name for field in Order._meta.fields if field.name != "receipt"] + ["receipt_copy"]

    readonly_fields = [field.name for field in Order._meta.fields if field.name != "receipt"] + ["receipt_copy"]

    def receipt_copy(self, obj):
        if not obj.receipt:
            return "-"

        return format_html(
        '''
        <div style="display:flex;flex-direction:column;gap:6px;">
            <img src="{}" style="width:50vw;border-radius:6px;" />
        </div>
        ''',
        obj.receipt,
    )

    receipt_copy.short_description = "Receipt"

    def has_add_permission(self, request):
        return False


admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Message)