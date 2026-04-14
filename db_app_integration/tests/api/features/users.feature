Feature: User API

  Scenario: Create a new user successfully
    Given I have a user payload with name "Bob" and email "bob@example.com"
    When I send POST request to "/users"
    Then the response status code should be 200
    And the response should contain user name "Bob" and email "bob@example.com"
    And the response should contain a valid user ID

  Scenario: Fail to create user with duplicate name
    Given a user already exists with name "Alice" and email "alice@example.com"
    When I send POST request to "/users" with name "Alice" and email "alice_new@example.com"
    Then the response status code should be 409
    And the response message should be "Username Alice already exists"

  Scenario: Fail to create user with duplicate email
    Given a user already exists with email "alice@example.com"
    When I send POST request to "/users" with name "Alice2" and email "alice@example.com"
    Then the response status code should be 409
    And the response message should be "User mail alice@example.com already exists"

  Scenario: Get all users successfully
    Given multiple users exist
    When I send GET request to "/users"
    Then the response status code should be 200
    And the response should be a list of users

  Scenario: Get user by ID successfully
    Given a user exists with ID 1
    When I send GET request to "/users/id/1"
    Then the response status code should be 200
    And the response should contain user ID 1
    And the response should contain name and email

  Scenario: Get user by invalid ID
    When I send GET request to "/users/id/9999"
    Then the response status code should be 404
    And the response message should be "User id 9999 not exists"

  Scenario: Get user by name successfully
    Given a user exists with name "Bob"
    When I send GET request to "/users/name/Bob"
    Then the response status code should be 200
    And the response should contain user name "Bob"

  Scenario: Get user by email successfully
    Given a user exists with email "bob@example.com"
    When I send GET request to "/users/email/bob@example.com"
    Then the response status code should be 200
    And the response should contain email "bob@example.com"

  Scenario: Update user successfully
    Given a user exists with ID 1
    When I send PUT request to "/users/id/1" with name "BobUpdated" and email "bob_updated@example.com"
    Then the response status code should be 200
    And the response should contain updated name "BobUpdated" and email "bob_updated@example.com"

  Scenario: Fail to update non-existing user
    When I send PUT request to "/users/id/9999"
    Then the response status code should be 404

  Scenario: Delete user successfully
    Given a user exists with ID 1
    When I send DELETE request to "/users/id/1"
    Then the response status code should be 200
    And the response message should confirm deletion

  Scenario: Fail to delete non-existing user
    When I send DELETE request to "/users/id/9999"
    Then the response status code should be 404