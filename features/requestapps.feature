Feature: 申请实例
  Scenario: 申请一个正常的游戏
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个"random"实例
    And 等待"2000"毫秒
    Then the instance should receive "address" message
    Then the status of instance should be "4"
    And the instance num of "xiamatest" should be "501"
    When I try to stop the instance
    And I wait "2000" ms
    Then the instance should be deleted successfully
    And the instance num of "xiamatest" should be "default"

  @playing_time
  Scenario: 申请一个带有可玩儿时间的游戏

  @playing_time
  Scenario: 申请一个永久可玩的游戏


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

  @playing_time
  Scenario: 排队时间不计入游戏可玩儿时间
    Given 玩家通过租户"xiamatest"注册一个用户
    Then I change the max instance of paas to "1"
    Given I request a "random" app with "90000" time
    Then I wait "1000" ms
    Given I request a "random" app with "90000" time
    Then I wait "60000" ms
    When I try to stop the "0th" instance
    And I wait "30000" ms
    Then the status of instance should be "4"
    When I wait "50000" ms
    Then the status of instance should be "4"
    When I wait "10000" ms
    Then the instance should receive "overtime" message



  Scenario: 一个用户默认可申请5个实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Given 用户申请一个"random"实例
    And 等待"1000"毫秒
    Then the status of instance should be "0"

  @no_impl
  Scenario: 修改单用户可申请实例个数

  @no_impl
  Scenario: 一个用户只能打开一个同款游戏

  @no_impl
  Scenario: 修改单用户同一游戏实例个数

  @no_impl
  Scenario: 申请游戏时, paas服务异常

  @no_impl
  Scenario: 申请游戏时, paas没有回调播流地址

  @no_impl
  Scenario: 申请游戏是时, 没有获取到routerID


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

  @no-impl
  Scenario: 当实例状态是Finished, 重复申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户申请一个实例
    Given 用户释放实例
    And 用户重复申请该实例
    Then 这个请求的状态应该是"Finished"
    And Paas服务应该收到一个"releaseInstance"请求