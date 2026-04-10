Feature: User API

  Scenario: Create a new user successfully
    Given I have a user payload with name "Bob" and email "Bob@example.com"
    When I send POST request to "/users"
    Then the response status code should be 200
    And the response should contain user name "Bob" and email "Bob@example.com"

  Scenario: Fail to create user with duplicate name
    Given a user already exists with name "Alice"
    When I send POST request to "/users" with name "Alice" and email "alice2@example.com"
    Then the response status code should be 409
    And the response message should be "User name already exists"

  Scenario: Fail to create user with duplicate email
    Given a user already exists with email "alice@example.com"
    When I send POST request to "/users" with name "Alice2" and email "alice@example.com"
    Then the response status code should be 409
    And the response message should be "User mail already exists"

  Scenario: Get user by ID successfully
    Given a user exists with ID 1
    When I send GET request to "/users/1"
    Then the response status code should be 200
    And the response should contain user ID 1

  Scenario: Get user by invalid ID
    When I send GET request to "/users/9999"
    Then the response status code should be 404
    And the response message should be "User not exists"