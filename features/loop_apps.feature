Feature: 是的发生地方

  Scenario: 申请实例
    Given 玩家通过租户"xiamatest"注册一个用户
#    When I request a app
#    And I wait "2000" ms
#    Then the status of instance should be "4"
#    And the instance num of "xiamatest" should be "501"



  Scenario: start and stop the instance normally
    Given I registry an user with "xiamatest" access key
    Given I start and stop the instance normally for "3000" times
    Then the instance num of "xiamatest" should be "default"