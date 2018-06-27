from django.shortcuts import render
from django.http import HttpResponse
from .models import Link
from .forms import LinkForm
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from django.views.generic import ListView 
from django.views.generic import DetailView #new
#def home(request):
#    links = Link.objects.all()
 #   return render(request, 'home.html', {'links':links})

class LinkListView(ListView):
    model = Link
    queryset = Link.with_votes.all()

class LinkDetailView(DetailView):
    model = Link

class LinkCreateView(CreateView):
    model = Link
    form_class = LinkForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.rank_score = 0.0
        f.submitter = self.request.user
        f.save()
        return super(LinkCreateView, self).form_valid(form)

class LinkUpdateView(UpdateView):
    model = Link
    form_class = LinkForm

class LinkDeleteView(DeleteView):
    model = Link
    success_url = reverse_lazy('home')

 #   link_names = list()

  #  for link in links:
   #     link_names.append(link.title)

    #response_html = '<br>'.join(link_names)

   # return HttpResponse(response_html)