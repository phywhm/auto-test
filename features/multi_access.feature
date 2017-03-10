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



  Scenario: one blocked access will not block another
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
