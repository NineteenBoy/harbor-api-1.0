# coding=utf8
# Autor : Alaways V
# Time : 2019/1/22 15:31 # File : harbor.py # Software PyCharm
import json
import urllib3
import requests
from pprint import pprint

urllib3.disable_warnings()

class HarborApi(object):
    def __init__(self, url, username, passwd, protocol="https"):
        '''
        init the request
        :param url: url address or doma
        :param username:
        :param passwd:
        :param protect:
        '''
        self.url = url
        self.username = username
        self.passwd =passwd
        self.protocol = protocol


    def login_get_session_id(self):
        '''
        by the login api to get the session of id
        :return:
        '''
        harbor_version_url = "%s://%s/api/systeminfo"%(self.protocol, self.url)
        header_dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0', \
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data_dict = {
            "principal": self.username,
            "password": self.passwd
        }
        v_req_handle = requests.get(harbor_version_url, verify=False)
        self.harbor_version = v_req_handle.json()["harbor_version"]
        pprint(self.harbor_version)
        if self.harbor_version.startswith("v1.4"):
            req_url = "%s://%s/login" % (self.protocol, self.url)
            self.session_id_key = 'beegosessionID'
        elif self.harbor_version.startswith("v1.7"):
            req_url = "%s://%s/c/login" % (self.protocol, self.url)
            self.session_id_key = "sid"
        else:
            raise ConnectionError("the %s version is not to supply!"%self.harbor_version)
        req_handle = requests.post(req_url, data=data_dict, headers=header_dict, verify=False)
        if 200 == req_handle.status_code:
            self.session_id = req_handle.cookies.get(self.session_id_key)
            return self.session_id
        else:
            raise Exception("login error,please check your account info!"+ self.harbor_version)


    def logout(self):
        requests.get('%s://%s/logout' %(self.protocol, self.url),
                     cookies={self.session_id_key: self.session_id})
        raise Exception("successfully logout")

    def project_info(self):
        project_url = "%s://%s/api/projects" %(self.protocol, self.url)
        req_handle = requests.get(project_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return req_handle.json()
        else:
            raise Exception("Failed to get the project info。")

    def repository_info(self, project_id):
        repository_url = '%s://%s/api/repositories?project_id=%s' %(self.protocol, self.url, project_id)
        req_handle = requests.get(repository_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return req_handle.json()
        else:
            raise Exception("Failed to get the repository info。")

    def tags_info(self, repository_name):
        tags_url = '%s://%s/api/repositories/%s/tags' %(self.protocol, self.url, repository_name)
        req_handle = requests.get(tags_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return req_handle.json()
        else:
            raise Exception("Failed to get the tags info。")

    def users_info(self):
        users_url = '%s://%s/api/users' %(self.protocol, self.url)
        req_handle = requests.get(users_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return req_handle.json()
        else:
            raise Exception("Failed to get the users info.")

    def project_members_info(self, project_id):
        project_members_url = '%s://%s/api/projects/%s/members' %(self.protocol, self.url, project_id)
        req_handle = requests.get(project_members_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return req_handle.json()
        else:
            raise Exception("Failed to get the project members info.")



harbor_api = HarborApi("xx.xx.xx.xx", "admin", "x")


#print(harbor_api)
harbor_api.login_get_session_id()
project_list = harbor_api.project_info()
#pprint(project_list[1])

#统计项目的仓库数量
'''for i in range(len(project_list)):
    project_name = project_list[i]['name']
    project_id = project_list[i]['project_id']
    repo_count = project_list[i]['repo_count']
    owner_id = project_list[i]['owner_id']
    print(project_name, project_id, repo_count, owner_id)   '''


#project_id = project_list[2]['project_id']
#project_id = '6'
#print(project_id)
#统计项目中所有镜像数量和下载次数
'''repo_list = harbor_api.repository_info(project_id)
for i in range(len(repo_list)):
    project_id = repo_list[i]['project_id']
    repo_name = repo_list[i]['name']
    tags_count = repo_list[i]['tags_count']
    pull_count = repo_list[i]['pull_count']
    print(project_id, repo_name, tags_count, pull_count) '''
#pprint(repo_list)

#统计用户信息
'''users_list = harbor_api.users_info()
for i in range(len(users_list)):
    user_id = users_list[i]['user_id']
    user_name = users_list[i]['username']
    role_name = users_list[i]['role_name']
    print(user_id, user_name, role_name)    '''

#查询项目成员和成员角色
#project_members_list = harbor_api.project_members_info(1)
#pprint(project_members_list)
#for i in range(len(project_members_list)):

