import hdfs.util
from hdfs import Client
from pprint import pprint

class HDFSAPI():
    #定义属性
    def __init__(self):
        self.client = Client(url="http://192.168.10.10:9870")
        print("返回操作HDFS对象",self.client)
    #方法（行为)
    #时间戳
    def time_transform(self, num):
        import time
        #将其转换成秒
        times =float(num / 1000)
        #转换
        time_array = time.localtime(times)
        #时间格式转换
        time_style = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return time_style
    #文件大小单位转换
    def file_size_transform(self, num):
        unit = ['B', 'KB', 'MB','GB','TB']
        for i in range(len(unit)):
            if num / 1024 < 1:
                return "%.2f %s" % (num, unit[i])
            num /= 1024
    # list() 相当于shell ls
    def list_df(self,h_path):
        try:
            list_d=dict(self.client.list(hdfs_path=h_path,status=True))
        except hdfs.util.HdfsError as e:
            return e
        else: #try中没有异常就执行else
            list_select_data =[
                dict(
                    filename=v['pathSuffix'],
                    modifitime=self.time_transform(v['modificationTime']),
                    filesize=self.file_size_transform(v['length']),
                    filetype=v['type']
                )
                for v in list_d.values()
            ]
            return list_select_data
            # return list_d.values()
        finally:
            print("不管有没有报错都执行")

    def def_file(self,h_path):
        try:
            del_result = self.client.delete(hdfs_path=h_path)
        except hdfs.util.HdfsError as e:
            return e
        else:
            return del_result

if __name__ == "__main__":
    #实例化类
    hdfsapi = HDFSAPI()
    #调用方法
    # h_path = input("请输入HDFS上的一个文件路径")
    # pprint(hdfsapi.list_df(h_path))
    h_path = input("请输入要删除的文件路径")
    print(hdfsapi.def_file(h_path))



