from django.urls import path
from .views import JobCreateView, JobDetailView, JobSearchView

urlpatterns = [
    path("", JobCreateView.as_view(), name="create-job"),
    path("search/", JobSearchView.as_view(), name="search-job"),
    path("<int:pk>/", JobDetailView.as_view(), name="job-detail"),
]
