Feature: 切换码率的各种场景
  
  
  @smoke
  Scenario: 正常切换码率
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    Then 等待"1000"毫秒
    Then 这个请求的状态应该是"InService"
    When 用户用"4"切换实例的码率
    Then 这个请求的状态应该是"InService"
    Then 这个实例应该包含"changeResolution"消息
    And 这个实例应该收到"address"消息
    When 等待"30000"毫秒
    Then 接入商"xiamatest"已占用的实例个数应该为"501"


  @smoke
  Scenario: 当用户达到最大实例数时, 切换码率
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
    When 用户用"4"切换实例的码率
    Then 这个请求的状态应该是"InService"
    Then 这个实例应该包含"changeResolution"消息
    Then 这个实例应该收到"address"消息
    And 接入商"xiamatest"已占用的实例个数应该为"505"

  # TODO: 后期需要细化
  Scenario: 当请求在不同状态下, 切换码率
    Given 玩家通过租户"xiamatest"注册一个用户


  Scenario: 切换码率时, Paas服务异常
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    When 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    When 设置paas"updateResolution"操作的错误响应次数为"1"
    And 用户用"4"切换实例的码率
    Then 这个请求的状态应该是"Finished"
    And 接入商"xiamatest"已占用的实例个数应该为"500"


  Scenario: 切换码率时, Paas没有回调流地址
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    When 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    When 设置paas不返回回调地址
    And 用户用"4"切换实例的码率
    Then 这个请求的状态应该是"Finished"
    And 接入商"xiamatest"已占用的实例个数应该为"500"
    
  Scenario: 切换码率时, Paas回调刷新失败
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    When 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    When 设置paas不返回回调地址
    And 用户用"4"切换实例的码率
    And 模拟paas回调实例的状态为"32"
    Then 这个请求的状态应该是"Finished"
    And 接入商"xiamatest"已占用的实例个数应该为"500"

  Scenario Outline: 无级变速
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | bitRate |  <bitrate> |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"resolutionInfo/id"字段值应该是"<resolution>"
    And paas收到的"apply"请求中"resolutionInfo/bitRate"字段值应该是"<rate>"
    Examples:
      | bitrate  | resolution |  rate   |
      |  299   |     1        | 2392000 |
      |  300   |     1        | 2400000 |
      |  399   |     1        | 3192000 |
      |  400   |     2        | 3200000 |
      |  401   |     2        | 3208000 |
      |  500   |     3        | 4000000 |
      |  501   |     3        | 4008000 |
      | 50000  |     4        | 8000000 |
      | 50001  |     4        | 8000000 |

  Scenario: 申请不带码率参数申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个"random"实例
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"resolutionInfo/id"字段值应该是"2"

  Scenario: 带定制码率申请游戏
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | resolution  |  4      |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"resolutionInfo/id"字段值应该是"4"

  Scenario Outline: 带定制码率和测速申请游戏
    Given 玩家通过租户"xiamatest"注册一个用户
    When 开始记录paas收到的请求
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | resolution  |  1      |
      | bitRate   |  <bitrate> |
    Then 最后一个请求的状态应该是"InService"
    And 获取paas收到的请求
    And paas收到的"apply"请求中"resolutionInfo/id"字段值应该是"<resolution>"
    And paas收到的"apply"请求中"resolutionInfo/bitRate"字段值应该是"<rate>"
    Examples:
      | bitrate  | resolution |  rate   |
      |  401   |     2        | 3208000 |
      |  0     |     1        | 2400000 |
      |  -1    |     1        | 2400000 |

