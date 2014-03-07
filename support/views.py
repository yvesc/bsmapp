from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from userdash.views import get_balance
from django.template import RequestContext
from support.forms import *
from django.http import HttpResponseRedirect, Http404

@login_required()
def support(request):
	try:
		support = ReplaySupport.objects.select_related('ticket').filter(ticket__user=request.user).order_by('-ticket__id')
	except:
		support = {}

	return render_to_response('support_ticket.html', {'user_balance':get_balance(request), 'support':support}, RequestContext(request))

@login_required()
def add_support_ticket(request):
	if request.method == 'GET':
		form = SupportForm()
		form_ask = ReplaySupportForm()
		return render_to_response('support_add_ticket.html', {'user_balance':get_balance(request), 'form':form, 'form_ask':form_ask}, RequestContext(request))
	else:
		form = SupportForm(request.POST)
		if form.is_valid():
			instance = TicketSupport(user=request.user, type_support=TypeSupport.objects.get(pk=request.POST.get('type_support')), subject=request.POST.get('subject'))
			instance.save()
			instance_ask = ReplaySupport(ticket=TicketSupport.objects.get(pk=instance.pk), user=request.user, body=request.POST.get('body'))
			instance_ask.save()
			return HttpResponseRedirect('/dashboard-cust/support')
		else:
			return render_to_response('support_add_ticket.html', {'user_balance':get_balance(request), 'form':form}, RequestContext(request))

@login_required()
def view_support_ticket(request, ticket_id):
	if request.method == 'GET':
		try:
			ticket = TicketSupport.objects.get(pk=ticket_id)
		except:
			raise Http404

		try:
			support = ReplaySupport.objects.select_related('ticket').filter(ticket=ticket_id).order_by('-pk')
		except:
			support = {}

		form = ReplaySupportForm()
		return render_to_response('support_view_ticket.html', {'user_balance':get_balance(request), 'support':support, 'form':form, 'ticket':ticket}, RequestContext(request))
	else:
		form = ReplaySupportForm(request.POST)
		if form.is_valid():
			instance = ReplaySupport(user=request.user, ticket=TicketSupport.objects.get(pk=request.POST.get('idsupport')), body=request.POST.get('body'))
			instance.save()
			return HttpResponseRedirect('/dashboard-cust/view-support-ticket/' + request.POST.get('idsupport'))
		else:
			return render_to_response('support_view_ticket.html', {'user_balance':get_balance(request), 'support':support, 'form':form}, RequestContext(request))