from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Status, Index
from .forms import StatusForm, IndexForm
from django.http import HttpResponse
import io
import datetime
import numpy as np
import matplotlib.pyplot as plt

#ANSES：一覧のためのモデルのリスト
#asn：編集のための任意のデータの変数

def index(request):
  d = {
      'Statuses': Status.objects.order_by('-id'),
      'Indexes': Index.objects.all(),
  }
  return render(request, 'calc/index.html', d)

def detail(request, pk):
    status = get_object_or_404(Status, pk=pk)
    return render(request, 'calc/detail.html', {'status': status})
    
def add(request):
    form = StatusForm(request.POST or None)
    if form.is_valid():
      Status.objects.create(**form.cleaned_data)
      return redirect('apcalc:index')

    d = {
        'form': form,
    }
    return render(request, 'calc/edit.html', d)
    
def edit(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            status.hp = form.cleaned_data['hp']
            status.mp = form.cleaned_data['mp']
            status.event = form.cleaned_data['event']
            status.ap = status.hp * status.mp/100
            status.save()
            return redirect('apcalc:index')
    else:
        # GETリクエスト（初期表示）時はDBに保存されているデータをFormに結びつける
        form = StatusForm(instance=status)
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
def calc(request):#apcalcにアプデ
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
        return redirect('apcalc:index')
        
    d = {
        #'form': form,
        'p1hp': p1hp,
        'p2hp': p2hp,
    }
    return render(request, 'calc/calc.html', d)
    
def apcalc(request):
    #calc2.htmlに入力したものを計算して登録
    rStatus = Status.objects.order_by('id').reverse()[:1]#過去1回分のレコードを抽出
    p1ap = rStatus[0].ap#1つ前の答え
    p1hp = rStatus[0].hp
    p1mp = rStatus[0].mp
    p1ev = rStatus[0].event
    p1tm = rStatus[0].updated_at
    
    if request.method == 'POST':#これをしないとcalc.htmlを開いたときに勝手にPOSTしようとする
        ihp = int(request.POST['hp'])
        imp = int(request.POST['mp'])
        iap = ihp * imp/100
        ievent = str(request.POST['event'])
        clossap = iap - p1ap
        cdmg = ihp - p1hp
        cusemp = imp - p1mp
        cbehavior = str(p1ev)
        #term = datetime.datetime.now() - p1tm #DateTimeFieldに直したい
    #答えを新しいレコードに記録
        Status.objects.create(ap=iap, hp=ihp, mp=imp, event=ievent)
        Index.objects.create(lossap=clossap, dmg=cdmg, usemp=cusemp, behavior=cbehavior)
        return redirect('apcalc:index')
        
    d = {
        'rStatus': rStatus,
        'p1ap': p1ap,
        'p1hp': p1hp,
        'p1mp': p1mp,
        'p1ev': p1ev,
        'p1tm': p1tm,
    }
    return render(request, 'calc/ap.html', d)
    
def graph(request):
    #apv = Status[:10].ap
    rStatus = Status.objects.all()
    y=[]#ap
    x=[]#id
    for i in range(len(rStatus)):
        ap=rStatus[i].ap
        y.append(ap)
        n=rStatus[i].id
        x.append(n)
        
    ap = np.array(y)
    num = np.array(x)
    plt.plot(num, ap)
    
    return render(request, 'calc/graph.html')
    
#png画像形式に変換数関数
def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    s = buf.getvalue()
    buf.close()
    return s

#画像埋め込み用view
def img_plot(request):
    # matplotを使って作図する

    ax = plt.subplot()
    png = plt2png()
    plt.cla()
    response = HttpResponse(png, content_type='image/png')
    return response