Feature: test the feature on the queue
"""
    make sure all kinds of release can change the queue status
"""
  Scenario Outline: notifying error status will reduce the instance count when limit le real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"
    When 模拟paas回调第"0"个实例的状态为"<status>"
    Then the deleted instance should receive "error" message
    And 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"
    When 模拟paas回调第"0"个实例的状态为"<status>"
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"
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
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"#Then I wait "100000" ms
    When 模拟paas回调第"0"个实例的状态为"20"
    Then the deleted instance should receive "kicked" message
    And 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"
    When 模拟paas回调第"0"个实例的状态为"20"
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"



  Scenario: stop the playing game will reduce the instance count when limit le real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"
    When 用户释放第"0"个实例
    Then 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 用户释放第"0"个实例
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"


  Scenario: overtime will reduce the instance count when limit le real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  90000  |
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  90000  |
    Then 这个请求的状态应该是"Enqueue"
    When 等待"90000"毫秒
    Then 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 等待"90000"毫秒
    Then the instance should receive "overtime" message
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"


  Scenario: disconneting websocket will reduce the instance count when limit le real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  90000  |
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个实例根据以下参数
      |    key      |  value  |
      | playingTime |  90000  |
    Then 这个请求的状态应该是"Enqueue"
    When 用户断开第"0"个实例的长链接持续"60"秒
    Then 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 用户断开第"0"个实例的长链接持续"60"秒
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"


  Scenario: requesting wrong game will reduce the instance count when limit le real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"501"和"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Given I request a "noapp.package.name" app
    Then the status of wrong instance should be "0"
    Given I request a "noapp.package1.name" app
    Then the status of wrong instance should be "0"
    When 用户释放第"0"个实例
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"


  Scenario Outline: notifying error status will reduce the instance count when limit gt real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Then I change the max instance of paas to "1"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"
    When I notify the first real instance with "<status>" status
    Then the deleted instance should receive "error" message
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When I notify the first real instance with "<status>" status
    Then 这个请求的状态应该是"InService"
    And 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"
    When 模拟paas回调第"0"个实例的状态为"<status>"
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"
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
    Given 玩家通过租户"xiamatest"注册一个用户
    Then I change the max instance of paas to "1"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"
    When I notify the first real instance with "20" status
    Then the deleted instance should receive "kicked" message
    When I notify the first real instance with "20" status
    Then 这个请求的状态应该是"InService"
    And 这个实例应该收到"address"消息
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 模拟paas回调第"0"个实例的状态为"20"
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"



  Scenario: stop the playing game will reduce the instance count when limit gt real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Then I change the max instance of paas to "1"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"Enqueue"
    When 用户释放第"0"个实例#And the instance num of "xiamatest" should be "502"
    When 用户释放第"0"个实例
    Then 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"#And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 用户释放第"0"个实例
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"


  Scenario: overtime will reduce the instance count when limit gt real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Then I change the max instance of paas to "1"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given 用户申请一个"random"实例 with "90000" time
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个"random"实例 with "90000" time
    Then 这个请求的状态应该是"Enqueue"
    Given 用户申请一个"random"实例 with "90000" time
    Then 这个请求的状态应该是"Enqueue"
    When 等待"90000"毫秒
    Then 接入商"xiamatest"已占用的实例个数应该为"501"
    When I wait "185000" ms
    Then the instance should receive "overtime" message
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"


  Scenario: disconneting websocket will reduce the instance count when limit gt real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Then I change the max instance of paas to "1"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given 用户申请一个"random"实例 with "90000" time
    Then 这个请求的状态应该是"InService"
    Given 用户申请一个"random"实例 with "90000" time
    Then 这个请求的状态应该是"Enqueue"
    Given 用户申请一个"random"实例 with "90000" time
    Then 这个请求的状态应该是"Enqueue"
    When 用户断开第"0"个实例的长链接持续"60"秒
    And I wait "60000" ms
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    When 用户断开第"0"个实例的长链接持续"60"秒
    And I wait "60000" ms
    Then 这个实例应该收到"address"消息
    And 这个请求的状态应该是"InService"
    When 用户断开第"0"个实例的长链接持续"60"秒
    And I wait "60000" ms
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"


  Scenario: requesting wrong game will reduce the instance count when limit gt real instance count
    Given 玩家通过租户"xiamatest"注册一个用户
    Then I change the max instance of paas to "1"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Given I request a "noapp.package.name" app
    Then the wrong instance should receive "error" message
    Given I request a "noapp.package1.name" app
    Then the wrong instance should receive "error" message
    When 用户释放第"0"个实例
    Then 接入商"xiamatest"已占用的实例个数应该为"500"
    Given 用户申请一个"random"实例
    Then 这个请求的状态应该是"InService"
    Then 接入商"xiamatest"已占用的实例个数应该为"501"
