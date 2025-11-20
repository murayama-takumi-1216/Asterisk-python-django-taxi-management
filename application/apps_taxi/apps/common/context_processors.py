from apps import __subversion__, __version__


def version_control_js_settings(request):
    return {
        "version_control_js": "jsv={}.{}".format(__version__, __subversion__),
    }
