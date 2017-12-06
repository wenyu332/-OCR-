#coding=utf-8
# 同步图片检测服务接口, 会实时返回检测的结果

from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20170112 import ImageSyncScanRequest
import json
import uuid
import datetime

import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("F:/ComputerNetwork/sample/aliyun.ak.conf")
# 请替换成你自己的accessKeyId、accessKeySecret, 您可以类似的配置在配置文件里面，也可以直接明文替换
clt = client.AcsClient(cf.get("AK", "accessKeyId"), cf.get("AK", "accessKeySecret"),'cn-shanghai')
region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
request = ImageSyncScanRequest.ImageSyncScanRequest()
request.set_accept_format('JSON')

# 同步现支持单张图片，即一个task
task1 = {"dataId": str(uuid.uuid1()),
         "url":"http://tupian.enterdesk.com/2015/mxy/5/20/41/10.jpg",
         "time":datetime.datetime.now().microsecond
        }

request.set_content(bytearray(json.dumps({"tasks": [task1], "scenes": ["ocr"]}), "utf-8"))

response = clt.do_action_with_exception(request)
result = json.loads(response)
print result
if 200 == result["code"]:
    taskResults = result["data"]
    for taskResult in taskResults:
        if (200 == taskResult["code"]):
            sceneResults = taskResult["results"]

            for sceneResult in sceneResults:
                scene = sceneResult["scene"]
                suggestion = sceneResult["suggestion"]
                data=sceneResult['ocrData']
                print suggestion
                print scene
                print data[0]
                #根据scene和suggetion做相关的处理
                #do something
