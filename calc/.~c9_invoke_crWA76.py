from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Status
from .forms import StatusForm

#ANSES：一覧のためのモデルのリスト
#asn：編集のための任意のデータの変数

def index(request):
  d = {
      'Statuses': Status.objects.all(),
  }
  return render(request, 'calc/index.html', d)

def add(request):
    form = StatusForm(request.POST or None)
    if form.is_valid():
      Status.objects.create(**form.cleaned_data)
      return redirect('index')

    d = {
        'form': form,
    }
    return render(request, 'calc/edit.html', d)
    
def edit(request, editing_id):
    status = get_object_or_404(Status, id=editing_id)
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            status.hp = form.cleaned_data['hp']
            status.mp = form.cleaned_data['mp']
            status.event = form.cleaned_data['event']
            status.ap = status.hp * status.mp/100
            status.save()
            return redirect('index')
    else:
        # GETリクエスト（初期表示）時はDBに保存されているデータをFormに結びつける
        form = StatusForm({'hp': status.hp},{'mp': status.mp},{'event': status.event})
    d = {
        'form': form,
    }

    return render(request, 'calc/edit.html', d)

#@require_POST    
def delete(request, editing_id):
#    ans = get_object_or_404(ANS, id=editing_id)
#    ans.delete()
    return redirect('index')

#@require_POST    
def calc(request):
    #calc2.htmlで入力されたものを計算する
    if request.method == 'POST':#これをしないとcalc.htmlを開いたときに勝手にPOSTしようとする
        dmg = int(request.POST['dmg'])
        nhp = p1hp - dmg
    #答えを新しいレコードに記録
        Status.objects.create(hp=nhp)
        return redirect('index')
        
    d = {
        #'form': form,
        'p1hp': p1hp,
        'p2hp': p2hp,
    }
    return render(request, 'calc/calc.html', d)
    
def calc2(request):
    #calc2.htmlに入力したものを計算して登録

    if request.method == 'POST':#これをしないとcalc.htmlを開いたときに勝手にPOSTしようとする
        ihp = int(request.POST['hp'])
        imp = int(request.POST['mp'])
        iap = ihp * imp/100
        event = str(request.POST)
    #答えを新しいレコードに記録
        Status.objects.create(ap=iap, hp=ihp, mp=imp, event=)
        return redirect('index')
        
    d = {
        #'form': form,
    }
    return render(request, 'calc/calc2.html', d)