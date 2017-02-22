Feature: start and stop the instance

    Scenario: request a normal game
        Given I registry an user with "xiamatest" access key
        Given I request a "random" app
        And I wait "2000" ms
        Then the instance should receive "address" message
        Then the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        When I try to stop the instance
        And I wait "2000" ms
        Then the instance should be deleted successfully
        And the instance num of "xiamatest" should be "default"

    Scenario: request a game that need to download
        Given I registry an user with "xiamatest" access key
        Given I change the callback interval of paas to "120000"
        Given I request a "random" app
        And I wait "2000" ms
        Then the status of instance should be "3"
        Then I wait "120000" ms
        Then the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        When I try to stop the instance
        And I wait "2000" ms
        Then the instance should be deleted successfully
        And the instance num of "xiamatest" should be "default"

    Scenario: request a non-existed game
        Given I registry an user with "xiamatest" access key
        Given I request a "wrong" app
        And I wait "2000" ms
        Then the instance should be deleted successfully
        And the instance num of "xiamatest" should be "default"


    Scenario: request a game with playtime
        Given I registry an user with "xiamatest" access key
        Given I request a "random" app with "90000" time
        And I wait "2000" ms
        Then the instance should receive "address" message
        Then the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        And I wait "90000" ms for overtime
        Then the instance should be deleted successfully
        And the instance num of "xiamatest" should be "default"

    Scenario: stop the instance with 0 status in applying
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Then the instance num of "xiamatest" should be "501"
        When I try to stop the "1th" instance
        Then the instance should be deleted successfully
        And I try to stop the "0th" instance
        And I try to stop the "0th" instance
        Then i wait "2000" ms
        Then the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"


    Scenario: stop the instance with 0 status in queue
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Then the instance num of "xiamatest" should be "501"
        When I try to stop the "1th" instance
        Then the instance should be deleted successfully
        And I try to stop the "0th" instance
        Then the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"

    Scenario: stop the instance which applied but in queue
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app with "1000" priority
        And I wait "1000" ms
        Given I request a "random" app with "2000" priority
        And I wait "1000" ms
        Then the instance num of "xiamatest" should be "501"
        When I try to stop the "1th" instance
        Then the instance should be deleted successfully
        Then the status of instance should be "0"
        And I try to stop the "0th" instance
        Then the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"


    Scenario: stop the instance with 3 status
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I change the callback interval of paas to "120000"
        Given I request a "random" app
        And I wait "1000" ms
        Then the status of instance should be "3"
        Given I request a "random" app
        And I wait "1000" ms
        Then the instance num of "xiamatest" should be "501"
        Given I change the callback interval of paas to "1000"
        And I try to stop the "0th" instance
        Then the instance should be deleted successfully
        Then I wait "100000" ms
        Then the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"


    Scenario: the playing time does not include the waiting time
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I request a "random" app with "90000" time
        Then I wait "1000" ms
        Given I request a "random" app with "90000" time
        Then I wait "60000" ms
        When I try to stop the "0th" instance
        And I wait "30000" ms
        Then the status of instance should be "4"
        When I wait "50000" ms
        Then the status of instance should be "4"
        When I wait "10000" ms
        Then the instance should receive "overtime" message

    Scenario: one user request 5 instance
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Given I request a "random" app
        And I wait "1000" ms
        Then the status of instance should be "0"

    Scenario: re-request the app when the status is 0
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then I wait "1000" ms
        Given I request a "random" app
        Then I wait "1000" ms
        When I re-request the app again
        Then the status of instance should be "0"
        And the instance should receive "waiting" message
        And the instance num of "xiamatest" should be "501"
"""
    Scenario: re-request the app when the status is 1
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I request a "random" app
        Then I wait "1000" ms
        Given I request a "random" app
        Then I wait "1000" ms
        When I re-request the app again
        Then the status of instance should be "0"
        And the instance should receive "apply" message
        And the instance num of "xiamatest" should be "501"
"""

    Scenario: re-request the app when the status is 3
        Given I registry an user with "xiamatest" access key
        Given I change the callback interval of paas to "120000"
        Given I request a "random" app
        Then I wait "1000" ms
        When I re-request the app again
        Then the status of instance should be "3"
        And the instance should receive "ready" message
        And the instance num of "xiamatest" should be "501"


    Scenario: re-request the app when the status is 4
        Given I registry an user with "xiamatest" access key
        Given I request a "random" app
        Then I wait "1000" ms
        Then the status of instance should be "4"
        When I re-request the app again
        Then the status of instance should be "4"
        And the instance should receive "address" message
        And the instance num of "xiamatest" should be "501"
