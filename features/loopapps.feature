Feature: 多次申请释放实例

  Scenario: 多次正常申请释放实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Then 用户正常申请释放实例"2000"次
    Then 接入商"xiamatest"已占用的实例个数应该为"default"


  Scenario: 多次短时间内申请释放实例
    Given 玩家通过租户"xiamatest"注册一个用户
    Given 用户短时间内申请释放实例"3000"次
    Then 接入商"xiamatest"已占用的实例个数应该为"default"