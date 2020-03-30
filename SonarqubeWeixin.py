#!/usr/bin/python
#_*_coding:utf-8 _*_

import requests,sys,json,os
requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')

#获取Token
def GetToken(Corpid,Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid": Corpid,
        "corpsecret": Secret
    }
    r = requests.get(url=Url,params=Data,verify=False)
    Token = r.json()['access_token']
    return Token

#将获取到的趋势图，上传至企业微信临时素材，返回MediaId发送图文消息是使用
def GetImageUrl(Token,Path):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image" % Token
    data = {
        "media": open(Path,'r')
        }
    r = requests.post(url=Url,files=data)
    dict = r.json()
    return dict['media_id']

#文本消息
def SendTextMessage(Token,User,Agentid,Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                 # 企业号中的用户帐号
        "msgtype": "text",                          # 消息类型
        "agentid": Agentid,                             # 企业号中的应用id
        "text": {
            "content": Content
        },
    "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text


#卡片消息
def SendCardMessage(Token,User,Agentid,Subject,Content,Detail_url):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                 # 企业号中的用户帐号
        "msgtype": "textcard",                          # 消息类型
        "agentid": Agentid,                             # 企业号中的应用id
        "textcard": {
            "title": Subject,
            "description": Content,
            "url": Detail_url,          #点击详情后打开的页面
            "btntxt": "点击查看详情"
        },
    "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text

#图文消息news
def SendnewsMessage(Token,User,Agentid,Subject,Content,History_url,Pic_url):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
            "touser": User,                                 # 企业号中的用户帐号
            "msgtype": "news",                            # 消息类型
            "agentid": Agentid,                             # 企业号中的应用id
            "news": {
                    "articles": [
                    {
                            "title": Subject,
                            "description": Content,
                            "picurl": Pic_url,
                            "url": History_url,      #点击阅读原文后，打开趋势图大图，第一次需要登录
                    }
                    ]
            },
            "safe": "0"
    }
    headers = {'content-type': 'application/json'}
    data = json.dumps(Data,ensure_ascii=False).encode('utf-8')
    r = requests.post(url=Url,headers=headers,data=data)
    return r.text

#图文消息mpnews
def SendmpnewsMessage(Token,User,Agentid,Subject,Content,Media_id,history_url):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
            "touser": User,                                 # 企业号中的用户帐号
            "msgtype": "mpnews",                            # 消息类型
            "agentid": Agentid,                             # 企业号中的应用id
            "mpnews": {
                    "articles": [
                    {
                            "title": Subject,
                            "thumb_media_id": Media_id,
                            "content": Content,
                            "content_source_url": history_url,      #点击阅读原文后，打开趋势图大图，第一次需要登录
                            "digest": Content,
                            "show_cover_pic": "1"
                    }
                    ]
            },
            "safe": "1"
    }
    headers = {'content-type': 'application/json'}
    data = json.dumps(Data,ensure_ascii=False).encode('utf-8')
    r = requests.post(url=Url,headers=headers,data=data)
    return r.text

#提交审批
def SendApproval(Token,Creator_userid, Template_id, Project_name, Branch_name, Branch_commit, Image_name, Image_tag, Option_id, Platform_type):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/oa/applyevent?access_token=%s" % Token
    Data = {
    	"creator_userid": Creator_userid,
    	"template_id": Template_id,
    	"use_template_approver": 1,
    	#"approver": [
    	#    {
    	#        "attr": 2,
    	#        "userid": ["WuJunJie","WangXiaoMing"]
    	#    },
    	#    {
    	#        "attr": 1,
    	#        "userid": ["LiuXiaoGang"]
    	#    }
    	#],
    	#"notifyer":[ "WuJunJie","WangXiaoMing" ],
    	#"notify_type" : 1,
    	"apply_data": {
    	    "contents":[
                {
    	            "control": "Text",
    	            "id": "Text-1581492024088",
    	            "title": [
    	                {
    	                    "text": "项目名称",
    	                    "lang": "zh_CN"
    	                }
    	            ],
    	            "value": {
    	                "text": Project_name.strip()
    	            }
    	        },
    	        {
    	           "control": "Selector",
    	           "id": "Selector-1581492416321",
    	           "title": [
    	               {
    	                   "text": "发布环境",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
                       "selector": {
	           	"type": "single",
                             "options": [
                                  {
                                      "key": Option_id
                                  }
                              ]
	               }
    	           }
    	        },
    	        {
    	           "control": "Text",
    	           "id": "Text-1581492549750",
    	           "title": [
    	               {
    	                   "text": "代码分支",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
    	               "text": Branch_name.strip()
    	           }
    	        },
    	        {
    	           "control": "Text",
    	           "id": "Text-1581492572185",
    	           "title": [
    	               {
    	                   "text": "Commit",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
    	               "text": Branch_commit.strip()
    	           }
    	        },
    	        {
    	           "control": "Text",
    	           "id": "Text-1581492656710",
    	           "title": [
    	               {
    	                   "text": "镜像名称",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
    	               "text": Image_name.strip()
    	           }
    	        },
    	        {
    	           "control": "Text",
    	           "id": "Text-1581492696732",
    	           "title": [
    	               {
    	                   "text": "镜像tag",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
    	               "text": Image_tag.strip()
    	           }
    	        }
            ]
        },
         "summary_list": [
            {
                "summary_info": [{
                    "text": "项目名称: %s" %Project_name ,
                    "lang": "zh_CN"
                }]
            },
            {
                "summary_info": [{
                    "text": "发布环境: %s" %Platform_type ,
                    "lang": "zh_CN"
                }]
            },
            { "summary_info": [{
                    "text": "镜像名称: %s:%s" %(Image_name, Image_tag),
                    "lang": "zh_CN"
                }]
            }

        ]
    }

    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text

#获取审批模板详情
def GetTemplateDetail(Token, Template_id):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/oa/gettemplatedetail?access_token=%s" % Token
    Data = {
        "template_id": Template_id
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text

#解析sonarqube扫描结果
def SonarqubeDetail(sonar_url, project_name):
    api_url = sonar_url + "/api/measures/search?projectKeys=" + project_name + "&metricKeys=alert_status%2Cbugs%2Creliability_rating%2Cvulnerabilities%2Csecurity_rating%2Ccode_smells%2Csqale_rating%2Cduplicated_lines_density%2Ccoverage%2Cncloc%2Cncloc_language_distribution"
    # 获取sonar指定项目结果
    resopnse = requests.get(api_url).text
    # 转换成josn
    result = json.loads(resopnse)
    bug = 0
    leak = 0
    code_smell = 0
    coverage = 0
    density = 0
    security = 0
    
    status = ''
    statusStr = ''

# 解析sonar json结果
    for item in result['measures']:
        #bug
        if item['metric'] == "bugs":
            bug = item['value'].strip()
        #漏洞数
        elif item['metric'] == "vulnerabilities":
            leak = item['value'].strip()
        #可能存在问题代码行数
        elif item['metric'] == 'code_smells':
            code_smell = item['value'].strip()
        #覆盖率
        elif item['metric'] == 'coverage':
            coverage = item['value'].strip()
        #重复率
        elif item['metric'] == 'duplicated_lines_density':
            density = item['value'].strip()
        #安全漏洞
        elif item['metric'] == 'security_rating':
            security = item['value'].strip()
        #状态
        elif item['metric'] == 'alert_status':
            status = item['value'].strip()
    return status, bug, leak, code_smell, security, coverage, density

if __name__ == "__main__":
    Corpid = os.getenv('PLUGIN_CORPID')
    Secret = os.getenv('PLUGIN_CORP_SECRET')
    Agent_id = os.getenv('PLUGIN_AGENT_ID')
    Project_name = os.getenv('DRONE_REPO')
    Repo_name = os.getenv('DRONE_REPO_NAME')
    Branch_name = os.getenv('DRONE_COMMIT_BRANCH')
    Build_num = os.getenv('DRONE_BUILD_NUMBER')
    Token = GetToken(Corpid,Secret)
    Sonar_url = os.getenv('PLUGIN_SONAR_URL')
    To_user = os.getenv('PLUGIN_TO_USER')

    Detail_url = '%s/dashboard?id=%s' %(Sonar_url, Repo_name)
    status, bug, leak, code_smell, security, coverage, density = SonarqubeDetail(Sonar_url, Repo_name)

    # 判断新代码质量阀状态
    title = ''
    description = ''
    if status == 'OK':
        title = "✅恭喜, 代码[%s]-分支[%s]#%s 扫描通过~👍" %(Repo_name, Branch_name, Build_num)
        description = """
Bug数: <div class=\"highlight\">%s 个</div><br>
漏洞数: <div class=\"highlight\">%s 个</div><br>
可能存在问题代码行数: <div class=\"highlight\">%s 行</div><br>
安全漏洞: <div class=\"highlight\">%s 个</div><br>
覆盖率: <div class=\"highlight\">%s%%</div><br>
重复率: <div class=\"highlight\">%s%%</div>
""" %(bug, leak, code_smell, security, coverage, density)
        print "代码扫描成功！！！"
        res = SendCardMessage(Token, To_user, Agent_id, title, description, Detail_url)
        res_dict = json.loads(res)
        if res_dict['errcode'] == 0:
            print 'Send Message success!!!'
            print 'Status: %s \nBug数: %s \n漏洞数: %s \n可能存在问题代码行数: %s \n安全漏洞: %s \n覆盖率: %s \n重复率: %s' %(status,bug, leak, code_smell, security, coverage, density)
        else:
            print 'Send Approval error!!! Detail: %s' %res_dict
            print 'Status: %s \nBug数: %s \n漏洞数: %s \n可能存在问题代码行数: %s \n安全漏洞: %s \n覆盖率: %s \n重复率: %s' %(status,bug, leak, code_smell, security, coverage, density)
            sys.exit(1)

    elif status == 'ERROR':
        title = "❌真遗憾, 代码[%s]-分支[%s]#%s 扫描未通过~😭" %(Repo_name, Branch_name, Build_num)
        description = """
Bug数: <div class=\"highlight\">%s 个</div><br>
漏洞数: <div class=\"highlight\">%s 个</div><br>
可能存在问题代码行数: <div class=\"highlight\">%s 行</div><br>
安全漏洞: <div class=\"highlight\">%s 个</div><br>
覆盖率: <div class=\"highlight\">%s%%</div><br>
重复率: <div class=\"highlight\">%s%%</div>
""" %(bug, leak, code_smell, security, coverage, density)

        print "代码扫描失败！！！请修改后代码重新提交构建!!!!"
        res = SendCardMessage(Token, To_user, Agent_id, title, description, Detail_url)
        res_dict = json.loads(res)
        if res_dict['errcode'] == 0:
            print 'Send Message success!!!'
            print 'Status: %s \nBug数: %s \n漏洞数: %s \n可能存在问题代码行数: %s \n安全漏洞: %s \n覆盖率: %s \n重复率: %s' %(status,bug, leak, code_smell, security, coverage, density)
            sys.exit(1)
        else:
            print 'Send Approval error!!! Detail: %s' %res_dict
            print 'Status: %s \nBug数: %s \n漏洞数: %s \n可能存在问题代码行数: %s \n安全漏洞: %s \n覆盖率: %s \n重复率: %s' %(status,bug, leak, code_smell, security, coverage, density)
            sys.exit(1)

