# GetTagMAC
通过websocket获取到uwbTag的MAC地址，进一步获取到TagMAC对应的TagId
## 文件
### 主要文件
* con_oracle.py:oracle数据库连接测试
* main.py:功能实现，主函数
* stable_tese.py:之前使用sockets库时，连接一段时间后会断开连接，用于测试websock连接的稳定性
* test.py:用于测试一些功能的实现
### 其他未列出文件
使用.gitignor忽略
* config.ini:配置文件，现阶段主要用于配置数据库
* logger.log:日志文件
### 问题
* 解决
1. 使用一段时间后websocket连接会自动断开
* 解决:查阅资料后发现主要问题是websockets库在连接到websocket后会定时发送ping包，当ping包超时后就会断开连接，但此websocket在js代码中运行正常，故关闭websocket的ping功能后即可正常使用，原文如下：
>I encountered the same problem. After digging a while I found multiple versions of the answer that tells to just reconnect, but I didn't think it was a reasonable route, so I dug some more.
Enabling DEBUG level logging I found out that python websockets default to sending ping packets, and failing to receive a response, timeouts the connection. I am not sure if this lines up with the standard, but at least javascript websockets are completely fine with the server my python script times out with.
The fix is simple: add another kw argument to connect:
>>websockets.connect(uri, ping_interval=None)
The same argument should also work for server side function serve
* 另一种解决方案是检测到断开连接后自动重连

2. 数据库连接问题
* 连接oracle数据库时应当使用cx_oracle库，同时还要到Oracle官网下载响应的Oracle instant
> https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html