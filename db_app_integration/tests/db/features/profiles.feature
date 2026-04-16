Feature: Profile Table DB operations

  Scenario: Create profile successfully
    Given a user exists with ID 1
    When I insert a profile with user_id 1 and bio "Hello World"
    Then the profile should exist in the database with correct user_id and bio

  Scenario: Fail to create duplicate profile for same user
    Given a profile already exists for user ID 1
    When I try to insert another profile for user ID 1
    Then the database should raise a uniqueness constraint error

  Scenario: Fail to create profile for non-existing user
    Given no user exists with ID 9999
    When I try to insert a profile with user_id 9999
    Then the database should raise a foreign key constraint error

  Scenario: Retrieve profile by user ID
    Given a profile exists for user ID 1
    When I query the profile by user ID 1
    Then the returned profile should have correct bio

  Scenario: Retrieve profile by profile ID
    Given a profile exists with profile ID 1
    When I query the profile by profile ID 1
    Then the returned profile should match the stored data

  Scenario: Update profile bio
    Given a profile exists for user ID 1
    When I update the profile bio to "Newly updated bio"
    Then the database should reflect the updated bio

  Scenario: Delete profile by user ID
    Given a profile exists for user ID 1
    When I delete the profile using user ID 1
    Then the profile should not exist in the database

  Scenario: Delete profile by profile ID
    Given a profile exists with profile ID 4
    When I delete the profile using profile ID 4
    Then the profile should not exist in the database