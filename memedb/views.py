from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from guardian.shortcuts import get_objects_for_user

from .forms import MemeCreateForm, MemeUpdateForm, MemeDeleteForm
from .models import Meme


class IndexView(TemplateView):
    template_name = "memedb/index.html"


class DashboardView(ListView):
    template_name = "memedb/dashboard.html"

    def get_queryset(self):
        qs = get_objects_for_user(self.request.user, "memedb.view_meme").order_by(
            "-created_at"
        )

        if search_tags_query := self.request.GET.get("q"):
            search_tags = [tag.strip() for tag in search_tags_query.split(",")]
            qs = qs.filter(tags__name__in=search_tags).distinct()

        return qs[:10]


class MemeListFragmentView(ListView):
    template_name = "memedb/meme_list_fragment.html"

    def get_queryset(self):
        qs = get_objects_for_user(self.request.user, "memedb.view_meme").order_by(
            "-created_at"
        )

        after = datetime.fromisoformat(self.request.GET.get("after"))

        ## since we sort by timestamp descending, we want results which were created
        ## before the cursor
        qs = qs.filter(created_at__lt=after)

        if search_tags_query := self.request.GET.get("q"):
            search_tags = [tag.strip() for tag in search_tags_query.split(",")]
            qs = qs.filter(tags__name__in=search_tags).distinct()

        return qs[:10]


class MemeCreateView(CreateView):
    template_name = "memedb/meme/create.html"
    model = Meme
    form_class = MemeCreateForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # set owner
        self.object.owner = self.request.user

        # set content
        content_ = form.cleaned_data.pop("content_")
        self.object.content_type = content_.content_type
        self.object.content = content_.read()

        # persist object
        self.object.save()

        # m2m
        ## Without this next line the tags won't be saved.
        form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())


class MemeUpdateView(UpdateView):
    template_name = "memedb/meme/update.html"
    model = Meme
    form_class = MemeUpdateForm
    success_url = reverse_lazy("dashboard")
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "memedb.change_meme")


class MemeDeleteView(DeleteView):
    template_name = "memedb/meme/delete.html"
    model = Meme
    form_class = MemeDeleteForm
    success_url = reverse_lazy("dashboard")
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "memedb.delete_meme")


class MemeContentView(DetailView):
    model = Meme
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "memedb.view_meme").defer()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        return HttpResponse(obj.content, content_type=obj.content_type)
