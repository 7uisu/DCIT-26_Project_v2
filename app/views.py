from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *

class HomePageView(TemplateView):
    template_name = 'app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all categories and their related services
        categories = ServiceCategory.objects.all()
        context['categories'] = categories
        return context

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ServicesPageView(TemplateView):
    template_name = 'app/services.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'

class SignInPageView(TemplateView):
    template_name = 'app/sign-in.html'

class FeedbackPageView(TemplateView):
    template_name = 'app/feedback.html'

class FAQsPageView(TemplateView):
    template_name = 'app/faqs.html'

class SupportPageView(TemplateView):
    template_name = 'app/support.html'

class AdminPanelPageView(TemplateView):
    template_name = 'app/admin-panel.html'


# ListView: Display all service categories
class ServiceCategoryListView(ListView):
    model = ServiceCategory
    template_name = 'app/service-category/category_list.html'
    context_object_name = 'categories'

# DetailView: Display details of a single service category
class ServiceCategoryDetailView(DetailView):
    model = ServiceCategory
    template_name = 'app/service-category/category_detail.html'
    context_object_name = 'category'

# CreateView: Add a new service category
class ServiceCategoryCreateView(CreateView):
    model = ServiceCategory
    template_name = 'app/service-category/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('service-category-list')

# UpdateView: Edit an existing service category
class ServiceCategoryUpdateView(UpdateView):
    model = ServiceCategory
    template_name = 'app/service-category/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('service-category-list')

# DeleteView: Delete a service category
class ServiceCategoryDeleteView(DeleteView):
    model = ServiceCategory
    template_name = 'app/service-category/category_confirm_delete.html'
    success_url = reverse_lazy('service-category-list')

# ListView: Display all services
class ServiceListView(ListView):
    model = Service
    template_name = 'app/services/service_list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch categories to be able to display them in the template
        categories = ServiceCategory.objects.all()
        context['categories'] = categories
        return context

# DetailView: Display details of a single service
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'app/services/service_detail.html'
    context_object_name = 'service'

# CreateView: Add a new service
class ServiceCreateView(CreateView):
    model = Service
    template_name = 'app/services/service_form.html'
    fields = ['category', 'name', 'description', 'price', 'image']  # Include 'image' field
    success_url = reverse_lazy('service-list')

# UpdateView: Edit an existing service
class ServiceUpdateView(UpdateView):
    model = Service
    template_name = 'app/services/service_form.html'
    fields = ['category', 'name', 'description', 'price', 'image']  # Include 'image' field
    success_url = reverse_lazy('service-list')

# DeleteView: Delete a service
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'app/services/service_confirm_delete.html'
    success_url = reverse_lazy('service-list')
