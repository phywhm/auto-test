Feature: test
  In order to increase the ninja survival rate,
  As a ninja commander
  I want my ninjas to decide whether to take on an
  opponent based on their skill levels


  Scenario: the wait request will kicked before 5 minutes
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I request a "random" app
    Then the status of instance should be "4"
    Given I request a "random" app
    Then the status of instance should be "0"
    Then I send maintenance message for "1" minutes in "6" minutes
    And I wait "60000" ms
    Then the instance should receive "readystop" message
    And the instance is kicked from queue
    When I wait "300000" ms
    Then the instance should receive "stopped" message
    When I wait "60000" ms
    Then the instance should receive "resume" message


  Scenario: the playing request will kicked when the service is stopped
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I request a "random" app
    Then the status of instance should be "4"
    Then I send maintenance message for "1" minutes in "6" minutes
    And I wait "60000" ms
    Then the instance should receive "readystop" message
    Then the status of instance should be "4"
    When I wait "300000" ms
    And the instance is kicked from queue
    Then the instance should receive "stopped" message
    When I wait "60000" ms
    Then the instance should receive "resume" message

  Scenario: the wait request will kicked when stop service between 0 and 5
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I request a "random" app
    Then the status of instance should be "4"
    Given I request a "random" app
    Then the status of instance should be "0"
    Then I send maintenance message for "1" minutes in "2" minutes
    Then the instance should receive "stop" message
    And the instance is kicked from queue
    When I wait "120000" ms
    Then the instance should receive "stopped" message
    When I wait "60000" ms
    Then the instance should receive "resume" message

  Scenario: the playing request will not kicked when stop service between 0 and 5
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I request a "random" app
    Then the status of instance should be "4"
    Then I send maintenance message for "1" minutes in "2" minutes
    Then the instance should receive "stop" message
    Then the status of instance should be "4"
    When I wait "120000" ms
    And the instance is kicked from queue
    Then the instance should receive "stopped" message
    When I wait "60000" ms
    Then the instance should receive "resume" message

  Scenario: the playing request can refresh and change resolution before stop
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I request a "random" app
    Then the status of instance should be "4"
    Then I send maintenance message for "1" minutes in "6" minutes
    Then the status of instance should be "4"
    Then I refresh the stoken of instance
    And the instance should receive "stoken" message
    When I change the resolution of instance with the "1th" ID
    And the instance should receive "resolution" message

Scenario: the playing request can refresh and change when stop service between 0 and 5
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I request a "random" app
    Then the status of instance should be "4"
    Then I send maintenance message for "1" minutes in "2" minutes
    Then the instance should receive "stop" message
    Then the status of instance should be "4"
    When I wait "120000" ms
    And the instance is kicked from queue
    Then the instance should receive "stopped" message
    When I wait "60000" ms
    Then the instance should receive "resume" message

  Scenario: request an app when the server is maintenaning
    Given I registry an user with "xiamatest" access key
    Given I send maintenance message for "1" minutes in "6" minutes
    Given I request a "random" app
    Then the status of instance should be "4"
    And I wait "60000" ms
    Given I request a "random" app
    Then the instance should receive "stopp" message
    When I wait "300000" ms
    Given I request a "random" app
    Then the instance should receive "stopped" message
    When I wait "60000" ms
    Given I request a "random" app
    Then the status of instance should be "4"


  Scenario: cancel the maintenance will stop the scheduled timer
    Given I registry an user with "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    Given I send maintenance message for "1" minutes in "6" minutes
    Then I recover the service right now
    Then the instance should not contain "cancelstop" message
    And I wait "60000" ms
    Then the instance should not contain "readystop" message
    When I wait "300000" ms
    Given I request a "random" app
    Then the instance should not contain "stopped" message
    When I wait "60000" ms
    Then the instance should not contain "resume" message
    
  Scenario: cancel the maintenance between 0 and 5
    Given I registry an user with "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    Given I send maintenance message for "1" minutes in "6" minutes
    Then I wait "120000" ms
    Then I recover the service right now
    Then the instance should receive "cancelstop" message
    When I wait "240000" ms
    Given I request a "random" app
    Then the instance should not contain "stopped" message
    When I wait "60000" ms
    Then the instance should not contain "resume" message

  Scenario: cancel the maintenance after stopped
    Given I registry an user with "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    Given I send maintenance message for "1" minutes in "2" minutes
    Then I wait "120000" ms
    Then I recover the service right now
    Then the instance should receive "resume" message
    When I wait "60000" ms
    Then the instance should contain "resume" message "1" times