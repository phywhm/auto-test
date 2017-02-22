Feature: all kinds of scenarios on Stoken

    Scenario: refresh stoken when the status of instance is 0
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then I wait "1000" ms
        Given I request a "random" app
        Then I wait "1000" ms
        When I refresh the stoken of instance
        Then the status of instance should be "0"
        And the instance should receive "waiting" message
        And the instance num of "xiamatest" should be "501"

    Scenario: refresh stoken when the status of instance is 3
        Given I registry an user with "xiamatest" access key
        Given I change the callback interval of paas to "120000"
        Given I request a "random" app
        Then I wait "1000" ms
        When I refresh the stoken of instance
        Then the status of instance should be "3"
        And the instance should receive "ready" message
        And the instance num of "xiamatest" should be "501"


    Scenario: refresh stoken when the status of instance is 4
        Given I registry an user with "xiamatest" access key
        Given I request a "random" app
        Then I wait "1000" ms
        Then the status of instance should be "4"
        When I refresh the stoken of instance
        Then the status of instance should be "4"
        And the instance should receive "address" message
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
        When I refresh the stoken of instance
        Then the status of instance should be "4"
        And the instance should receive "address" message
        And the instance num of "xiamatest" should be "505"


     #TODO: should complete run shell command on server
"""
    Scenario: refresh stoken when there is no instance record
        Given I registry an user with "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I try to stop the instance
        When I refresh the stoken of instance
        And the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
"""