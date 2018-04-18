Feature: 用户长链接
"""
    receive and send data via access
"""

  @smoke
  Scenario: 断开长链接不超时, 实例不被释放
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    When 用户断开实例的长链接持续"50"秒
    And 用户重连实例的长链接
    And 等待"20000"毫秒
    Then 这个请求的状态应该是"InService"

  @smoke
  Scenario: 断开长链接超过1分钟, 实例被释放
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    When 用户断开实例的长链接持续"70"秒
    Then 这个请求应该被成功释放

  @smoke
  Scenario: 反复断开和重连长链接不超时, 实例不应该被释放
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    When 用户断开实例的长链接持续"20"秒
    And 用户重连实例的长链接
    And 等待"20000"毫秒
    When 用户断开实例的长链接持续"40"秒
    And 用户重连实例的长链接
    Then 这个请求的状态应该是"InService"
    When 用户断开实例的长链接持续"70"秒
    Then 这个请求应该被成功释放

  @smoke
  Scenario: 如果SDK不发送ping消息, 实例会被服务端释放
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | ping     |  False |
    Then 等待"30000"毫秒
    Then 这个请求应该被成功释放
