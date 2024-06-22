<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-disconnect-notice

_✨ bot断连时的通知插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Cypas/nonebot_plugin_disconnect_notice.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-disconnect-notice">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-disconnect-notice.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>


## 📖 介绍

- 可以在bot断开与nonebot的连接时向主人发送微信公众号消息或邮件消息，用来通知主人bot可能被风控掉线
- 目前支持全部适配器协议，通知方式支持: [pushplus](https://www.pushplus.plus/)微信公众号通知; [server酱](https://sct.ftqq.com/)(方糖)微信公众号通知; emil邮件通知
- 如果有其他通知方式的需求，欢迎提issues或pr

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-disconnect-notice

</details>


<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-disconnect-notice
</details>

<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-disconnect-notice
</details>

</details>


## ⚙️ 配置
运行插件前，需要在 nonebot2 项目的`.env.prod`文件中按照不同推送方式添加下表中的相应配置项

<details>
<summary>pushplus微信公众号消息配置教程</summary>

1. 进入[pushplus官网](https://www.pushplus.plus/)
2. 点击网页右上角 **登录** 按钮，微信扫码完成登录
3. 点击公众号提示的该卡片完成登录绑定，提示启用成功即可
   
   ![1.png](images/pushplus/1.png)
4. 回到网页端，顶部菜单栏选择**发送消息 - 一对一消息**,然后点击**一键复制**
   
   ![2.png](images/pushplus/2.png)
5. 将token按照下方配置项名 disconnect_notice_pushplus_token = "" 填入`.env.prod` 文件内

</details>

<details>
<summary>server酱(方糖)公众号消息配置教程</summary>
> server酱每天免费消息推送额度只有5条

1. 进入[server酱官网](https://sct.ftqq.com/)
2. 点击网页右上角 **登录** 按钮，微信扫码完成登录
3. 回到网页端点击 **扫码后点此继续**  按钮
4. 点击sendkey下方的 **复制** 按钮，或者你可以新建单独的appkey，然后进行复制

   ![1.png](images/server/1.png)
5. 将token按照下方配置项名 disconnect_notice_server_key = "" 填入`.env.prod` 文件内

</details>

<details>
<summary>邮件通知配置教程</summary>

- 以qq邮箱为例，其他邮箱的开启smtp方式是类似的

1. 点击qq邮箱的设置
![img.png](images/mail/img.png)

2. 点击账户
![img_1.png](images/mail/img_1.png)

3. 点击管理服务，如果没有开启，这里可能显示的是`开启服务`
![img_2.png](images/mail/img_2.png)

4. 点击`生成授权码`
![img_3.png](images/mail/img_3.png)

5. 按照要求用密保手机号发送短信验证
![img_4.png](images/mail/img_4.png)

6. 复制得到的这个授权码
![img_5.png](images/mail/img_5.png)

7. 得到的这个`授权码`就相当于邮箱密码，邮箱账号就是qq邮箱，其他的一些常见邮箱的smtp_server和smtp_port配置参数参考下表

|   邮箱名    |   smtp_server   | smtp_port |   
|:--------:|:---------------:|:---------:|
|   qq邮箱   |   smtp.qq.com   |    465    |   
| 网易yeah邮箱 |  smtp.yeah.net  |    465    |
|  阿里云邮箱   | smtp.aliyun.com |    465    |
| 网易163邮箱  |  smtp.163.com   |    465    |
| 移动139邮箱  |  smtp.139.com   |    465    |


</details>

|               配置项                | 必填 |    值类型    |     默认值      |                              说明                               |
|:--------------------------------:|:--:|:---------:|:------------:|:-------------------------------------------------------------:|
|   disconnect_notice_mode_list    | 是  | list[str] | ["pushplus"] | 通知类型列表，枚举值:pushplus mail server，可填写多个通知源，如["pushplus"，"mail"] |
| disconnect_notice_pushplus_token | 是  |    str    |      ""      |                pushplus微信公众号token，具体获取方式见上方教程                 |
|   disconnect_notice_server_key   | 是  |    str    |      ""      |                  server酱微信公众号key，具体获取方式见上方教程                  |
|   disconnect_notice_smtp_user    | 是  |    str    |      ""      |                    邮箱账号,如 114514@yeah.net                     |
| disconnect_notice_smtp_password  | 是  |    str    |      ""      |                       邮箱密码或授权码,如 114514                       |
|  disconnect_notice_smtp_server   | 是  |    str    |      ""      |                    邮箱服务器地址,如 smtp.yeah.net                    |
|   disconnect_notice_smtp_port    | 是  |    int    |     465      |                       邮箱端口号，ssl模式时为465                        |
|  disconnect_notice_notice_email  | 是  |    str    |      ""      |                        收件人邮箱，填写自己邮箱即可                         |
|    disconnect_notice_dev_mode    | 否  |   bool    |    False     |       开发者模式，该模式下bot断开连接不会触发通知消息，避免本地测试插件时不断重载而导致的大量掉线通知       |
| disconnect_notice_max_grace_time | 否  |    int    |      10      |            断连后最大宽限时长，单位:秒，如果在此期间bot完成了重连，则不触发邮件通知             |

<details>
<summary>示例配置</summary>
  
```env
## disconnect_notice掉线通知示例配置
# 通知方式list，可填写多种通知方式 枚举值:pushplus mail server
disconnect_notice_mode_list = ["pushplus"]
# pushplus微信公众号通知 https://www.pushplus.plus/
disconnect_notice_pushplus_token = ""
# server酱 https://sct.ftqq.com/
disconnect_notice_server_key = ""
# 邮件通知
disconnect_notice_smtp_user = "114514@yeah.net" #邮箱账号
disconnect_notice_smtp_password = "114514" #邮箱密码
disconnect_notice_smtp_server = "smtp.yeah.net" #邮箱服务器地址
disconnect_notice_smtp_port = 465 #邮箱端口号
disconnect_notice_notice_email = "114514@qq.com" #收件人邮箱
# 其他设定
disconnect_notice_dev_mode = False #开发者模式，该模式下bot断连不会触发通知消息，避免本地测试插件时不断重载而导致的大量掉线通知
disconnect_notice_max_grace_time = 10 #断连后最大宽限时长，单位:秒，如果在此期间bot完成了重连，则不触发邮件通知
```

</details>

## 🎉 使用
### 指令表
|  指令   | 权限 | 需要@ |  范围  |           说明            |
|:-----:|:----:|:----:|:----:|:-----------------------:|
| /掉线测试 | 主人 | 否 | 所有会话 | 主动触发掉线通知测试，用来测试通知是否正常可用 |
### 效果图
<details>
<summary>邮件通知</summary>

![mail.png](images/mail.png)

</details>

<details>
<summary>pushplus微信通知</summary>

![mail.png](images/pushplus.jpg)

</details>

<details>
<summary>server酱微信通知</summary>

![server.png](images/server.png)

</details>

## ✨喜欢的话就点个star✨吧，球球了QAQ


## ⏳ Star 趋势

[![Stargazers over time](https://starchart.cc/Cypas/nonebot_plugin_disconnect_notice.svg)](https://starchart.cc/Cypas/nonebot_plugin_disconnect_notice)
