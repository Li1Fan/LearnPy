### SDUM-WebSocket接口文档



#### 文档更新说明

| 版本  | 作者   | 参与者 | 日期       | 备注 |
| ----- | ------ | ------ | ---------- | ---- |
| 1.0.0 | 方瑞智 |        | 2023/04/13 | 初稿 |

 

#### 简介

本文主要介绍SDUM（轻量级网管工具）与话机的通信接口协议，该接口协议基于WebSocket，客户端可以由 Java、 C#、 C++、 JavaScript、Go 等开发语言实现。



#### 交互原理

SDUM作为服务端，等待话机连接；话机作为客户端，主动挂载。设备挂载成功后，请求内容封装在WebSocket的消息体中，消息体格式将在后续章节进行详细说明。

对于挂载问题，话机出厂默认有一个挂载地址。
同一局域网场景下，SDUM在局域网内通过广播，重新配置所有话机的挂载地址（功能待定），实现话机的挂载。
不同局域网场景下，话机通过默认挂载地址实现挂载，或者通过同一局域网重新配置后再进行挂载。



#### 消息体组成

请求地址：ws://ip:port/，即挂载地址

```json
// 报文基本结构：
{
  "method": "xxx",
  "type": "xxx",
  "data": {
    "xxx": "xxx"
  }
}

method:get post reply
type:auth update configure alarm info
data:{}

// 错误
{
  "method": "xxx",
  "type": "xxx",
  "data": {
    "error": "440"
  }
}
```

##### 请求报文

| 字段名 | 选项 | 参数说明                                  | 配置值或者数据类型                         |
| ------ | ---- | ----------------------------------------- | ------------------------------------------ |
| method | 必选 | 请求方法，"GET"为查询，“POST”为配置、上报 | “GET”、"POST"                              |
| key    | 必选 | 操作类型                                  | 字符串类型，"auth"认证、"keep_alive"保活等 |
| value  | 必选 | 配置值、上报值，可为空字典                | 字典类型                                   |

##### 响应报文

| 字段名  | 选项 | 参数说明                                      | 配置值或者数据类型 |
| ------- | ---- | --------------------------------------------- | ------------------ |
| success | 必选 | 请求处理结果，"true"表示成功，"false"表示失败 | "true"、"false"    |
| reason  | 必选 | 失败原因，成功则为空字符串，详见后文          | 字符串类型         |
| result  | 必选 | 返回值，可为空字典                            | 字典类型           |



#### 认证与请求

C-S 认证请求
S-C 返回auth_id
C-S 再次认证，上报auth_id （）
S-C 返回认证结果

```json
//认证请求
{
  "method": "POST",
  "key": "auth",
  "value": {}
}
//返回auth_id (该auth_id通过hash加密生成，与时间绑定)
{
  "success": "true",
  "reason": "",
  "result": {"auth_id":"xxxxxxx"}
  }
}
//再次认证请求 （再次上报的auth_id为，服务器返回的值与"Starnet@0591"拼接后，再经过hash加密生成）
{
  "method": "POST",
  "key": "auth",
  "value": {"auth_id":"xxxxxxx"}
}
//返回认证结果
{
  "success": "true",
  "reason": "",
  "result": {}
  }
}
```



 #### 保活

C-S保活请求
S-C返回

认证请求成功后，服务端会保持连接 120s，超过 120s 服务端主动断开连接。同时，讯飞侧有连接的保活监测，连续 120s 无数据交互，服务端主动断开连接。

```json
{
  "method": "POST",
  "key": "keep_alive",
  "value": {}
}
```

#### 操作

##### 获取设备信息（待商议!）

S-C获取设备信息请求
C-S返回

```json
{
  "method": "GET",
  "key": "info",
  "value": {}
}
// 成功响应
{
  "success": "true",
  "reason": "",
  "result": {
    "DevInfo": {
      "mac": "xxx",
      "sn": "xxx",
      "model": "xxx"
    },
    "AccInfo": {
      "number":"xxx"
    }
  }
}
```



##### 获取任务信息

任务包括配置任务、升级任务等

S-C获取设备信息请求
C-S返回

```json
{
  "method": "GET",
  "key": "task",
  "value": {}
}
// 成功响应
{
  "success": "true",
  "reason": "",
  "result": {"process":"sucess"}
  }
}
```

##### 配置（待商议!）

（以文件方式，或者直接POST值）

如果以文件方式下发，工具集成HTTP服务器，等待话机主动获取配置文件

S-C下发任务
C-S返回

```json
{
  "method": "POST",
  "key": "config_url",
  "value": {"url":"192.168.222.108:8080/config/xxx.xml"}
}
// 成功响应
{
  "success": "true",
  "reason": "",
  "result": {}
  }
}
```



##### 升级

如果以文件方式下发，工具集成HTTP服务器，等待话机主动获取升级文件

S-C下发任务
C-S返回

```json
{
  "method": "POST",
  "key": "update_url",
  "value": {"url":"192.168.222.108:8080/update/xxx.img"}
}
// 成功响应
{
  "success": "true",
  "reason": "",
  "result": {}
  }
}
```



##### 重启、恢复出厂

S-C下发任务
C-S返回

```json
{
  "method": "POST",
  "key": "reboot",
  "value": {}
}
// 成功响应
{
  "success": "true",
  "reason": "",
  "result": {}
  }
}
```



##### 上报告警信息

S-C上报告警信息
C-S返回

```json
{
  "method": "POST",
  "key": "alam",
  "value": {"xxx":"xxx"}
}
// 成功响应
{
  "success": "true",
  "reason": "",
  "result": {}
  }
}
```

