from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.detail import DetailView

from .models import Order

from apps.comment.models import Comment
from project.custom_mixins import HasOrderPermissionMixin


from django.forms import ModelForm


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ["comment"]


class OrderListView(LoginRequiredMixin, ListView):

    model = Order

    def get_queryset(self):

        status_id = self.kwargs["status_id"]
        queryset = self.model.objects.filter(
            status=status_id, owner=self.request.user)

        return queryset

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        context["status_type"] = self.kwargs['status_id']

        return context


class OrderDetailView(LoginRequiredMixin, HasOrderPermissionMixin, DetailView):

    model = Order

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        # context["comments"] = CommentListView().get_queryset()
        context["comments"] = Comment.objects.filter(order=self.object.pk)
        context["form"] = CommentForm()

        return context


class OrderCreateView(LoginRequiredMixin, CreateView):

    model = Order
    fields = ['title', 'description']

    def get_success_url(self):
        return reverse('order:orders-list', kwargs={'status_id': self.object.status}, current_app='order')

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.owner = self.request.user

        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, HasOrderPermissionMixin, UpdateView):

    model = Order
    fields = ['title', 'description']

    def get_success_url(self):
        # return reverse('order:orders-detail', args=[self.object.pk], current_app='order')
        return reverse('order:orders-detail', kwargs={'pk': self.object.pk}, current_app='order')


class OrderDeleteView(LoginRequiredMixin, HasOrderPermissionMixin, DeleteView):

    model = Order
    template_name = 'confirm_delete.html'

    status_id = None

    def get_success_url(self):
        return reverse('order:orders-list', kwargs={"status_id": self.status_id}, current_app='order')

    def delete(self, request, *args, **kwargs):

        self.status_id = self.get_object().status
        return super().delete(request, *args, **kwargs)
