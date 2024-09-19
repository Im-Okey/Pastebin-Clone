import json

from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .models import Tag
from .forms import TagForm


# ----------------------------------------------------------------------------
# main page
def index(request):
    tags = Tag.objects.all()
    return render(request, 'blog/index.html', {'tags': tags})
# ----------------------------------------------------------------------------





# ----------------------------------------------------------------------------
# tags
class TagListView(ListView):
    model = Tag
    template_name = 'tag_list.html'


class TagCreateView(CreateView):
    model = Tag
    fields = ['name']
    http_method_names = ['post']  # Разрешаем только POST-запросы

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        tag = self.model.objects.create(name=data['name'])
        return JsonResponse({'success': True, 'tag': {'id': tag.id, 'name': tag.name}})

class TagUpdateView(UpdateView):
    model = Tag
    fields = ['name']
    http_method_names = ['put']  # Разрешаем только PUT-запросы

    def put(self, request, *args, **kwargs):
        tag = self.get_object()
        data = json.loads(request.body)
        tag.name = data['name']
        tag.save()
        return JsonResponse({'success': True, 'tag': {'id': tag.id, 'name': tag.name}})

class TagDeleteView(DeleteView):
    model = Tag
    http_method_names = ['delete']  # Разрешаем только DELETE-запросы

    def delete(self, request, *args, **kwargs):
        tag = self.get_object()
        tag.delete()
        return JsonResponse({'success': True})
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# comments
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# categories
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# posts
# ----------------------------------------------------------------------------
