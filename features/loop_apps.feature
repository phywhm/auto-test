Feature: 是的发生地方

  Scenario: 申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Then 用户正常申请释放实例"2000"次
    Then 接入商"xiamatest"已占用的实例个数应该为"default"
#    When I request a app
#    And I wait "2000" ms
#    Then the status of instance should be "4"
#    And the instance num of "xiamatest" should be "501"



  Scenario: start and stop the instance normally
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户短时间内申请释放实例"3000"次
    Then 接入商"xiamatest"已占用的实例个数应该为"default"