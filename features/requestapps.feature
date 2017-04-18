Feature: 申请实例

  @smoke
  Scenario: 申请一个正常的游戏
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    And 等待"2000"毫秒
    Then 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 用户释放实例
    And 等待"2000"毫秒
    Then 这个请求应该被成功释放
    And 接入商"xiamatest"已占用的实例个数应该为"500"

  @playing_time, @smoke
  Scenario: 申请一个带有可玩儿时间的游戏
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  90000  |
    Then 这个请求的状态应该是"InService"
    When 等待"90000"毫秒
    Then 这个请求的状态应该是"Finished"
    And 这个实例应该收到"timeover"消息

  @playing_time, @smoke
  Scenario: 排队时间不计入游戏可玩儿时间
    Given 玩家通过租户"xiamatest"注册一个用户
    Then 设置paas的最大实例数为"1"
    Then I change the max instance of paas to "1"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  90000  |
    Then I wait "1000" ms
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  90000  |
    When 等待"60000"毫秒
    And 用户释放第"0"个实例
    When 等待"30000"毫秒
    Then 最后一个请求的状态应该是"InService"
    When 等待"50000"毫秒
    Then 最后一个请求的状态应该是"InService"
    When 等待"10000"毫秒
    Then 这个实例应该收到"timeover"消息
    And 最后一个请求的状态应该是"Finished"


  @playing_time
  Scenario: 申请一个永久可玩的游戏
    Given 玩家通过租户"xiamatest"注册一个用户


  @playing_time
  Scenario: 没有单次播流时长限制时,申请游戏
    Given 玩家通过租户"xiamatest"注册一个用户
    Given I request a "random" app with "90000" time
    And I wait "2000" ms
    Then the instance should receive "address" message
    And I wait "60000" ms
    Then the status of instance should be "4"
    And the instance num of "xiamatest" should be "501"
    And I wait "30000" ms for overtime
    Then the instance should be deleted successfully
    And the instance num of "xiamatest" should be "default"

  @playing_time
  Scenario: 当单次播流时长大于可玩儿时长时,申请游戏
  "set the global playing time to 60s"
    Given 玩家通过租户"xiamatest"注册一个用户
    Given I request a "random" app with "90000" time
    And I wait "2000" ms
    Then the instance should receive "address" message
    And I wait "45000" ms
    Then the status of instance should be "4"
    And the instance num of "xiamatest" should be "501"
    And I wait "15000" ms for overtime
    Then the instance should be deleted successfully
    And the instance num of "xiamatest" should be "default"

  @playing_time
  Scenario: 当单次播流时等于可玩儿时长时,申请游戏
  "set the global playing time to 60s"
    Given 玩家通过租户"xiamatest"注册一个用户
    Given I request a "random" app with "60000" time
    And I wait "2000" ms
    Then the instance should receive "address" message
    And I wait "45000" ms
    Then the status of instance should be "4"
    And the instance num of "xiamatest" should be "501"
    And I wait "15000" ms for overtime
    Then the instance should be deleted successfully
    And the instance num of "xiamatest" should be "default"

  @playing_time
  Scenario: 当单次播流时小于可玩儿时长时,申请游戏
  "set the global playing time to 60s"
    Given 玩家通过租户"xiamatest"注册一个用户
    Given I request a "random" app with "40000" time
    And I wait "2000" ms
    Then the instance should receive "address" message
    Then the status of instance should be "4"
    And the instance num of "xiamatest" should be "501"
    And I wait "40000" ms for overtime
    Then the instance should be deleted successfully
    And the instance num of "xiamatest" should be "default"

  @playing_time
  Scenario: 当单次播流时长是字符串时, 申请实例
  "set the global playing time to '12312sf'"
    Given 玩家通过租户"xiamatest"注册一个用户
    Given I request a "random" app with "90000" time
    And I wait "2000" ms
    Then the instance should receive "address" message
    Then the status of instance should be "4"
    And the instance num of "xiamatest" should be "501"
    And I wait "90000" ms for overtime
    Then the instance should be deleted successfully
    And the instance num of "xiamatest" should be "default"



  @no_impl
  Scenario: 修改单用户可申请实例个数
    Given 玩家通过租户"xiamatest"注册一个用户

  @no_impl
  Scenario: 一个用户只能打开一个同款游戏
    Given 玩家通过租户"xiamatest"注册一个用户

  @no_impl
  Scenario: 修改单用户同一游戏实例个数
    Given 玩家通过租户"xiamatest"注册一个用户

  @no_impl
  Scenario: 申请游戏时, paas服务异常
    Given 玩家通过租户"xiamatest"注册一个用户

  @no_impl
  Scenario: 申请游戏时, paas没有回调播流地址
    Given 玩家通过租户"xiamatest"注册一个用户

  @no_impl
  Scenario: 申请游戏是时, 没有获取到routerID
    Given 玩家通过租户"xiamatest"注册一个用户


  Scenario: 申请一个不存在的游戏
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"wrong"实例
    And 等待"2000"毫秒
    Then 这个请求应该被成功释放
    And the instance num of "xiamatest" should be "default"

  Scenario Outline: 当请求在不同状态下, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个状态为"<status>"的实例
    And 用户重复申请该实例
    And 用户重复申请该实例
    Then 这个请求的状态应该是"<expect_status>"
    Examples:
      | status  |  expect_status |
      | Created |    Created     |
      | Linked  |    InService   |

  Scenario: 当实例状态是InstanceApplying, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas不返回回调地址
    Given 用户申请一个实例
    And 用户重复申请该实例
    Then 这个请求的状态应该是"InstanceApplying"

  Scenario: 当实例状态是InService, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    And 用户重复申请该实例
    Then 这个请求的状态应该是"InService"

  Scenario: 当实例状态是WaitingConfirmEnqueue, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"0"
    Given 用户申请一个实例但不入对
    And 用户重复申请该实例
    Then 这个请求的状态应该是"WaitingConfirmEnqueue"

  Scenario: 当实例状态是Enqueue, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"0"
    Given 用户申请一个实例
    And 用户重复申请该实例
    Then 这个请求的状态应该是"Enqueue"

  Scenario: 当实例状态是WaitingInstanceRelease, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas不返回回调地址
    Given 用户申请一个实例
    Given 用户释放实例
    And 用户重复申请该实例
    Then 这个请求的状态应该是"WaitingInstanceRelease"

  Scenario: 当实例状态是InstanceReleaseing, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    Given 用户释放实例
    And 用户重复申请该实例
    Then 这个请求的状态应该是"InstanceReleaseing"

  @no_impl
  Scenario: 当实例状态是Finished, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    Given 用户释放实例
    And 用户重复申请该实例
    Then 这个请求的状态应该是"Finished"
    And paas收到的请求中应该包含"releaseInstance"的请求