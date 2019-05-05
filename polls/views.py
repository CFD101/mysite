from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# DELETE FUNCTION
# def delete(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     question.delete()
#     return redirect('index')

def newpoll(request):
    q_text = str(request.POST['question_wording'])
    q_choice1 = str(request.POST['choice1'])
    q_choice2 = str(request.POST['choice2'])
    q_choice3 = str(request.POST['choice3'])
    q = Question(question_text=q_text, pub_date=timezone.now())
    q.save()
    q.choice_set.create(choice_text=q_choice1, votes=0)
    q.choice_set.create(choice_text=q_choice2, votes=0)
    q.choice_set.create(choice_text=q_choice3, votes=0)
    q.save()
    q_id=q.id
    question = get_object_or_404(Question, pk=q_id)
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponseRedirect(render(request, 'polls/detail.html', {'question': q}))
    #return HttpResponseRedirect(request, 'polls/detail.html',{'question': q})
    #return HttpResponseRedirect(template.render(request, 'polls/detail.html', {'question': q}))
    #return HttpResponseRedirect('polls/detail.html',{'question': q})
    #return HttpResponseRedirect(reverse('polls/index.html'))
    #return HttpResponseRedirect(reverse('polls:index'))
    #return HttpResponseRedirect(reverse('polls:details', q.id))
    #return render('polls/detail.html', q.id)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
