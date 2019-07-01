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
    #使用する値
    #form = ANSForm(request.POST or None)#ここで使用するformを定義
    rStatus = Status.objects.order_by('id').reverse()[:2]#過去2回分のレコードを抽出
    #もし無ければ手入力する画面を表示
    p1hp = rStatus[0].hp#1つ前の答え
    p2hp = rStatus[1].hp#2つ前の答え
    #計算
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