Feature: Profile API

  Scenario: Create profile successfully
    Given a user exists with ID 1
    And I have a profile payload with user_id 1 and bio "Hello, I'm Alice"
    When I send POST request to "/profiles"
    Then the response status code should be 200
    And the response should contain user_id 1 and bio "Hello, I'm Alice"

  Scenario: Fail to create profile for non-existing user
    Given no user exists with ID 9999
    When I send POST request to "/profiles" with user_id 9999 and bio "Ghost"
    Then the response status code should be 409
    And the response message should be "User does not exists"

  Scenario: Fail to create profile if it already exists
    Given a profile already exists for user ID 1
    When I send POST request to "/profiles" with user_id 1
    Then the response status code should be 409
    And the response message should be "User profile already exists"

  Scenario: Get profile by user ID successfully
    Given a profile exists for user ID 1
    When I send GET request to "/profiles/1"
    Then the response status code should be 200
    And the response should contain user_id 1