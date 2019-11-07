from django.core.mail import send_mail
from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from app.models import Planet, ShadowHand, Recruit, Sith
from .forms import RecruitForm, QuestionForm, ChooseSithForm, ChooseRecruitForm


def main_page(request):
    planets = Planet.objects.all()
    return render(request, 'app/main_page.html', {'planets': planets})


@csrf_exempt
def recruit(request):
    if request.method == "POST" and request.POST.get('name'):
        form = RecruitForm(request.POST)
        if form.is_valid():
            current_recruit = form.save()
            request.session['recruit'] = current_recruit.email
            form1 = QuestionForm()
            return render_to_response('app/recruit.html', {'recruit': current_recruit, 'form': form1})
    elif request.method == "POST":
        email = request.session.get('recruit')
        recruit1 = Recruit.objects.get(pk=email)
        form1 = QuestionForm(request.POST)
        if form1.is_valid():
            for quest in ShadowHand.objects.filter(recruit=None):
                ShadowHand.objects.create(recruit=recruit1, question=quest.question,
                                          answer=form1.cleaned_data[quest.question])
        return redirect('main_page')
    else:
        form = RecruitForm()
        return render(request, 'app/recruit.html', {'form': form})


def sith(request):
    if request.method == "POST" and request.POST.get('choose_sith'):  # check !!!!
        form = ChooseSithForm(request.POST)
        if form.is_valid():
            choosen_sith = form.cleaned_data['choose_sith']
            request.session['sith'] = choosen_sith.name
            form1 = ChooseRecruitForm()
            quest_list = list()
            if len(Recruit.objects.filter(sith=None)) == 0:
                quest_list.append('There are no free recruits')
            else:
                for cur_recruit in Recruit.objects.filter(sith=None):
                    quest_list.append('Recruit : ' + cur_recruit.name)
                    for quest in ShadowHand.objects.filter(recruit=cur_recruit):
                        quest_list.append(quest.question + ': ')
                        quest_list.append(quest.answer)
                    quest_list.append('\n')
                print(quest_list)
            return render(request, 'app/sith.html', {'form': form1, 'quest_list': quest_list})
    elif request.method == "POST":
        form1 = ChooseRecruitForm(request.POST)
        if form1.is_valid():
            choosen_recruit = form1.cleaned_data['choose_recruit']
            choosen_recruit = Recruit.objects.get(pk=choosen_recruit.email)
            sith_name = request.session.get('sith')
            choosen_sith = Sith.objects.get(pk=sith_name)
            choosen_recruit.sith = choosen_sith
            choosen_recruit.save()
            print(choosen_recruit.email)
            send_mail('sub', 'mes', 'bars.sith1@gmail.com', [choosen_recruit.email], fail_silently=False)
        return redirect('main_page')
    else:
        form = ChooseSithForm()
        return render(request, 'app/sith.html', {'form': form})


def sithinfo(request):
    list_all_sith = list()
    list_sith_with_sh = list()
    for sith in Sith.objects.all():
        sh = len(Recruit.objects.filter(sith=sith))
        list_all_sith.append(sith.name + ' ' + str(sh))
        if sh > 0:
            list_sith_with_sh.append(sith.name)
    return render(request, 'app/sithinfo.html',
                  {'list_all_sith': list_all_sith, 'list_sith_with_sh': list_sith_with_sh})
