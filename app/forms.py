from django import forms

from .models import Recruit, ShadowHand, Sith


class RecruitForm(forms.ModelForm):
    class Meta:
        model = Recruit
        fields = ('name', 'age', 'planet', 'email')


class QuestionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        question = ShadowHand.objects.filter(recruit=None)
        for quest in question:
            field_name = quest.question
            self.fields[field_name] = forms.CharField(max_length=30)

    def save(self, recruit):
        for quest in ShadowHand.objects.filter(recruit=None):
            ShadowHand.objects.create(recruit=recruit, question=quest.question,
                                      answer=self.cleaned_data[quest.question])


class ChooseSithForm(forms.Form):
    query = list()
    for sith in Sith.objects.all():
        if len(Recruit.objects.filter(sith=sith)) < 3:
            query.append(Sith.objects.filter(name=sith.name))
    print(query)
    if len(query) == 0:
        comb_query = Sith.objects.none()
    else:
        comb_query = query[0]
        for q in query[1:]:
            comb_query = comb_query.union(q)
    choose_sith = forms.ModelChoiceField(queryset=comb_query)


class ChooseRecruitForm(forms.Form):
    choose_recruit = forms.ModelChoiceField(queryset=Recruit.objects.filter(sith=None).order_by('name'))
