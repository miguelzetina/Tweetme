from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django import forms
from django.forms.utils import ErrorList
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
                            CreateView,
                            DetailView,
                            DeleteView,
                            ListView,
                            UpdateView
                            )

from .mixins import FormUserNeededMixin, UserOwnerMixin
from .forms import TweetModelForm
from .models import Tweet
# Create your views here.


# class TweetCreateView(LoginRequiredMixin,  CreateView):
class TweetCreateView(FormUserNeededMixin, CreateView):
    # queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = "tweets/create_view.html"
    # success_url = "/tweet/create/"
    # fields = ["user", "content"]
    # login_url = "/admin/"


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = "tweets/update_view.html"
    # success_url = "/tweet/"

# Las vistas Create&Update necesitan especificar ya sea un succes_url en las clases,
# o bien, un get_absolute_url en el models.py

    # def form_valid(self, form):
    #    if self.request.user.is_autehnticated():
    #        form.instance.user = self.request.user
    #        return super(TweetCreateView, self).form_valid(form)
    #    else:
    #        form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(
    #            ["El usuario debe estar logeado para poder publicar un Tweet."])
    #        return self.form_invalid(form)


# def tweet_create_view(request):
#     form = TweetModelForm(request.POST or None)
#     if form.is_valid():
#        instance = form.save(commit=False)
#        instance.user = request.user
#        instance.save()
#    context = {
#        "form": form
#    }
#    return render(request, "tweets/create_view.html", context)

class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = "tweets/delete_confirm.html"
    success_url = reverse_lazy("tweet:list")


class TweetDetailView(DetailView):
    # template_name = "tweets/detail_view.html"
    # En caso de no especificar el nombre del template, se debe crear el html
    # con el nombre de la clase sin el "View"
    queryset = Tweet.objects.all()

    # def get_object(self):
    #    print(self.kwargs)
    #    pk = self.kwargs.get("pk")
    #    obj = get_object_or_404(Tweet, pk=pk)
    #    print(pk)
    #    # return Tweet.objects.get(id=pk)
    #    return obj


class TweetListView(ListView):
    # template_name = "tweets/list_view.html"
    # En caso de no especificar el nombre del template, se debe crear el html
    # con el nombre de la clase sin el "View"
    # queryset = Tweet.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.all()
        print(self.request.GET)
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        # context["another_list"] = Tweet.objects.all()
        # print(context)
        print(context)
        return context


# def tweet_detail_view(request, id=1):
#     obj = Tweet.objects.get(id=id)
#     obj = get_object_or_404(Tweet, pk=pk)
#     print(obj)
#     context = {
#         "object": obj
#     }
#     return render(request, "tweets/detail_view.html", context)
#
#
# def tweet_list_view(request):
#     queryset = Tweet.objects.all()
#     print(queryset)
#     for obj in queryset:
#         print(obj.content)
#     context = {
#         "object_list": queryset
#     }
#     return render(request, "tweets/list_view.html", context)
