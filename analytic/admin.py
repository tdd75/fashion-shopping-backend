from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse


# class AnalyticAdmin(admin.ModelAdmin):
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('analytic/', self.admin_site.admin_view(self.analytic_view))
#         ]
#         return my_urls + urls

#     def analytic_view(self, request):
#         context = dict(
#             # self.admin_site.each_context(request),
#             # key=value,
#         )
#         return TemplateResponse(request, "admin/analytic.html", context)
