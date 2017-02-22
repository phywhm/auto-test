Feature: all kinds of scenarios on resolution

    Scenario: request an app with displayinfo on PC
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           | resolution|      1200x9000    |
           |  dpi      |       300         |
           | os_type   |       1           |
        Then the dpi of client display should be "300"
        And the resolution of client display should be "1200x9000"

    Scenario: request an app with displayinfo on iPhone6Plus
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           |   model   |   iPhone6Plus     |
           | os_type   |       4           |
        Then the dpi of client display should be "401"
        And the resolution of client display should be "1080x1920"


    Scenario: request an app with displayinfo on IOS
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           |   model   |      iPhone6      |
           | os_type   |       4           |
        Then the dpi of client display should be "326"
        And the resolution of client display should be "750x1334"


    Scenario: request an app with specified displayinfo on IOS
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           |   model   |      iPhone6      |
           | os_type   |       4           |
           |  dpi      |       300         |
           | resolution|      1200x9000    |
        Then the dpi of client display should be "326"
        And the resolution of client display should be "750x1334"


    Scenario: request an app with displayinfo on Andriod
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           | resolution|      1200x9000    |
           |  dpi      |       300         |
           | os_type   |       2           |
        Then the dpi of client display should be "300"
        And the resolution of client display should be "1200x9000"



    Scenario: request an app with displayinfo on web
    """I set the default modle to iPhone6"""
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           | resolution|      1200x9000     |
           |  dpi      |       300         |
           | os_type   |       3           |
        Then the dpi of client display should be "300"
        And the resolution of client display should be "1200x9000"



    Scenario: request an app with default displayinfo on PC
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           | os_type   |       1           |
        Then the dpi of client display should be "-1"
        And the resolution of client display should be "-1x-1"


    Scenario: request an app with default displayinfo on IOS
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           | os_type   |       4           |
           |   model   |      iPhone       |
        Then the dpi of client display should be "null"
        And the resolution of client display should be "null"


    Scenario: request an app with default displayinfo on Andriod
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           | os_type   |       2           |
        Then the dpi of client display should be "320"
        And the resolution of client display should be "1920x1080"

    Scenario: request an app with default displayinfo on web
        Given I registry an user with "xiamatest" access key
        When I request an "random" app with
           |    key    |      value        |
           | os_type   |       3           |
        Then the dpi of client display should be "320"
        And the resolution of client display should be "1920x1080"
      
  Scenario: reqest the an app without resolution info
    Given I registry an user with "xiamatest" access key
    Given I request a "random" app
    Then the status of instance should be "4"
    Then the ID of resolution info should be "2"
    And the bit rate of resolution info should be "1600000"
    And the resolution of resolution info should be "1280x720"


  Scenario: reqest the an app with resolution info
    Given I registry an user with "xiamatest" access key
    When I request an "random" app with
      |    key     |      value    |
      | push_resolution |      1        |
    Then the status of instance should be "4"
    Then the ID of resolution info should be "1"
    And the bit rate of resolution info should be "800000"
    And the resolution of resolution info should be "1280x720"

  Scenario: reqest the an app with a disable resolution info
    Given I registry an user with "xiamatest" access key
    When I request an "random" app with
      |    key     |      value    |
      | push_resolution |      4        |
    Then the status of instance should be "4"
    Then the ID of resolution info should be "4"
    And the bit rate of resolution info should be "4000000"
    And the resolution of resolution info should be "1280x720"

  Scenario: change the resolution
    Given I registry an user with "xiamatest" access key
    When I request an "random" app with
      |    key     |      value    |
      | push_resolution |      4        |
    Then the status of instance should be "4"
    Then the ID of resolution info should be "4"
    When I change the resolution of instance with the "1th" ID
    Then the instance should contain "changeResolution" message
    Then the instance should receive "address" message

  Scenario: chang resolution when the status of instance is 0
    Given I registry an user with "xiamatest" access key
    Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then I wait "1000" ms
    When I change the resolution of instance with the "1th" ID
    Then the status of instance should be "0"
    And the instance should receive "waiting" message
    And the instance num of "xiamatest" should be "501"


  Scenario: chang resolution when the status of instance is 3
    Given I registry an user with "xiamatest" access key
    Given I change the callback interval of paas to "120000"
    Given I request a "random" app
    Then I wait "1000" ms
    When I change the resolution of instance with the "1th" ID
    Then the status of instance should be "3"
    And the instance should receive "ready" message
    And the instance num of "xiamatest" should be "501"

  Scenario: refresh stoken when one user have 5 instances
    Given I registry an user with "xiamatest" access key
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then I wait "1000" ms
    Given I request a "random" app
    Then the status of instance should be "4"
    When I change the resolution of instance with the "1th" ID
    Then the status of instance should be "4"
    And the instance should receive "address" message
    And the instance num of "xiamatest" should be "505"

  #TODO: this scenario do not work, have to stop the mock server
  """
  Scenario: change the resolution and the pass return null
    Given I registry an user with "xiamatest" access key
    When I request an "random" app with
      |    key     |      value    |
      | push_resolution |      4        |
    Then the status of instance should be "4"
    Then the instance num of "xiamatest" should be "501"
    Then the ID of resolution info should be "4"
    When I change the resolution of instance with the "0th" ID
    Then the instance num of "xiamatest" should be "500"
  """