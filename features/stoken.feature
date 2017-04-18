Feature: all kinds of scenarios on Stoken

  @smoke
  Scenario: 正常刷新stoken
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    Then 等待"1000"毫秒
    Then 这个请求的状态应该是"InService"
    When 用户刷新实例的stoken
    Then 这个请求的状态应该是"InService"
    Then 这个实例应该包含"refreshstoken"消息
    And 这个实例应该收到"address"消息
    And 接入商"xiamatest"已占用的实例个数应该为"501"

  @smoke
  Scenario: 当用户达到最大实例数时, 刷新stoken
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    Then 等待"1000"毫秒
    Given 用户申请一个"random"实例
    Then 等待"1000"毫秒
    Given 用户申请一个"random"实例
    Then 等待"1000"毫秒
    Given 用户申请一个"random"实例
    Then 等待"1000"毫秒
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    When 用户刷新实例的stoken
    Then 这个请求的状态应该是"InService"
    Then 这个实例应该包含"refreshstoken"消息
    Then 这个实例应该收到"address"消息
    And 接入商"xiamatest"已占用的实例个数应该为"505"


#  Scenario Outline: 当请求在不同状态下, 刷新stoken

  Scenario: 刷新stoken时, Paas服务异常
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    When 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    When 设置paas的错误响应次数为"1"
    And 用户刷新实例的stoken
    Then 这个请求的状态应该是"Finish"
    And 接入商"xiamatest"已占用的实例个数应该为"500"


  Scenario: 刷新stoken时, Paas没有回调流地址
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    When 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    When 设置paas不返回回调地址
    And 用户刷新实例的stoken
    Then 这个请求的状态应该是"Finish"
    And 接入商"xiamatest"已占用的实例个数应该为"500"
    
  Scenario: 刷新stoken时, Paas没有回调刷新失败
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    When 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    When 设置paas不返回回调地址
    And 用户刷新实例的stoken
    And 模拟paas回调实例的状态为"13"
    Then 这个请求的状态应该是"Finish"
    And 接入商"xiamatest"已占用的实例个数应该为"500"

