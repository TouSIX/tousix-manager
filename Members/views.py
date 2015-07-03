# -*- coding: utf8 -*-
__author__ = 'remy'
from formtools.wizard.views import CookieWizardView
from Members.forms import MemberForm, BillingForm, TechnicalForm, NOCForm, RouterForm


class CreateMemberView(CookieWizardView):

    template_name = 'inscription_membre.html'
    form_list = [MemberForm, RouterForm, BillingForm, NOCForm, TechnicalForm]


    def done(self, form_list, form_dict, **kwargs):
        # Create object for filling missing values
        member = form_dict['0'].save(commit=False)
        if form_dict['2'].isempty is False:
            billing = form_dict['2'].save()
            member.billing_id = billing.pk
        if form_dict['3'].isempty is False:
            noc = form_dict['3'].save()
            member.noc_id = noc.pk
        if form_dict['4'].isempty is False:
            technical = form_dict['4'].save()
            member.technical_id = technical.pk
        member.save()

        router = form_dict['1'].save(commit=False)
        router.idmembre_id = member.pk
        router.save()
