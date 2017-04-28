Feature: 排队的基本功能
"""
    make sure that all kinds of releasing can make the next request work fine
"""

  @smoke
  Scenario: 接入商只能获得订单中的实例个数
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"1000"和"999"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"1000"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    #TODO: 这个申请不要确认入队, 请求状态应该是"WaitingConfirmEnqueue"
    Then 这个请求的状态应该是"Enqueue"
    And 接入商"xiamatest"已占用的实例个数应该为"1000"

  @smoke
  Scenario: 没有空闲实例会导致用户排队
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"
    And 接入商"xiamatest"已占用的实例个数应该为"501"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    #TODO: 这个申请不要确认入队, 请求状态应该是"WaitingConfirmEnqueue"
    Then 这个请求的状态应该是"Enqueue"
    And 接入商"xiamatest"已占用的实例个数应该为"501"

  @smoke
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


  @smoke
  Scenario: 优先级(2001)相同时, 先申请的请求优先获取实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | confirm  |  0  |
      | priority |  2001  |
    And 等待"1000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | confirm  |  0 |
      | priority |  2001  |
    And 等待"1000"毫秒
    Then 这个请求的状态应该是"WaitingConfirmEnqueue"
    When 用户确认请求入队
    And 用户确认第"1"个请求入队
    When 用户释放第"0"个实例
    And 等待"10000"毫秒
    Then 最后一个请求的状态应该是"Enqueue"
    And 第"0"个请求的状态应该是"InService"

   @smoke
  Scenario: 优先级(0)相同时, 先申请的请求优先获取实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个实例
    And 等待"2000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | confirm  |  0  |
    And 等待"1000"毫秒
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | confirm  |  0 |
    And 等待"1000"毫秒
    Then 这个请求的状态应该是"WaitingConfirmEnqueue"
    When 用户确认请求入队
    And 用户确认第"1"个请求入队
    When 用户释放第"0"个实例
    And 等待"10000"毫秒
    Then 最后一个请求的状态应该是"Enqueue"
    And 第"0"个请求的状态应该是"InService"


  @smoke
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

  @smoke
  Scenario: 同一个product不同的router的请求进入到不同的队列
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"1"
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个路由为"3,4"的实例
    Then 这个请求的排队位置应该是"2"

    Given 用户申请一个路由为"5,4"的实例
    Then 请求的排队位置应该是"1"
    When 用户释放第"0"个实例
    Then 最后一个请求的排队位置应该是"1"
    And 第"2"个请求的排队位置应该是"1"

  @smoke
  Scenario: 不同product相同router的请求进入到不同的队列
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"1000"和"999"
    Given 用户申请一个实例
    Given 用户申请一个实例
    Given 用户申请一个实例
    Given 用户申请一个实例
    Then 这个请求的排队位置应该是"3"
    Given 玩家通过租户"xiamatest01"注册一个用户
    Given 用户申请一个实例
    Then 这个请求的排队位置应该是"1"
    When 用户释放第"0"个实例
    Then 最后一个请求的排队位置应该是"1"



  Scenario: router队列阻塞其他product的router队列, 不会阻塞同一product的其他router
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas中"3,4"路由的实例个数为"2"
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个路由为"3,4"的实例
    Then 这个请求的状态应该是"Enqueue"
    Given 用户申请一个路由为"2,4"的实例
    Then 这个请求的状态应该是"InService"
    And 这个实例不应该收到"confirm"消息
    Given 玩家通过租户"xiamatest01"注册一个用户
    Given 用户申请一个路由为"3,4"的实例
    Then 这个请求的状态应该是"Enqueue"
    Given 用户申请一个路由为"2,4"的实例
    Then 这个请求的状态应该是"InService"
    And 这个实例不应该收到"confirm"消息


  Scenario: 一个product等待不会影响其他prod申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"1000"和"999"
    Given 用户申请一个实例
    Given 用户申请一个实例
    Given 用户申请一个实例
    Then 这个请求的状态应该是"Enqueue"
    Given 玩家通过租户"xiamatest01"注册一个用户
    Given 用户申请一个实例
    Then 这个请求的状态应该是"InService"
    And 这个实例不应该收到"confirm"消息



  @smoke
  Scenario: 随机触发的实例申请不会是已达到实例上限的队列
    Given 设置paas的最大实例数为"2"
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置接入商"xiamatest"的实例上限和已用是个个数分别为"1000"和"999"
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
    Then paas收到的请求中应该不包含"InstanceApply"的请求
    Given 用户申请一个实例根据以下参数:
      |    key   |  value |
      | confirm |  False  |
    And 等待"2000"毫秒
    Then 这个请求的状态应该是"InService"


  @no_impl, @smoke
  Scenario: 用户释放实例会优先随机触发同一个router的请求申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"2"
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个实例
    Given 用户申请一个实例
    Given 用户申请一个路由为"3,4"的实例
    When 用户释放第"0"个实例
    Then 最后一个请求的状态应该是"InService"


  @no_impl, @smoke
  Scenario: 当释放的router没有请求时, 触发其他router的请求申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"2"
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个实例
    Given 用户申请一个实例
    When 用户释放第"0"个实例
    Then 最后一个请求的状态应该是"InService"

  @no_impl, @smoke
  Scenario: 当释放的router请求后, 第一个申请失败后, 会触发其他申请
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 设置paas的最大实例数为"2"
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个实例
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个实例
    When 设置paas处理"apply"请求失败"4"次
    When 用户释放第"0"个实例
    Then 最后一个请求的状态应该是"InService"


  @no_impl, @smoke
  Scenario: 服务会根据释放过的实例个数定时触发新的申请
  """
  cloudservice-return-count-${routekey}
  这个应该是全局的,而不是针对某个router的
  """
    Given 设置paas的最大实例数为"2"
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个实例
    Given 用户申请一个路由为"3,4"的实例
    Given 用户申请一个实例
    When 开始记录paas收到的请求
    And 更新路由"3,4"归还实例个数为"2"
    And 等待"5000"毫秒
    And 获取paas收到的请求
    Then paas收到的请求中应该包含"apply"的请求
    And 这个实例不应该收到"confirm"消息
    
    

  @no_impl, @smoke
  Scenario: 一个成功的释放才会增加释放实例个数
    """
    1. releaseInstanceFromPaas返回True的时候,会增加释放实例个数;
    需要确认http各种返回时, releaseInstanceFromPaas的返回值
    """
    Given 设置paas的最大实例数为"2"

