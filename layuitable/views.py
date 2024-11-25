from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .hdfs_python_api import HDFSAPI
from pprint import pprint

hdfs_api = HDFSAPI()
# Create your views here.
def layuitable(request):
    return render(request,'layuitable.html')

def data_table(request):
    page = int(request.GET.get('page',0))
    limit = int(request.GET.get('limit',0))
    # student_data = [
    #         {"id": '001',"name": "张一",'gender':'男','age':18},
    #         {"id": '002',"name": "张二",'gender':'男','age':18},
    #         {"id": '003',"name": "张三",'gender':'女','age':17},
    #         {"id": '004',"name": "张四",'gender':'男','age':18},
    #         {"id": '005',"name": "张五",'gender':'男','age':18},
    #         {"id": '006',"name": "张六",'gender':'女','age':18},
    #         ]


    list_d =hdfs_api.list_df('/')
    obj_page = list_d[(page-1) * limit: page * limit]
    pprint(list_d)
    data = {
        "code": 0,
        "msg": "",
        "count": len(list_d),
        "data": obj_page
    }
    return JsonResponse(data)
@csrf_exempt
def login(request):
    username = request.POST.get('username1')
    pwd = request.POST.get('pwd1')
    authcode = request.POST.get('authcode1')
    if username == 'admin' and pwd == '123':
        data = {
            'code':1,
            'msg':'登录成功'
        }
        return JsonResponse(data)
    else:
        data = {
            'code':2,
            'msg':'登录失败'
        }
        return JsonResponse(data)
@csrf_exempt
def delete_f(request):
    #接受前端传递的参数
    df_name = request.POST.get('df_name')
    df_type = request.POST.get('df_type')
    print(df_name,df_type)
    pass
    #删除文件
    if str(df_name)[0] == '/' and len(str(df_name))== 1:
        data = {
            'code': 2,
            'msg': '根目录不能删除'
        }
        return JsonResponse(data)
    elif df_type == "FILE":
        d_path = "/" + df_name
        del_r = hdfs_api.def_file(d_path)
        if del_r:
            data = {
                'code': 1,
                'msg': '文件删除成功'
            }
            return JsonResponse(data)
        else:
            data = {
                'code': 2,
                'msg': '文件删除失败'
            }
    elif df_type == "DIRECTORY":
        d_path = "/" + df_name
        del_r = hdfs_api.def_file(d_path)
        if del_r == True:
            data = {
                'code': 1,
                'msg': '文件夹删除成功'
            }
            return JsonResponse(data)
        else:
            data = {
                'code': 2,
                'msg': '文件夹不为空'
            }
            return JsonResponse(data)