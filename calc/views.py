from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Status, Index
from .forms import StatusForm, IndexForm
import io
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import codecs

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
        #ihp = int(request.POST['hp'])
        #imp = int(request.POST['mp'])
        ifood = int(request.POST['food'])
        imedicine = int(request.POST['medicine'])
        isleep = int(request.POST['sleep'])
        ihappy = int(request.POST['happy'])
        istress = int(request.POST['stress'])
        iworry = int(request.POST['worry'])
        iiritate = int(request.POST['iritate'])
        irefuresh = int(request.POST['refuresh'])
        itired = ((ihappy+irefuresh)+((6-istress)+(6-iworry)+(6-iiritate)))/5
        ihp = 100 * (((ifood/3)+(isleep/7))/2)
        imp = 100 * itired/5
        iap = ihp * imp/100
        ievent = str(request.POST['event'])
        clossap = iap - p1ap
        cdmg = ihp - p1hp
        cusemp = imp - p1mp
        cbehavior = str(p1ev)
        #now= datetime.now()
        #term = now.timestamp() - p1tm.timestamp() #DateTimeFieldに直したい
    #答えを新しいレコードに記録
        Status.objects.create(ap=iap, hp=ihp,food=ifood, medicine=imedicine, sleep=isleep, happy=ihappy, stress=istress , worry=iworry, iritate=iiritate, tired=itired, refuresh=irefuresh, mp=imp, event=ievent)
        #r2Status = Status.objects.order_by('id').reverse()[:1]#過去1回分のレコードを抽出
        #tm = r2Status[0].updated_at
        #term = tm.timestamp() - p1tm.timestamp()
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
    return render(request, 'calc/apc.html', d)
    
def graph(request):
    #apv = Status[:10].ap
    rStatus = Status.objects.all()
    y=[]#ap
    x=[]#id
    for i in range(len(rStatus)):#スマートなやり方じゃないかも
        ap=rStatus[i].ap
        y.append(ap)
        n=rStatus[i].id
        x.append(n)
        
    ap = np.array(y)
    num = np.array(x)
    plt.plot(num, ap)
    
    return render(request, 'calc/graph.html')
    
def graph_hp(request):
    rStatus = Status.objects.all()
    y=[] #hp
    x=[] #id
    for i in range(len(rStatus)): #スマートなやり方じゃないかも
        hp=rStatus[i].hp
        y.append(hp)
        n=rStatus[i].id
        x.append(n)
        
    hp = np.array(y)
    num = np.array(x)
    plt.plot(num, hp)
    
    return render(request, 'calc/graph_hp.html')

def graph_mp(request):
    rStatus = Status.objects.all()
    y=[] #hp
    x=[] #id
    for i in range(len(rStatus)): #スマートなやり方じゃないかも
        mp=rStatus[i].mp
        y.append(mp)
        n=rStatus[i].id
        x.append(n)
        
    mp = np.array(y)
    num = np.array(x)
    plt.plot(num, mp)
    
    return render(request, 'calc/graph_mp.html')

def graph_all(request):
    graph(request)
    graph_hp(request)
    graph_mp(request)

    return render(request, 'calc/graph_all.html')

#png画像形式に変換数関数
def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
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

import neologdn
import numpy as np
import MeCab
import pickle
from gensim.models import word2vec
import re

def wakati(request):
    rStatus = Status.objects.all()
    tagger = MeCab.Tagger(' -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('') 

    corpus = []
    for i in range(len(rStatus)):#スマートなやり方じゃないかも
        event=rStatus[i].event
        if event is not None:
            node = tagger.parseToNode(event)
        else:
            continue
        #print(event)
        word_list = []
        while node :
            pos = node.feature.split(",")[0]
            if pos in ["名詞", "動詞", "形容詞"]:   # 対象とする品詞
                word = node.feature.split(",")[6]
                word_list.append(word)
            node = node.next
        corpus.append(word_list)
    #print(corpus) #[['起床'], ['朝食'], ['自作', 'アプリ', '作成'], ['test'], ['グラフ', '見る', 'やすい', 'よう'], ['昼食'], 
    
    model = word2vec.Word2Vec(corpus, size=100, min_count=2, window=2) #毎回作り直してる
    model.save("myw2v.model")

    word_to_id = {}
    id_to_word = {}
    for sentence in corpus:
        for word in sentence:
            if word not in word_to_id:#新しい単語を追加するためのコード
                    new_id = len(word_to_id)
                    word_to_id[word] = new_id
                    id_to_word[new_id] = word
    #print('id',id_to_word)
    #print('word',word_to_id)
    corpus2=[]
    for i in range(len(corpus)):
        s_corpus = np.array([word_to_id[w] for w in corpus[i]])
        corpus2.append(s_corpus)
    #print(corpus2) #[array([0]), array([1]), array([2, 3, 4]), array([5]), array([ 6,  7,  8,  9, 10, 11]), ...])]
    mydic = [corpus, corpus2, word_to_id, id_to_word]
    file_name = 'mydic' + '.pkl'
    with open(file_name, 'wb') as f:
            pickle.dump(mydic, f)
            
    d = {
        'corpus': corpus, #リスト形式
        'id2word': id_to_word, #辞書型
    }
    return render(request, 'calc/corpus.html', d)   

from HPcalc.settings import MODEL_FILE_PATH1, MODEL_FILE_PATH2

def w2vin(request):
    if request.method == 'POST':#これをしないとcalc.htmlを開いたときに勝手にPOSTしようとする
        iwd = str(request.POST['word'])

        model1 = word2vec.Word2Vec.load(MODEL_FILE_PATH1) #wiki.modelじゃないとdef get_vectorが上手く働かない
        model2 = word2vec.Word2Vec.load(MODEL_FILE_PATH2) #自分のコーパスより、myw2v.modelから

        #results = model.wv.most_similar(positive=['純粋','悪'],negative=['正義'])
        results1 = model1.most_similar([iwd])    
        results2 = model2.most_similar([iwd])    
        #results=iwd

        d={
            'results1':results1,
            'results2':results2, 
            }

        return render(request, 'calc/w2vout.html', d)

    return render(request, 'calc/w2vin.html')

def w2vout(request):

    return render(request, 'calc/w2vout.html')

def w2v_corpus(request):
    model1 = word2vec.Word2Vec.load(MODEL_FILE_PATH1) #wiki.modelじゃないとdef get_vectorが上手く働かない
    model2 = word2vec.Word2Vec.load(MODEL_FILE_PATH2) #自分のコーパスより、myw2v.modelから
    w2v_corpus1 = model1.wv.index2word
    w2v_corpus2 = model2.wv.index2word
    d = {
        'w2v_corpus1':w2v_corpus1,
        'w2v_corpus2':w2v_corpus2,
    }
    return render(request, 'calc/w2v_corpus.html', d)

"""
def test(request): #word2vec
    
    自分の語彙と一般的な語彙の乖離を見たい。
    =>wiki.modelだけで良さそう=>自分の近い語彙で調べて他の言葉を探す
    0.コーパスファイルをw2vファイルに変換=>ニューラルネットワークを使ったディープラーニングが必要
    ：(one-hot=>共起行列=>コサイン類似、PPMI=>SVD)=>DeepLearning
    *PPMIをすると日本の助詞問題も解決するのでは？=>日本語はw2vで行う。英語はdoc2vecへ進む。
    1．wiki.model(modelファイル)を使ったword2vec
    2．mydic.pklを使ったword2vec
    2-1. 入出力画面の作成
    2-2. urlの作成
    2-3. コードの作成, ref:def apcalc
    

    if request.method == 'POST':#これをしないとcalc.htmlを開いたときに勝手にPOSTしようとする
        iwd = str(request.POST['word'])

    model = word2vec.Word2Vec.load(MODEL_FILE_PATH) #wiki.modelじゃないとdef get_vectorが上手く働かない

    #results = model.wv.most_similar(positive=['純粋','悪'],negative=['正義'])
    results = model.most_similar([iwd])

    d = {
        'results': results
    }

    return render(request, 'calc/w2vout.html', d)
"""