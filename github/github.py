#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import re
import shutil

__author__ = 'Devin(http://zhangchuzhao.site)'

"""
1、GitHub文件在线访问地址
https://github.com/zhuifengshen/AppSetting/blob/master/settingview.PNG
2、添加获取真实访问地址的参数
https://github.com/zhuifengshen/AppSetting/blob/master/settingview.PNG?raw=true
3、返回文件在GitHub上的真实访问地址
https://raw.githubusercontent.com/zhuifengshen/AppSetting/master/settingview.PNG

4、非master分支的情况
https://github.com/zhuifengshen/zhangchuzhao/blob/gh-pages/img/home-bg-o.jpg
https://raw.githubusercontent.com/zhuifengshen/zhangchuzhao/gh-pages/img/home-bg-o.jpg

5、常见Markown文档示例
picture reference
![mind_mapping1](images/xmind1.png)  # 相对路径图片资源，需要替换
![mind_mapping](http://images/xmind.png)  # 完整路径图片资源，不需要替换
![mind_mapping](images/xmind.png)
![mind_mapping](https://images/xmind.png)
file reference
[parse_xmind.py](example/parse_xmind.py)  # 相对路径文件资源，需要替换
[parse_xmind.py](http://example/parse_xmind.py)  # 完整文件资源路径，不需要替换
[parse_xmind.py](example/parse_xmind.py)
[parse_xmind.py](https://example/parse_xmind.py)

6、Markdown文档中通过相对路径引用项目中的图片资源
![mind_mapping](images/xmind.png)  # 替换前
![mind_mapping](https://raw.githubusercontent.com/zhuifengshen/xmind/master/images/xmind.png)  # 替换后

7、Markdown文档中通过相对路径引用项目中的文件资源
[parse_xmind.py](example/parse_xmind.py)  # 替换前
[parse_xmind.py](https://github.com/zhuifengshen/xmind/blob/master/example/parse_xmind.py)  # 替换后
"""


# 全局变量
project = ''  # 项目名
branch = 'master'  # 项目分支名
user_name = 'zhuifengshen'  # 默认用户名
relative_path = ''  # 资源在项目中的相对路径


# 资源匹配正则表达式
http_url_regexp = re.compile(r"^https?://", re.I)
github_url_regexp = re.compile(r'^https?://github.com/.*?[.].*?', re.I)
file_relative_url_regexp = re.compile(r'[^!]\[.*?\]\(([^http].*?)\)')
pic_relative_url_regexp = re.compile(r'!\[.*?\]\(([^http].*?)\)')


def get_absolute_path(path):
    """
        Return the absolute path of a file

        If path contains a start point (eg Unix '/') then use the specified start point
        instead of the current working directory. The starting point of the file path is
        allowed to begin with a tilde "~", which will be replaced with the user's home directory.
    """
    fp, fn = os.path.split(path)
    if not fp:
        fp = os.getcwd()
    fp = os.path.abspath(os.path.expanduser(fp))
    return os.path.join(fp, fn)


def get_file_online_url(m):
    """将Markdown文档中相对路径的文件引用，替换为上传GitHub后的在线访问地址"""
    global relative_path
    path, filename = os.path.split(relative_path)
    url = 'https://github.com/' + user_name + '/' + project + '/blob/' + branch + '/' + path + m.group(1)
    print(m.group(1), ' -> ', url)
    return m.group().replace(m.group(1), url)


def get_picture_real_url(m):
    """将Markdown文档中相对路径的图片引用，替换为上传GitHub后的真实资源访问地址"""
    global relative_path
    path, filename = os.path.split(relative_path)
    url = 'https://raw.githubusercontent.com/' + user_name + '/' + project + '/' + branch + '/' + path + m.group(1)
    print(m.group(1), ' -> ', url)
    return m.group().replace(m.group(1), url)


def get_github_resource_real_url(file_or_path_or_url, project_name='', github_user_name='zhuifengshen', branch_name='master', backup=True):
    """
    获取项目资源在Github上真实访问地址，方便写文档时引用，支持外网访问
    @param file_or_path_or_url: 某一文件、某一资源目录的路径，或Github在线资源文件的URL
                                情况一：参数为普通文件路径，需要传入项目名和用户名参数，结果返回文件上传GitHub后的真实访问地址，为只有一个元素的列表；
                                情况二：参数为Markdown文件路径，需要传入项目名和用户名参数，程序自动将文件中引用项目中相对路径的资源替换为文件上传GitHub后的真实访问地址，并返回只有一个Markdown文件绝对路径的列表；
                                情况三：参数为项目资源目录，需要传入项目名和用户名参数，则结果返回目录中各个文件上传Github后的真实访问地址列表；
                                情况四：参数为GitHub在线文件访问路径，则不需要传入项目名和用户名参数，结果返回文件在GitHub的真实访问地址，为只有一个元素的列表；
                                注意：路径中如果包含多个项目名的字符串，则默认第一个为项目名！
    @param project_name: 项目名（区分大小写）
    @param github_user_name: Github账号名
    @param branch_name: 代码分支名
    @param backup: 当更新Markdown文档时，是否备份原文件（xxx.md -> xxx_backup.md)
    @return: 真实资源URL列表
    """
    global project, branch, user_name
    project = project_name.strip() or project
    branch = branch_name.strip() or branch
    user_name = github_user_name.strip() or user_name

    file_or_path_or_url = file_or_path_or_url.strip()

    urls = []

    # Github在线资源文件（只需要传`file_or_path_or_url`参数即可）
    if github_url_regexp.match(file_or_path_or_url):
        url = file_or_path_or_url.replace('github.com', 'raw.githubusercontent.com').replace('blob/', '')
        urls.append(url)
        return urls

    absolute_path = get_absolute_path(file_or_path_or_url)
    if project and file_or_path_or_url and project in absolute_path and os.path.exists(absolute_path):
        global relative_path
        relative_path = absolute_path[absolute_path.find(project) + len(project) + 1:]  # 相对本地项目的路径
        if os.path.isfile(absolute_path):
            if absolute_path.endswith('.md'):  # 本地项目某一Markdown文件
                backup_path = absolute_path.replace('.md', '_backup.md')
                shutil.move(absolute_path, backup_path)
                with open(backup_path, 'r', encoding='utf-8') as fr:
                    content = fr.read()
                    content = file_relative_url_regexp.sub(get_file_online_url, content)
                    content = pic_relative_url_regexp.sub(get_picture_real_url, content)
                    with open(absolute_path, 'w', encoding='utf-8') as fw:
                        fw.write(content)
                if not backup:
                    os.remove(backup_path)
                print('Congratulations! Update successfully: %s' % absolute_path)
                urls.append(absolute_path)
            else:  # 本地项目某一资源文件
                file_real_url = 'https://raw.githubusercontent.com/' + \
                                user_name + '/' + project + '/' + branch + '/' + relative_path
                urls.append(file_real_url)
        elif os.path.isdir(absolute_path):  # 本地项目某一资源目录
            for dirpath, dirnames, filenames in os.walk(absolute_path):
                for filename in filenames:
                    file_real_url = 'https://raw.githubusercontent.com/' + \
                                    user_name + '/' + project + '/' + \
                                    branch + '/' + os.path.join(relative_path, filename)
                    urls.append(file_real_url)
                break
        else:
            print('输入参数file_or_path_or_url有误，请重新输入：%s' % file_or_path_or_url)
    else:
        print('输入参数有误，请确认路径、项目名是否存在且拼写正确！')

    return urls


def cli_main():
    print('Hello, Github!')


if __name__ == '__main__':
    # 1、指定本地项目资源目录
    urls = get_github_resource_real_url(
        project_name='xmind',
        file_or_path_or_url='/Users/zhangchuzhao/Project/python/tmp/xmind/images')
    for url in urls: print(url)

    # 2、指定本地项目文件
    urls = get_github_resource_real_url(
        project_name='xmind',
        file_or_path_or_url='/Users/zhangchuzhao/Project/python/tmp/xmind/images/xmind.png')
    for url in urls: print(url)

    # 3、指定Github线上文件地址
    url = 'https://github.com/zhuifengshen/xmind/blob/master/images/xmind.png'
    urls = get_github_resource_real_url(project_name='xmind', file_or_path_or_url=url)
    for url in urls: print(url)

    # 4、指定Markdown文档1
    xmind = '/Users/zhangchuzhao/Project/python/tmp/xmind/README.md'
    urls = get_github_resource_real_url(file_or_path_or_url=xmind, project_name='xmind')
    for url in urls: print(url)

    # 4、指定Markdown文档2
    xmind2testcase = '/Users/zhangchuzhao/Project/python/tmp/xmind2testcase/README.md'
    urls = get_github_resource_real_url(file_or_path_or_url=xmind2testcase, project_name='xmind2testcase')
    for url in urls: print(url)




