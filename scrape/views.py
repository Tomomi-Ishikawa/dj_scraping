from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .forms import RequestForm
from .models import Request
from .views import Request
from django.views import generic
import pandas as pd
import uuid #id生成
from .tasks import start_task

class GetDate(generic.FormView):
    template_name = 'scrape/index.html'
    form_class =RequestForm

    def form_valid(self, form):
        # uuidを生成
        _uuid = str(uuid.uuid4())
        # gcs_bucket = 'gs://scr_django'
        # formオブジェクトの初期化
        f = form.save(commit=False)
        # formにuuidを保存
        f.uuid = _uuid  
        # f.url ='https'URLを渡すのも可
        task_id = start_task.delay(_uuid)
        print('task_id:', task_id) # 生成したuuidを別のところで処理するため値を引き渡す必要あり
        # formを保存
        f.save()

        context = {
            'url': form.cleaned_data['url'],
            'form': self.form_class,
            'name': f'scrapoo {datetime.today()}',
            'result': Request.objects.all().order_by('-date') #降順

        }
        return render(
            self.request,
            self.template_name,
            context
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = f'scrapoo {datetime.today()}'
        context['result'] = Request.objects.all().order_by('-date') #降順
        return context

def downloader(request, uuid):
    gcs_bucket = 'gs://scr_django'
    filename = f'{gcs_bucket}/{uuid}.pkl'
    df = pd.read_pickle(filename)

    res = HttpResponse(content_type='text/csv; charset=utf-8')
    file_name = f'{datetime.today()}_dj.csv'
    res['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{file_name}'
    df.to_csv(res, index=False) #　sep='\t'　← ,　処理をしている場合は\t の方が良い
    return res
    #return HttpResponse(df.to_html())

        #return HttpResponse({f'uuid : {uuid'})
 
# def index(request):
#     name = f'scrapoo {datetime.today()}'
#     form = RequestForm()
#     html = f'''
#     <h1>Hello {name}</h1>
#     <hr>
#     {form}
#     <hr>
#     <button>Requests</button>
#     '''
#     return HttpResponse(html)
