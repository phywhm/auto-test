Feature: the priority and the notifying message
"""
    The priority and the notifying message
"""

    Scenario: the request get the instance by priority
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "1000" priority
        Then I wait "1000" ms
        Given I request a "random" app with "1000" priority
        Then I wait "1000" ms
        Given I request a "random" app with "1001" priority
        Then I wait "1000" ms
        When I try to stop the "0th" instance
        Then the status of instance should be "4"
        When I try to stop the instance
        Then the status of instance should be "4"


    Scenario: the index of instance when there is enough instances
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "1000" priority
        And I wait "500" ms
        Given I request a "random" app with "1000" priority
        Then the index of instance should be "1"
        Given I request a "random" app with "1000" priority
        Then the index of instance should be "2"
        Given I registry an user with "xiamatest" access key
        Given I request a "random" app with "1002" priority
        Then the index of instance should be "1"
        When I request a "random" app with "1000" priority
        Then the index of instance should be "4"
        Given I switch to the "0th" user
        Given I request a "random" app with "1001" priority
        Then the index of instance should be "2"
        When I switch to the "1th" user
        Then the index of instance should be "5"
        When I try to stop the "0th" instance
        Then the index of instance should be "4"
        When I try to stop the "2th" instance
        Then the index of instance should be "3"


    Scenario: the index of instance when there is not enough instances
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I request a "random" app with "1000" priority
        And I wait "500" ms
        Given I request a "random" app with "1000" priority
        And I wait "500" ms
        Given I request a "random" app with "1000" priority
        Then the index of instance should be "2"
        Given I registry an user with "xiamatest" access key
        Given I request a "random" app with "1002" priority
        Then the index of instance should be "1"
        When I request a "random" app with "1000" priority
        Then the index of instance should be "4"
        Given I switch to the "0th" user
        Given I request a "random" app with "1001" priority
        Then the index of instance should be "2"
        When I switch to the "1th" user
        Then the index of instance should be "5"
        When I try to stop the "0th" instance
        Then the index of instance should be "4"
        When I try to stop the "2th" instance
        Then the index of instance should be "3"
