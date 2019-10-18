from django.conf.urls import patterns

urlpatterns = patterns(
    'iwork.views',
    (r'^$', 'home'),
    (r'save_record', 'save_record'),
    (r'records', 'records'),
)
