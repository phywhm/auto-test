Feature: 排队的基本功能
"""
    make sure that all kinds of releasing can make the next request work fine
"""


  Scenario: 接入商只能获得订单中的实例个数
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置租户"xiamatest"订单并发量为"501", 实际已占用实例个数为"500"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    And 租户"xiamatest"实际已占用实例个数为"501"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    #TODO: 这个申请不要确认入队, 请求状态应该是"WaitingConfirmEnqueue"
    Then 这个请求的状态应该是"Enqueue"
    And 租户"xiamatest"实际已占用实例个数为"501"

  Scenario: 没有空闲实例会导致用户排队
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    And 租户"xiamatest"实际已占用实例个数为"501"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    #TODO: 这个申请不要确认入队, 请求状态应该是"WaitingConfirmEnqueue"
    Then 这个请求的状态应该是"Enqueue"
    And 租户"xiamatest"实际已占用实例个数为"501"


  Scenario: 优先级高的请求优先获取实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | priority |  2000  |
    And 等待"1000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | priority |  2001  |
    And 等待"1000"毫秒
    Then 这个请求的状态应该是"Enqueue"
    When 用户释放第"0"个实例
    Then 最后一个请求的状态应该是"InService"

  Scenario: 优先级相同时, 先入队的请求优先获取实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | confirm  |  False  |
    And 等待"1000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | confirm  |  False |
    And 等待"1000"毫秒
    Then 这个请求的状态应该是"WaitingConfirmEnqueue"
    When 用户确认请求入队
    And 用户确认第"1"个请求入队
    When 用户释放第"0"个实例
    Then 最后一个请求的状态应该是"Enqueue"
    And 第"1"个请求的状态应该是"InService"

  Scenario: 排队的请求定期收到排队消息
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | priority |  2000  |
    And 等待"1000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | priority |  2001  |
    And 等待"1000"毫秒
    Then 这个请求的排队位置应该是"1"
    And 第"1"个请求的排队位置应该是"2"
    When 用户释放第"0"个实例
    Then 最后一个请求的状态应该是"InService"
    And 第"1"个请求的排队位置应该是"1"

  Scenario: 用户释放实例会随机触发同一个router的请求申请实例

  Scenario: 随机触发的实例申请不会是已达到实例上限的队列
    Given 设置paas的最大实例数为"2"
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置租户"xiamatest"订单并发量为"501", 实际已占用实例个数为"500"
    Given 用户申请一个实例
    Given 用户申请一个实例
    Given 玩家通过租户"xiamatest01"注册一个用户
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    When 开始记录paas收到的请求
    And 用户释放实例
    And 等待"2000"毫秒
    And 获取paas收到的请求
    Then paas的请求中不包含"InstanceApply"的请求



    Scenario Outline: notifying error status will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I notify the "0th" instance with "<status>" status
        Then the deleted instance should receive "error" message
        And the instance should receive "address" message
        And the status of instance should be "4"
        When I notify the "0th" instance with "<status>" status
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"
        Examples:
            | status |
            |   02   |
            |   10   |
            |   11   |
            |   12   |
            |   13   |
            |   24   |
            |   32   |


    Scenario: notifying 20 status will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        #Then I wait "100000" ms
        When I notify the "0th" instance with "20" status
        Then the deleted instance should receive "kicked" message
        And the instance should receive "address" message
        And the status of instance should be "4"
        When I notify the "0th" instance with "20" status
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"



    Scenario: stop the playing game will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I try to stop the "0th" instance
        Then the instance should receive "address" message
        And the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        When I try to stop the "0th" instance
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: overtime will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "90000" time
        Then the status of instance should be "4"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        When I wait "90000" ms
        Then the instance should receive "address" message
        And the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        When I wait "90000" ms
        Then the instance should receive "overtime" message
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: disconneting websocket will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "90000" time
        Then the status of instance should be "4"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        Then the instance should receive "address" message
        And the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: requesting wrong game will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "noapp.package.name" app
        Then the status of wrong instance should be "0"
        Given I request a "noapp.package1.name" app
        Then the status of wrong instance should be "0"
        When I try to stop the "0th" instance
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario Outline: notifying error status will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I notify the first real instance with "<status>" status
        Then the deleted instance should receive "error" message
        And the instance num of "xiamatest" should be "501"
        When I notify the first real instance with "<status>" status
        Then the status of instance should be "4"
        And the instance should receive "address" message
        And the status of instance should be "4"
        When I notify the "0th" instance with "<status>" status
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"
        Examples:
            | status |
            |   02   |
            |   10   |
            |   11   |
            |   12   |
            |   13   |
            |   24   |
            |   32   |


    Scenario: notifying 20 status will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I notify the first real instance with "20" status
        Then the deleted instance should receive "kicked" message
        When I notify the first real instance with "20" status
        Then the status of instance should be "4"
        And the instance should receive "address" message
        And the instance num of "xiamatest" should be "501"
        When I notify the "0th" instance with "20" status
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"



    Scenario: stop the playing game will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I try to stop the "0th" instance
        #And the instance num of "xiamatest" should be "502"
        When I try to stop the "0th" instance
        Then the instance should receive "address" message
        And the status of instance should be "4"
        #And the instance num of "xiamatest" should be "501"
        When I try to stop the "0th" instance
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: overtime will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "90000" time
        Then the status of instance should be "4"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        When I wait "90000" ms
        Then the instance num of "xiamatest" should be "501"
        When I wait "185000" ms
        Then the instance should receive "overtime" message
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: disconneting websocket will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "90000" time
        Then the status of instance should be "4"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        And the instance num of "xiamatest" should be "501"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        Then the instance should receive "address" message
        And the status of instance should be "4"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: requesting wrong game will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "noapp.package.name" app
        Then the wrong instance should receive "error" message
        Given I request a "noapp.package1.name" app
        Then the wrong instance should receive "error" message
        When I try to stop the "0th" instance
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"
