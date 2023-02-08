from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path

from .models import ChatMessage


@staff_member_required
def admin_statistics_view(request):
    return render(request, 'admin/chat/inbox.html', {
        'title': 'Inbox'
    })


class InboxSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                'name': 'Inbox',
                'app_label': 'inbox',
                'models': [
                    {
                        'name': 'Inbox',
                        'object_name': 'chat',
                        'admin_url': '/admin/inbox',
                        'view_only': True,
                    }
                ],
            }
        ]
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('statistics/', admin_statistics_view, name='admin-statistics'),
        ]
        return urls
