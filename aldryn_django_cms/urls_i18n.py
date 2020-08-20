from django.urls import include, re_path


urlpatterns = [
    re_path(r'^api/~select2/', include('django_select2.urls')),

    # required by aldryn-forms
    re_path(r'^api/~captcha/', include('captcha.urls')),
]
