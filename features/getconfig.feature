# Created by xiama at 11/29/16

Feature: the test scenarios on geting configuration
  # Enter feature description here

  Scenario: Get the configuration without configuration in configuration server
    Given I registry an user with "xiamatest" access key
    When I get the configuration
    Then the vaule of "toast_countdown" should be "您本次云玩时间还剩 |。" in tips



  Scenario: Get the configuration with the configuration in configuration server
    Given I registry an user with "xiamatest" access key
    When I get the configuration
    Then the vaule of "toast_countdown" should be "xxxxx-您本次云玩时间还剩 |。" in tips


  Scenario: Get the configuration only without tips configuration in configuration server
    Given I registry an user with "xiamatest01" access key
    When I get the configuration
    Then the vaule of "toast_countdown" should be "您本次云玩时间还剩 |。" in tips

