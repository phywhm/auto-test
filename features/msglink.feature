# Created by PHY at 2017/5/4
Feature: 测试消息中心与长连接服务

  @smoke
  Scenario: 长连接建立连接后注册消息中心
    Given use cid testcid1 connect link
    Then send msg tmsg to client with cid testcid1
    When client with cid testcid1 receive msg tmsg
    Then client with cid testcid1 disconnect


  @smoke
  Scenario: 踢出指定终端
    Given use cid testcid1 connect link
    Then kick off client with cid testcid1


  @smoke
  Scenario: 客户端分组并推送组消息
    Given use cid testcid1 connect link
    Then alloc cid testcid1 group ["g1", "g2", "g3"]
    Then push group msg gmsp to group ["g1"]