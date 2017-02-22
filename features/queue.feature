Feature: test the feature on the queue
"""
    make sure that all kinds of releasing can make the next request work fine
"""

    Scenario Outline: notifying error status will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I notify the "0th" instance with "<status>" status
        Then the deleted instance should receive "error" message
        And the instance should receive "address" message
        And the status of instance should be "4"
        When I notify the "0th" instance with "<status>" status
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"
        Examples:
            | status |
            |   02   |
            |   10   |
            |   11   |
            |   12   |
            |   13   |
            |   24   |
            |   32   |


    Scenario: notifying 20 status will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        #Then I wait "100000" ms
        When I notify the "0th" instance with "20" status
        Then the deleted instance should receive "kicked" message
        And the instance should receive "address" message
        And the status of instance should be "4"
        When I notify the "0th" instance with "20" status
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"



    Scenario: stop the playing game will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I try to stop the "0th" instance
        Then the instance should receive "address" message
        And the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        When I try to stop the "0th" instance
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: overtime will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "90000" time
        Then the status of instance should be "4"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        When I wait "90000" ms
        Then the instance should receive "address" message
        And the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        When I wait "90000" ms
        Then the instance should receive "overtime" message
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: disconneting websocket will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "90000" time
        Then the status of instance should be "4"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        Then the instance should receive "address" message
        And the status of instance should be "4"
        And the instance num of "xiamatest" should be "501"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: requesting wrong game will reduce the instance count when limit le real instance count
        Given I registry an user with "xiamatest" access key
        Given I update the instance limit to 501 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "noapp.package.name" app
        Then the status of wrong instance should be "0"
        Given I request a "noapp.package1.name" app
        Then the status of wrong instance should be "0"
        When I try to stop the "0th" instance
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario Outline: notifying error status will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I notify the first real instance with "<status>" status
        Then the deleted instance should receive "error" message
        And the instance num of "xiamatest" should be "501"
        When I notify the first real instance with "<status>" status
        Then the status of instance should be "4"
        And the instance should receive "address" message
        And the status of instance should be "4"
        When I notify the "0th" instance with "<status>" status
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"
        Examples:
            | status |
            |   02   |
            |   10   |
            |   11   |
            |   12   |
            |   13   |
            |   24   |
            |   32   |


    Scenario: notifying 20 status will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I notify the first real instance with "20" status
        Then the deleted instance should receive "kicked" message
        When I notify the first real instance with "20" status
        Then the status of instance should be "4"
        And the instance should receive "address" message
        And the instance num of "xiamatest" should be "501"
        When I notify the "0th" instance with "20" status
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"



    Scenario: stop the playing game will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "random" app
        Then the status of instance should be "0"
        Given I request a "random" app
        Then the status of instance should be "0"
        When I try to stop the "0th" instance
        #And the instance num of "xiamatest" should be "502"
        When I try to stop the "0th" instance
        Then the instance should receive "address" message
        And the status of instance should be "4"
        #And the instance num of "xiamatest" should be "501"
        When I try to stop the "0th" instance
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: overtime will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "90000" time
        Then the status of instance should be "4"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        When I wait "90000" ms
        Then the instance num of "xiamatest" should be "501"
        When I wait "185000" ms
        Then the instance should receive "overtime" message
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: disconneting websocket will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app with "90000" time
        Then the status of instance should be "4"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        Given I request a "random" app with "90000" time
        Then the status of instance should be "0"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        And the instance num of "xiamatest" should be "501"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        Then the instance should receive "address" message
        And the status of instance should be "4"
        When I disconnet websocket for the "0th" instance
        And I wait "60000" ms
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"


    Scenario: requesting wrong game will reduce the instance count when limit gt real instance count
        Given I registry an user with "xiamatest" access key
        Then I change the max instance of paas to "1"
        Given I update the instance limit to 502 and count to 500 on "xiamatest" access key
        Given I request a "random" app
        Then the status of instance should be "4"
        Given I request a "noapp.package.name" app
        Then the wrong instance should receive "error" message
        Given I request a "noapp.package1.name" app
        Then the wrong instance should receive "error" message
        When I try to stop the "0th" instance
        Then the instance num of "xiamatest" should be "500"
        Given I request a "random" app
        Then the status of instance should be "4"
        Then the instance num of "xiamatest" should be "501"
