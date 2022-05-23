from django.contrib import admin

class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        query = self.request.GET.get('q')
        return super().index(request, extra_context=extra_context)