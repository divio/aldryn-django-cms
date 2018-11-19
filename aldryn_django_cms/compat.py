try:
    # Django>=2.0
    from django.urls import url, include
except ImportError:
    from django.conf.urls import url, include
