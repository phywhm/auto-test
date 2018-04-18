# Created by xiama at 4/11/17
Feature: Stop instance when it is in all kinds of status
  stop instance via stopping, notify
  check the instance has been delete. and the instance num is right
  the next request will not be blocked


@smoke
Scenario Outline: 模拟paas回调各种实例状态
  Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    And 等待"2000"毫秒
    And 这个请求的状态应该是"InService"
    When 模拟paas回调实例的状态为"<status>"
    And 等待"2000"毫秒
    Then 这个实例应该收到"<message>"消息
    Then 这个请求的状态应该是"<instace_status>"
    And 接入商"xiamatest"已占用的实例个数应该为"<count>"
    Examples:
      | status |  message  | instace_status |  count |
      |   02   |   error   |    Finished    |   500  |
      |   10   |   error   |    Finished    |   500  |
      |   11   |   error   |    Finished    |   500  |
      |   12   |   error   |    Finished    |   500  |
      |   13   |   error   |    Finished    |   500  |
      |   20   |   kicked  |    Finished    |   500  |
#      |   21   |   error   |    Finished   |    500  |程序无处理
#      |   22   |   error   |    Finished   |    500  |程序无处理
      |   23   |   address |    InService   |   501  |
      |   24   |   error   |    Finished    |   500  |
      |   31   |   address |    InService   |   501  |
      |   32   |   error   |    Finished    |   500  |



  Scenario: 当请求状态为Preparing时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Then 用户申请一个状态为"Created"的实例
    When 用户释放实例
    Then 这个请求应该被成功释放
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    When 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    And 这个实例不应该包含"confirm"消息


  Scenario: 当排过队请求状态为InstanceApplying时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    And 等待"1000"毫秒
    Given 用户申请一个实例
    Then 这个请求的状态应该是"Enqueue"
    And 设置paas不返回回调地址
    When 用户释放第"0"个实例
    Then 这个请求的状态应该是"InstanceApplying"
    When 用户释放实例
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    Then 这个请求的状态应该是"Finished"



  Scenario: 当没有排过队的请求状态为InstanceApplying时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置paas不返回回调地址
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InstanceApplying"
    When 用户释放实例
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    Then 这个请求的状态应该是"Finished"

  Scenario: 请求状态为InstanceApplying时, 异步准备失败
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置paas不返回回调地址
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InstanceApplying"
    When 模拟paas回调实例的状态为"02"
    And 等待"2000"毫秒
    Then 这个实例应该收到"error"消息
    Then 这个请求的状态应该是"Finished"
    And 接入商"xiamatest"已占用的实例个数应该为"default"



  Scenario: 当排过队的请求状态为waiting address时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当没有排过队的请求状态为waiting address时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当请求状态为InService时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    When 用户释放实例
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    Then 这个请求的状态应该是"Finished"

  Scenario: 当请求状态为WaitingConfirmEnqueue时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    And 等待"1000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | confirm  |  0 |
    Then 这个请求的状态应该是"WaitingConfirmEnqueue"
    When 用户释放实例
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    Then 这个请求的状态应该是"Finished"

  Scenario: 当请求状态为Enqueue时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    And 等待"1000"毫秒
    Given 用户申请一个实例
    Then 这个请求的状态应该是"WaitingConfirmEnqueue"
    When 用户释放实例
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    Then 这个请求的状态应该是"Finished"

  Scenario: 当请求状态为WaitingInstanceRelease时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    And 设置paas不返回回调地址
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InstanceApplying"
    When 用户释放实例
    When 用户释放实例
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    Then 这个请求的状态应该是"Finished"

  Scenario: 当请求状态为InstanceReleaseing时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    When 用户释放实例
    When 用户释放实例
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    Then 这个请求的状态应该是"Finished"

  Scenario: 当请求状态为Finished时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    When 用户释放实例
    And 接入商"xiamatest"已占用的实例个数应该为"default"
    Then 这个请求的状态应该是"Finished"
    When 开始记录paas收到的请求
    When 用户释放实例
    And 获取paas收到的请求
    And paas收到的请求中应该包含"release"的请求