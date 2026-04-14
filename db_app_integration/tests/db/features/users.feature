Feature: User Table DB operations

  Scenario: Create a new user successfully
    Given I have a user payload with name "john" and email "john@example.com"
    When I insert the user into the users table
    Then the user should exist in the database with the correct name and email

  Scenario: Fail to insert user with duplicate name
    Given a user already exists with name "mike" and email "mike@example.com"
    When I try to insert another user with name "mike" and email "mike_new@example.com"
    Then the database should raise a uniqueness constraint error

  Scenario: Fail to insert user with duplicate email
    Given a user already exists with name "kate" and email "kate@example.com"
    When I try to insert another user with name "ford" and email "kate@example.com"
    Then the database should raise a uniqueness constraint error

  Scenario: Retrieve user by ID
    Given a user exists with ID 1
    When I query the users table for user ID 1
    Then the returned record should have correct name and email

  Scenario: Retrieve user by name
    Given a user exists with name "john"
    When I query the users table by name "john"
    Then the returned record should match the user details

  Scenario: Retrieve user by email
    Given a user exists with email "john@example.com"
    When I query the users table by email "john@example.com"
    Then the returned record should match the user details

  Scenario: Update user details
    Given a user exists with ID 1
    When I update the user's name to "john_updated" and email to "john_updated@example.com"
    Then the database should reflect the updated values

  Scenario: Delete user by ID
    Given a user exists with ID 1
    When I delete the user from the users table
    Then the user should not exist in the database