from django.urls import path
from .views import *

urlpatterns = [
    # Static pages
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('services/', ServicesPageView.as_view(), name='services'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('sign-in/', SignInPageView.as_view(), name='sign-in'),
    path('feedback/', FeedbackPageView.as_view(), name='feedback'),
    path('faqs/', FAQsPageView.as_view(), name='faqs'),
    path('support/', SupportPageView.as_view(), name='support'),
    path('admin-panel/', AdminPanelPageView.as_view(), name='admin-panel'),

    # ServiceCategory CRUD URLs
    path('service-categories/list/', ServiceCategoryListView.as_view(), name='service-category-list'),
    path('service-categories/<int:pk>/', ServiceCategoryDetailView.as_view(), name='service-category-detail'),
    path('service-categories/add/', ServiceCategoryCreateView.as_view(), name='service-category-create'),
    path('service-categories/<int:pk>/edit/', ServiceCategoryUpdateView.as_view(), name='service-category-update'),
    path('service-categories/<int:pk>/delete/', ServiceCategoryDeleteView.as_view(), name='service-category-delete'),

    # Service CRUD URLs
    path('services/list/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/add/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),
]
