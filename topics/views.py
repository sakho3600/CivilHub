from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from places_core.mixins import LoginRequiredMixin
from .models import Discussion, Entry
from .forms import ReplyForm


class DiscussionDetailView(DetailView):
    """
    Single discussion page as forum page.
    """
    model = Discussion

    def get_context_data(self, **kwargs):
        topic = super(DiscussionDetailView, self).get_object()
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        replies = Entry.objects.filter(discussion=topic)
        paginator = Paginator(replies, 25)
        page = self.request.GET.get('page')
        try:
            context['replies'] = paginator.page(page)
        except PageNotAnInteger:
            context['replies'] = paginator.page(1)
        except EmptyPage:
            context['replies'] = paginator.page(paginator.num_pages)
        context['form'] = ReplyForm(initial={
            'discussion': topic.slug
        })
        context['title'] = topic.question
        return context


def reply(request, slug):
    """
    Create forum reply.
    """
    if request.method == 'POST' and request.POST:
        post = request.POST
        topic = Discussion.objects.get(slug=post['discussion'])
        entry = Entry(
            content = post['content'],
            creator = request.user,
            discussion = topic,
        )
        try:
            entry.save()
        except:
            return HttpResponse('There was some errors')
    return HttpResponseRedirect(reverse('discussion:details', kwargs={'slug': topic.slug,}))
