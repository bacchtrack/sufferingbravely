from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Link
from .models import Vote#new

from .forms import LinkForm
from .forms import VoteForm#new

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.views.generic.edit import FormView#new

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

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

class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    form_class = LinkForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.rank_score = 0.0
        f.submitter = self.request.user
        f.save()
        return super(LinkCreateView, self).form_valid(form)

#TO DO: make sure only submitter can edit
class LinkUpdateView(UpdateView):
    model = Link
    form_class = LinkForm

class LinkDeleteView(DeleteView):
    model = Link
    success_url = reverse_lazy('home')

class VoteFormView(FormView):
    form_class = VoteForm

    def form_valid(self, form):
        link = get_object_or_404(Link, pk=form.data["link"])
        user = self.request.user
        prev_votes = Vote.objects.filter(voter=user, link=link)
        has_voted = (prev_votes.count()>0)

        if not has_voted:
            #add vote
            Vote.objects.create(voter=user, link=link)
            print("voted")
        else:
            #delete vote
            prev_votes[0].delete()
            print("unvoted")
        return redirect("home")
    
    def form_invalid(self, form):
        print("invlaid")
        return redirect("home")

 #   link_names = list()

  #  for link in links:
   #     link_names.append(link.title)

    #response_html = '<br>'.join(link_names)

   # return HttpResponse(response_html)