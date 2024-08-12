PBX HttpApi测试用例编写分享
（具体使用请查阅《星网锐捷IPPBX-RESTFUL_API_JSON接口文档》）

/（接口简介）
API接口主要分为四大类型，配置、呼叫控制、事件订阅、电话附加服务
配置：
分机、中继、路由、队列、振铃组等的增删改查
呼叫控制：
发起呼叫、保持呼叫、强插呼叫、咨询呼叫、盲转等通话相关的控制
事件订阅：
订阅事件后，就可以在该事件触发时，服务器上报给客户端，起到监听指定事件的作用。如呼叫到达事件、呼叫接通事件。
电话附加服务：
附加服务如免打扰、前转、呼叫转接、呼叫权限、指定代答等的设置。

/（关键字封装）
/（每种类型举例使用，配合报告讲解）
IMSApi初始化	
Api鉴权登录，模块初始化调用

设置IMS配置接口
参数：
type 配置类型，如分机ext、注册中继busitrk、对等中继peertrk
data 字典数据 
method 增删改查分别对应post,delete,put,get
举例：
配置-配置分机-查询单个分机号码-分机号存在
type=ext data={"domain":"", "keys":"number,auth_user,auth_pwd", "cond":{"number":"5001"}} method=get
ps：返回值处理、判断

设置IMS呼叫控制接口
参数：
type 配置类型，如发起呼叫make_call、创建放音连接make_connection、拆除通话连接clear_connection
data 字典数据 
method 默认为post，该项无需更改
举例：
呼叫控制-呼叫-1.发起呼叫
IMSApi初始化-创建连接-发起呼叫-拆除连接-关闭连接
ps:
1.这里我们对关键字进行了封装，封装在keywords.robot文件中
2.“创建连接”比较特殊，可以理解为创建一个Http会话，所有的呼叫控制都必须建立在这个连接创建成功后；此外结束时需要调用“关闭连接”，以免影响下一个Http会话。
因为关闭连接会影响会话的问题，断言都放在了最后。
3.用例均使用虚拟话机测试，如果需要使用真实话机测试，可以在变量修改号码，忽略“正在通话”关键字的失败
4.场景组合复杂，以队列场景呼叫驻留恢复为例

设置IMS事件订阅接口
参数：
data 字典数据 
method 默认为post，该项无需更改
举例：
事件订阅-呼叫事件-事件订阅
data={"event_type":"all", "expire":"600", "port":"12345", "ext_id":"", "queue_id":""}
method=post
ps:
事件订阅需要配合HttpServer服务器、呼叫控制进行测试

设置IMS电话附加业务接口
serv_type 配置类型，配置类型，获取免打扰get_do_not_disturb、获取前转get_forwarding、设置免打扰set_do_not_disturb
data 字典数据 
method 默认为post，该项无需更改
举例：
电话服务服务-免打扰-设置第一个号码的免打扰开关为开

注意：
1.环境检查会自动添加用户名、密码（每次单独运行前最好提前运行环境检查）