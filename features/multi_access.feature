Feature: multi-access key
  In order to increase the ninja survival rate,
  As a ninja commander
  I want my ninjas to decide whether to take on an
  opponent based on their skill levels

  Scenario: the request get the instance by priority
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
    Given I request a "random" app with "1000" priority
    Then I wait "1000" ms
    Given I request a "random" app with "1000" priority
    Then I wait "1000" ms
    Given I request a "random" app with "1001" priority
    Then I wait "1000" ms
    Given I registry an user with "xiamatest01" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest01" access key
    Given I request a "random" app with "1000" priority
    Then I wait "1000" ms
    Given I request a "random" app with "1000" priority
    Then I wait "1000" ms
    Given I request a "random" app with "10000" priority
    Then I wait "1000" ms
    Given I switch to the "0th" user
    When I try to stop the "0th" instance
    Then the status of instance should be "4"
    When I try to stop the "0th" instance
    Then the status of instance should be "4"
    Given I switch to the "1th" user
    When I try to stop the "0th" instance
    Then the status of instance should be "0"
    When I try to stop the "0th" instance
    Then the status of instance should be "4"



  Scenario: the different access key in the different queue
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then the index of instance should be "2"
    Given I registry an user with "xiamatest01" access key
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then the index of instance should be "2"
    When I try to stop the "0th" instance
    Then the index of instance should be "2"
    Given I switch to the "0th" user
    Then the index of instance should be "1"



  Scenario: one blocked access will not block others
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then the index of instance should be "1"
    Given I registry an user with "xiamatest01" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    Then I wait "1000" ms
    Given I request a "random" app
    Then the status of instance should be "4"


  Scenario: The same access in the different routers
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
    Given I request a "random" app with "2,4" route
    Then I wait "1000" ms
    Given I request a "random" app with "2,4" route
    Then the index of instance should be "1"
    Given I request a "random" app with "3,4" route
    Then the index of instance should be "1"
    Given I request a "random" app with "2,4" route
    Then the index of instance should be "2"
    Given I request a "random" app with "4,4" route
    Then the index of instance should be "1"
    Given I request a "random" app with "4,4" route
    Then the index of instance should be "2"

  Scenario: The same access in the different routers
    Given I registry an user with "xiamatest" access key
    Given I request a "noidle.test.test" app with "2,4" route
    Then I wait "1000" ms
    Given I request a "noidle.test.test1" app with "2,4" route
    Then the index of instance should be "2"
    Given I request a "noidle.test.test2" app with "2,4" route
    Then the index of instance should be "3"
    Then I change the max instance of paas to "1"
    Given I request a "random" app with "4,4" route
    Then I wait "1000" ms
    Given I request a "random" app with "4,4" route
    Then the index of instance should be "1"


  Scenario: push correct wating message when multi-router in one access
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I request a "random" app with "4,4" route
    Then I wait "1000" ms
    Given I request a "random" app with "4,4" route
    Then the index of instance should be "1"
    Given I request a "random" app with "100" priority
    Then the index of instance should be "1"
    Given I request a "random" app with "101" priority
    Then the index of instance should be "1"
    When I try to stop the "0th" instance
    Then the status of instance should be "4"

  Scenario: The higher priority will get the instance first when multi-router in one access
    popfirst会先将不是等待状态router的队列中去除优先级较高的申请
    如果都是等待的router队列, 那么将取出等待router队列中的优先级较高的申请
    router队列之间没有优先级, 或者是创建先后,或是字母排序
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given I request a "random" app with "4,4" route
    Then I wait "1000" ms
    Given I request a "random" app with "6,6" route
    Then the index of instance should be "1"
    Given I request a "random" app with "6,6" route
    Given I request a "random" app with "100" priority
    Then I wait "1000" ms
    Given I request a "random" app with "101" priority
    Then I wait "1000" ms
    When I try to stop the "0th" instance
    Then the status of instance should be "4"


  Scenario: The higher priority should not blocked others routes when multi-router in one access
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "2"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given I request a "random" app with "4,4" route
    Then I wait "1000" ms
    Given I request a "noidle.test.test" app with "100" priority
    Given I request a "noidle.test.test2" app with "100" priority
    Then I wait "1000" ms
    Given I request a "random" app with "4,4" route
    Then the status of instance should be "4"

  Scenario: one router which release will get the instance in higher priority
    router的优先级和router队列的创建时间相关. 这样就不能保证同一个同一个接入商优先级高的先获取实例
    执行之前需要重启saascore服务.
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "2"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given I request a "random" app with "100" priority
    Then I wait "2000" ms
    Given I request a "random" app with "4,4" route
    Then the status of instance should be "4"
    Given I request a "random" app with "6,6" route
    Given I request a "random" app with "100" priority
    Then I wait "2000" ms
    Given I request a "random" app with "4,4" route
    Then I wait "1000" ms
    When I try to stop the "1th" instance
    Then the status of instance should be "4"


Scenario: one router which release will get the instance when all router is await
    router的优先级和router队列的创建时间相关. 这样就不能保证同一个同一个接入商优先级高的先获取实例
    执行之前需要重启saascore服务
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "2"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given I request a "random" app with "100" priority
    Then I wait "2000" ms
    Given I request a "random" app with "4,4" route
    Then the status of instance should be "4"
    Given I request a "noidle.test1" app with "6,6" route
    Given I request a "noidle.test2" app with "100" priority
    Then I wait "2000" ms
    Given I request a "random" app with "4,4" route
    Then I wait "1000" ms
    When I try to stop the "1th" instance
    Then the status of instance should be "4"

  Scenario: one router releasing allow another router get the instance
    router的优先级和router队列的创建时间相关. 这样就不能保证同一个同一个接入商优先级高的先获取实例
    执行之前需要重启saascore服务
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "2"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given I request a "random" app with "4,4" route
    Given I request a "random" app with "4,4" route
    Then the status of instance should be "4"
    Given I request a "random" app with "6,6" route
    Given I request a "random" app with "100" priority
    Given I request a "random" app with "101" priority
    Then I wait "1000" ms
    When I try to stop the "0th" instance
    Then the status of instance should be "4"
