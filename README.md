# Get Github Resource Real URL

```
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
```
