Feature: Full system integration tests

  Scenario: Create a user, profile, and orders successfully
    Given I have a user payload with name "mike" and email "mike@example.com"
    When I create the user via the API
    Then the user should exist in the database with the correct name and email
    When I create a profile for the user with bio "Hello, I'm mike"
    Then the profile should exist in the database with the correct user_id and bio "Hello, I'm mike"
    When I create two orders for the user "Laptop,1200" and "Mouse,50"
    Then the orders should exist in the database with the correct user_id, item_name, and price
    When I fetch the user details via the API
    Then the API response should include the profile and all orders

  Scenario: Fail to create profile for non-existing user
    Given no user exists with ID 9999
    When I try to create a profile via the API for user ID 9999
    Then the API response should return status code 409
    And the message should be "User id 9999 does not exists"

  Scenario: Fail to create order for non-existing user
    Given no user exists with ID 9999
    When I try to create an order via the API for user ID 9999
    Then the API response should return status code 404
    And the message should be "User does not exists"

  Scenario: Retrieve user with profile and orders
    Given a user exists with ID 1
    And a profile exists for user ID 1
    And multiple orders exist for user ID 1
    When I fetch user details via the API for user ID 1
    Then the API response should include the correct user info
    And the response should include the correct profile info
    And the response should include all orders for the user