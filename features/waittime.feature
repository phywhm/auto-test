# Created by xiama at 12/20/16
Feature: show the estimated time via configuration
  # Enter feature description here

  Scenario: The instance should receive timestr when there is not enough instances
    Given I registry an user with "xiamatest" access key
    Then I change the max instance of paas to "1"
    Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    Given I request a "random" app
    Then the status of instance should be "0"
    Given I request a "random" app
    Then the status of instance should be "0"
    Then the index of instance should be "2"
    And the wait message should contain "timeStr"
    Then I try to stop the "1th" instance
    Then the index of instance should be "1"
    And the wait message should contain "timeStr"

  Scenario: The instance should receive timestr when reach the instance limit
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    Given I request a "random" app
    Then the status of instance should be "0"
    Given I request a "random" app
    Then the status of instance should be "0"
    Then the index of instance should be "2"
    And the wait message should contain "timeStr"
    Then I try to stop the "1th" instance
    Then the index of instance should be "1"
    And the wait message should contain "timeStr"
