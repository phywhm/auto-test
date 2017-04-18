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
    Examples:
      | status |  message  | instace_status |
      |   02   |   error   |    Finished    |
      |   10   |   error   |    Finished    |
      |   11   |   error   |    Finished    |
      |   12   |   error   |    Finished    |
      |   13   |   error   |    Finished    |
      |   20   |   kicked  |    Finished    |
#      |   21   |   error   |    Finished    |程序无处理
#      |   22   |   error   |    Finished    |程序无处理
      |   23   |   address |    InService   |
      |   24   |   error   |    Finished    |
      |   31   |   address |    InService   |
      |   32   |   error   |    Finished    |



  Scenario Outline: 当请求状态为Created时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Then 用户申请一个状态为"Created"的实例
    When 用户通过"<method>"方法释放请求
    Then 这个请求应该被成功释放
    And 接入商"xiamatest"的实例个数应该为"default"
    When 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    Examples:
      | method |  status   |
      | stop   |    0      |
      | notify |    20     |
      | notify |    13     |
      | disconnet|   0     |



  Scenario: 当请求状态为Linked时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当排过队请求状态为InstanceApplying时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当没有排过队的请求状态为InstanceApplying时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当排过队的请求状态为waiting address时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当没有排过队的请求状态为waiting address时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当请求状态为InService时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当请求状态为WaitingConfirmEnqueue时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当请求状态为Enqueue时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当请求状态为WaitingInstanceRelease时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当请求状态为InstanceReleaseing时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户

  Scenario: 当请求状态为Finished时, 停止申请
    Given 玩家通过租户"xiamatest"注册一个用户
