# Created by PHY at 2017/5/4
Feature: 测试消息中心与长连接服务

  @smoke
  Scenario: 长连接建立连接后注册消息中心
    Given 使用CID testcid1 连接长连接服务器
    Then 检查 testcid1 路由是否在消息中心注册成功
#    Then 清除CID testcid1 的所有消息
    Then 推送单播消息 tmsg 给 testcid1 客户端
    When 当 testcid1 客户端收到消息 tmsg
    Then 检查数据库中 testcid1 的消息状态是否为 Sent
    Then testcid1 客户端主动断开长连接
    Then 检查 testcid1 路由是否在消息中心注销成功


  @smoke
  Scenario: 踢出指定终端
    Given 使用CID testcid2 连接长连接服务器
    Then 检查 testcid2 路由是否在消息中心注册成功
    Then 踢出CID为 testcid2 的用户
    Then 推送单播消息 tmsg 给 testcid2 客户端
    Then 检查数据库中 testcid2 的消息状态是否为 Created
    Then 检查 testcid2 路由是否在消息中心注销成功


  @smoke
  Scenario: 客户端分组并推送组消息 1
    Given 使用CID testcid1 连接长连接服务器
    Then 检查 testcid1 路由是否在消息中心注册成功
    Then alloc cid testcid1 group ["g1", "g2", "g3"]
    Then push group msg gmsp to group ["g1"]
    Then push group msg gmsp to group ["g1", "g5"]
    Then testcid1 客户端主动断开长连接
    Then 检查 testcid1 路由是否在消息中心注销成功