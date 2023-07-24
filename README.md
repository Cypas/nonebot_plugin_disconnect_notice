<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-disconnect-notice

_✨ QQbot断连时的通知插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Skyminers/Bot-Splatoon3.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-disconnect-notice">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-disconnect-notice.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>


## 📖 介绍

- 可以在qqbot断开与nonebot连接时向主人进行例如邮件的通知
- 目前支持onebotv11协议，通知方式支持邮件通知
- 如果有其他协议或通知方式的需求，欢迎提issus或pr

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
运行插件前，需要在 nonebot2 项目的`.env.prod`文件中添加下表中的代理地址配置项

| 配置项 | 必填 | 值类型 | 默认值 | 说明 |
|:------:|:----:|:---:|:---:|:--:|
| disconnect_notice_smtp_user | 是 | str | ""  | 邮箱账号,如 114514@yeah.net |
| disconnect_notice_smtp_password | 是 | str | ""  | 邮箱密码,如 114514 |
| disconnect_notice_smtp_server | 是 | str | ""  | 邮箱服务器地址,如 smtp.yeah.net |
| disconnect_notice_smtp_port | 是 | int | 465  | 邮箱端口号，ssl模式时为465 |
| disconnect_notice_notice_email | 是 | str | ""  | 收件人邮箱，填写自己邮箱即可 |

<details>
<summary>示例配置</summary>
  
```env
# disconnect_notice示例配置
disconnect_notice_smtp_user = "114514@yeah.net" #邮箱账号
disconnect_notice_smtp_password = "114514" #邮箱密码
disconnect_notice_smtp_server = "smtp.yeah.net" #邮箱服务器地址
disconnect_notice_smtp_port = 465 #邮箱端口号
disconnect_notice_notice_email = "114514@qq.com" #收件人邮箱
```

</details>

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围  |           说明            |
|:-----:|:----:|:----:|:---:|:-----------------------:|
| 断连通知测试 | 主人 | 否 | 私聊/群聊 | 主动触发掉线通知测试，用来测试通知是否正常可用 |
### 效果图
<details>
<summary>邮件通知</summary>

![mail.png](images/mail.png)

</details>

## ✨喜欢的话就点个star✨吧，球球了QAQ
