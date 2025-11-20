# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views import defaults as default_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Chrome DevTools - return empty JSON to avoid 404s
    path(
        ".well-known/appspecific/com.chrome.devtools.json",
        lambda request: JsonResponse({}),
        name="chrome-devtools",
    ),
    path("", include("apps.common.urls", namespace="common")),
    path("app/", include("apps.core_app.urls", namespace="core_app")),
    path(
        "app-reportes/",
        include("apps.core_app_reportes.urls", namespace="core_app_reportes"),
    ),
    path("app-turno/", include("apps.core_turno.urls", namespace="core_app_turno")),
    path(
        "app-servicio/",
        include("apps.core_servicio.urls", namespace="core_app_servicio"),
    ),
    path(
        "app-operador/",
        include("apps.core_operador.urls", namespace="core_app_operador"),
    ),
    path(
        "app-conductor/",
        include("apps.core_conductor.urls", namespace="core_conductor"),
    ),
    path(
        "app-vehiculo/",
        include("apps.core_vehiculo.urls", namespace="core_vehiculo"),
    ),
    path(
        "app-mantenimiento/",
        include("apps.core_app_mantenimiento.urls", namespace="core_app_mantenimiento"),
    ),
    path("webhook/", include("apps.webhook.urls", namespace="webhook")),
    # User management URLs
    path("users/", include("apps.users.urls", namespace="users")),
    # Django-allauth URLs
    path("accounts/", include("allauth.urls")),
    # TODO falta verificar y completar
    path(settings.ADMIN_URL, admin.site.urls),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

urlpatterns = [
    path(settings.APPLICATION_PATH, include(urlpatterns)),
]
