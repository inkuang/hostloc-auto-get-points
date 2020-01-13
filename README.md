# Hostloc Auto Get Points
使用 GitHub Actions 自动获取 Hostloc 论坛积分

## 使用说明

Fork 本仓库，然后点击你的仓库右上角的 Settings，找到 Secrets 这一项，添加两个秘密环境变量。

![VIAs.png](https://img.xirikm.net/images/VIAs.png)

其中 `HOSTLOC_USERNAME` 是你在 Hostloc 的帐户名，`HOSTLOC_PASSWORD` 是你的帐户密码。

设置好环境变量后点击你的仓库上方的 Actions 选项，确认在 Fork 的仓库上启用 Github Actions 即可。

![VZ5E.png](https://img.xirikm.net/images/VZ5E.png)

仓库内包含的 GitHub Actions 脚本每天会在国际标准时间 17 点（北京时间凌晨 1 点）自动执行，你也可以通过 `Push` 操作手动触发。

支持多帐号了，其他操作不用变，直接在 HOSTLOC_USERNAME 和 HOSTLOC_PASSWORD 两个变量内写入多组数据即可，数据之间用半角逗号 “,” 分开，帐号和密码需要一一对应

还有，在测试时发现，Github Actions 的定时任务存在5到10分钟的延迟，如果到时间了没有执行任务，不用着急，多等一会儿就行了
