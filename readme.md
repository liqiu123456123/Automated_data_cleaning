<div id="top"></div><div id="top"></div>

* 联系作者
* 邮箱：liqiu6789@qq.com
* qq：674658532
* 微信:liqiu6746

# 基于Pyqt和Django的云数据自动化清洗系统
<!-- 目录 -->
<details>
  <summary>目录</summary>
  <ol>
    <li>
      <a href="#关于本项目">关于本项目</a></li>
    <li>
      <a href="#开始">开始</a>
      <ul>
        <li><a href="#依赖">依赖</a></li>
        <li><a href="#安装">安装</a></li>
      </ul>
    </li>
    <li><a href="#使用方法">使用方法</a></li>
    <li><a href="#贡献">贡献</a></li>
    <li><a href="#许可证">许可证</a></li>
    <li><a href="#联系作者">联系作者</a></li>
  </ol>
</details>


<!-- 关于本项目 -->
## 关于本项目


这是一个一个自带云盘的数据清洗自动化系统，前端部分使用Pyqt5进行开发，后端使用流行的web框架Django，
接口是使用REST framework开发的RESTful API，前后端交互通过requests库来完成。

以下是项目的一些特点：
* 秒开显示大型excel，体验良好！
* 读取excel文件进度条显示
* 常用数据清洗操作全界面操作，上手简单！
* 自带云盘功能，跨设备处理数据无担忧！
* API使用REST-framework框架进行开发，规范易维护！
* celery异步邮件验证注册！
* exe封装，随开随用！
* 精美QT界面和合理UI设计！
* 不联网也可使用数据清洗功能！


1、启动redis
![img.png](readme_img%2Fimg.png)

2、运行django

python .\manage.py runserver

![img_1.png](readme_img%2Fimg_1.png)

3、启动celery

celery -A ctx_django worker --loglevel=info -P eventlet


<p align="right">(<a href="#top">返回顶部</a>)</p>

![img_2.png](readme_img%2Fimg_2.png)

4、运行 new_ctx_win.py进入主界面
![img_3.png](readme_img%2Fimg_3.png)

5、从磁盘选择文件进行读入，读入完成解锁数据选项
![img_4.png](readme_img%2Fimg_4.png)

6、点击数据排序，排序菜单添加到已选操作栏中

![img_5.png](readme_img%2Fimg_5.png)
7、在已选操作栏中点击排序菜单

![img_6.png](readme_img%2Fimg_6.png)
8、在排序菜单中，选择月份降序排列，然后点击CTX,启动按钮！

月份降序排列后：
![img_7.png](readme_img%2Fimg_7.png)

9、点击注册/登陆按钮，开始进行云盘注册
![img_new_8.png](readme_img%2Fimg_new_8.png)

![img_new_9.png](readme_img%2Fimg_new_9.png)
10、切换到注册界面，进行注册

填入邮箱，收到验证码后，输入验证码
![img_9.png](readme_img%2Fimg_9.png)

11、注册后进行登陆，登陆成功会弹出云盘菜单

![img_10.png](readme_img%2Fimg_10.png)

12、点击云盘进入云盘界面，可像网盘一样进行文件上传和下载
![img_11.png](readme_img%2Fimg_11.png)

![img_12.png](readme_img%2Fimg_12.png)


<!-- 开始 -->
## 开始

这是一份在本地构建项目的指导的例子。
要获取本地副本并且配置运行，你可以按照下面的示例步骤操作。

### 依赖

这只是一个列出软件依赖和安装方法的例子。
* pip
  ```sh
  pip install -r requirements.txt
  ```

### 安装


1. 克隆本仓库
   ```sh
   https://github.com/liqiu123456123/Automated_data_cleaning.git
   ```
2. 直接下载本项目源码

<p align="right">(<a href="#top">返回顶部</a>)</p>



<!-- 使用方法 示例 -->
## 使用方法

运行xx.py开始运行，放操作截图。可以和软著的操作截图共用


<p align="right">(<a href="#top">返回顶部</a>)</p>



<!-- 贡献 -->
## 贡献

如果你想参与本项目的开发，请不要客气！
贡献让开源社区成为了一个非常适合学习、启发和创新的地方。你所做出的任何贡献都是**受人尊敬**的。

如果你有好的建议，请复刻（fork）本仓库并且创建一个拉取请求（pull request）。你也可以简单地创建一个议题（issue），并且添加标签「enhancement」。不要忘记给项目点一个 star！再次感谢！

1. 复刻（Fork）本项目
2. 创建你的 Feature 分支
3. 提交你的变更 
4. 推送到该分支 
5. 创建一个拉取请求（Pull Request）

<p align="right">(<a href="#top">返回顶部</a>)</p>



<!-- 许可证 -->
## 许可证

根据 MIT 许可证分发。打开 [LICENSE.txt](LICENSE.txt) 查看更多内容。


<p align="right">(<a href="#top">返回顶部</a>)</p>



<!-- 联系作者 -->
## 联系作者

* 邮箱：liqiu6789@qq.com
* qq：674658532
* 微信:liqiu6746

* 项目链接: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">返回顶部</a>)</p>






