from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    FormView,
)
from guardian.shortcuts import get_objects_for_user

from memedb.services import find_suggested_tags, cache_content_comparison_hash

from .forms import (
    MemeCreateForm,
    MemeUpdateForm,
    MemeDeleteForm,
    MemeCreateSuggestedTagsForm,
)
from .models import Meme


class IndexView(TemplateView):
    template_name = "memedb/index.html"


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "memedb/dashboard.html"

    def get_queryset(self):
        qs = get_objects_for_user(self.request.user, "memedb.view_meme").order_by(
            "-created_at"
        )

        if search_tags_query := self.request.GET.get("q"):
            search_tags = [tag.strip() for tag in search_tags_query.split(",")]
            qs = qs.filter(tags__name__in=search_tags).distinct()

        return qs[:10]


class MemeListFragmentView(LoginRequiredMixin, ListView):
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


class MemeCreateView(LoginRequiredMixin, CreateView):
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

        # cache comparison hash
        cache_content_comparison_hash(self.object)

        # persist object
        self.object.save()

        # m2m
        ## Without this next line the tags won't be saved.
        form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())


class MemeCreateSuggestedTagsView(LoginRequiredMixin, FormView):
    template_name = "memedb/meme/create_suggested_tags_fragment.html"
    form_class = MemeCreateSuggestedTagsForm

    def form_valid(self, form):
        context = self.get_context_data()

        content_ = form.cleaned_data.pop("content_")
        content_type = content_.content_type
        content = content_.read()

        user = self.request.user

        context["tags"] = find_suggested_tags(user, content, content_type)

        return self.render_to_response(context)


class MemeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "memedb/meme/update.html"
    model = Meme
    form_class = MemeUpdateForm
    success_url = reverse_lazy("dashboard")
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "memedb.change_meme")


class MemeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "memedb/meme/delete.html"
    model = Meme
    form_class = MemeDeleteForm
    success_url = reverse_lazy("dashboard")
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "memedb.delete_meme")


class MemeContentView(LoginRequiredMixin, DetailView):
    model = Meme
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "memedb.view_meme").defer()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        return HttpResponse(obj.content, content_type=obj.content_type)
