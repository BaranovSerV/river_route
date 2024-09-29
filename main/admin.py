from django.contrib import admin
from .models import Topic
from django.db.models import Count, Avg
from django.utils.html import format_html
from django.urls import path
from .models import Report

# Регистрация модели Topic
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Поля, отображаемые в списке
    search_fields = ('title', 'content')  # Поля, по которым можно выполнять поиск
    list_filter = ('created_at', 'author')  # Поля для фильтрации
    ordering = ('-created_at',)  # Порядок сортировки в списке

    # Дополнительная возможность удалять посты
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        # Логика удаления
        for obj in queryset:
            obj.delete()
        self.message_user(request, "Выбранные посты были успешно удалены.")

    delete_selected.short_description = "Удалить выбранные посты"



class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at', 'updated_at')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('report-stats/', self.admin_site.admin_view(self.report_stats), name='report-stats'),
        ]
        return custom_urls + urls

    def report_stats(self, request):
        # Получение статистики
        total_reports = Report.objects.count()
        reports_by_status = Report.objects.values('status').annotate(count=Count('status'))
        avg_time_to_close = Report.objects.filter(status='closed').aggregate(avg_duration=Avg('updated_at'))

        # Форматирование вывода
        stats_html = "<h2>Статистика отчетов</h2>"
        stats_html += f"<p>Общее количество отчетов: {total_reports}</p>"
        stats_html += "<h3>Отчеты по статусу:</h3><ul>"
        for item in reports_by_status:
            stats_html += f"<li>{item['status'].capitalize()}: {item['count']}</li>"
        stats_html += "</ul>"

        if avg_time_to_close['avg_duration']:
            stats_html += f"<p>Среднее время на выполнение закрытых отчетов: {avg_time_to_close['avg_duration']}</p>"

        # Вернуть HTML для отображения в админке
        return format_html(stats_html)

# Регистрация модели в админке
admin.site.register(Report, ReportAdmin)