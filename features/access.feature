Feature: the feature on access
"""
    receive and send data via access
"""

  Scenario: disconnet WebSocket for less 1 minute
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    When I disconnet the websocket of instance for "50" seconds
    And I reconnect the websocket of instance
    And I wait "20000" ms
    Then the status of instance should be "4"


  Scenario: disconnet WebSocket for more than 1 minute
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    When I disconnet the websocket of instance for "70" seconds
    Then the instance should be deleted successfully

  Scenario: disconnet WebSocket for several times
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    When I disconnet the websocket of instance for "20" seconds
    And I reconnect the websocket of instance
    Then I wait "20000" ms
    When I disconnet the websocket of instance for "40" seconds
    And I reconnect the websocket of instance
    Then the status of instance should be "4"
    When I disconnet the websocket of instance for "70" seconds
    Then the instance should be deleted successfully

  Scenario: play the game without ping message
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
    When I request an "random" app with
      |    key    |      value        |
      |    ping    |                 |
    Then I wait "60000" ms for overtime
    Then the instance should be deleted successfully
