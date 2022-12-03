from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView, UpdateView
from .filters import RequestFilter
from .forms import *
from .models import Request, Category


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


class LogoutView(LogoutView):
    template_name = "registration/logout.html"


def index(request):
    request_in_proqress = Request.objects.all().filter(status='in proqress').count()
    requests_completed = Request.objects.filter(status='completed')

    class Meta:
        ordering = ['date']

    return render(request, 'index.html',
                  context={'requests_completed': requests_completed,
                           'request_in_proqress': request_in_proqress})


class Profile(LoginRequiredMixin, generic.ListView):

    model = Request
    template_name = 'profile.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Request.objects.all()
        else:
            return Request.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RequestFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CreateRequests(CreateView):
    template_name = 'requests.html'
    form_class = CreateRequestForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        fields = form.save(commit=True)
        fields.user = self.request.user
        fields.save()
        return super().form_valid(form)


class RequestUpdate(UpdateView):
    model = Request
    template_name = 'editing.html'
    success_url = reverse_lazy('profile')


def request_update(request, pk, st):
    newRequest = Request.objects.get(id=pk)
    newRequest.save()

    if st == 'completed':
        if request.method == 'POST':
            form = DonePhotoRequests(request.POST, request.FILES)
            if form.is_valid():
                newRequest.photo_done = form.cleaned_data['photo_done']
                newRequest.status = st
                newRequest.save()
                return redirect('profile')
        else:
            form = DonePhotoRequests()
        return render(request, 'editing.html', {'form': form})

    if st == 'in proqress':
        if request.method == 'POST':
            form = CommitRequests(request.POST, request.FILES)
            if form.is_valid():
                newRequest.text_commit = form.cleaned_data['text_commit']
                newRequest.status = st
                newRequest.save()
                return redirect('profile')
        else:
            form = CommitRequests()
        return render(request, 'editing.html', {'form': form})


class RequestDelete(DeleteView):
    model = Request
    template_name = 'request_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        object_instance = self.get_object()
        object_user = request.user
        if object_user != object_instance.user and request.status_verbose() != 'Новая':
            return HttpResponseForbidden('Permission Error')
        else:
            return render(request, 'request_confirm_delete.html')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html',
                  context={'categories': categories})


class CreateCategory(CreateView):
    template_name = 'category.html'
    form_class = CreateCategoryForm
    success_url = reverse_lazy('category_list')


class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')






