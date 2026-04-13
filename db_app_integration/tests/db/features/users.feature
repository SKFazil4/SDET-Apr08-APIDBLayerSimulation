Feature: User Table DB operations

  Scenario: Create a new user successfully
    Given I have a user payload with name "john" and email "john@example.com"
    When I insert the user into the users table
    Then the user should exist in the database with the correct name and email

  Scenario: Fail to insert user with duplicate name
    Given a user already exists with name "mike" and email "mike@example.com"
    When I try to insert another user with name "mike" and email "mike@example.com"
    Then the database should raise a uniqueness constraint error

  Scenario: Fail to insert user with duplicate email
    Given a user already exists with name "kate" and email "kate@example.com"
    When I try to insert another user with name "ford" and email "kate@example.com"
    Then the database should raise a uniqueness constraint error

  Scenario: Retrieve user by ID
    Given a user exists with ID 1
    When I query the users table for user ID 1
    Then the returned record should have user ID 1 the correct name and email