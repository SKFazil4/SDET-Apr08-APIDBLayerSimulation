Feature: Profile Table DB operations

  Scenario: Create a profile for a user successfully
    Given a user exists with ID 1
    And I have a profile payload with user_id 1 and bio "Hello, I'm Alice"
    When I insert the profile into the profiles table
    Then the profile should exist with the correct user_id and bio

  Scenario: Fail to create profile for non-existing user
    Given no user exists with ID 9999
    When I try to insert a profile with user_id 9999
    Then the database should raise a foreign key constraint error

  Scenario: Fail to create duplicate profile for the same user
    Given a profile already exists for user ID 1
    When I try to insert another profile for user ID 1
    Then the database should raise a uniqueness constraint error

  Scenario: Retrieve profile by user ID
    Given a profile exists for user ID 1
    When I query the profiles table by user ID 1
    Then the returned profile should have the correct bio