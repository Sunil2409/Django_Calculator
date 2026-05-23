from django.contrib import admin

from .models import CalculationHistory


@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):
    """Admin interface for CalculationHistory model."""
    list_display = ("user", "num1", "operation", "num2", "result", "created_at")
    list_filter = ("operation", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)
