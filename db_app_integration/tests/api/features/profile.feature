Feature: Profile API

  Scenario: Create profile successfully
    Given a user exists with ID 10
    And I have a profile payload with user_id 10 and bio "Hello, I'm Bob"
    When I send POST request to "/profiles"
    Then the response status code should be 200
    And the response should contain user_id 10 and bio "Hello, I'm Bob"

  Scenario: Fail to create profile for non-existing user
    Given no user exists with ID 9999
    And I have a profile payload with user_id 9999 and bio "Ghost"
    When I send POST request to "/profiles"
    Then the response status code should be 409
    And the response message should be "User id 9999 does not exists"

  Scenario: Fail to create duplicate profile
    Given a profile already exists for user ID 10
    When I send POST request to "/profiles" with user_id 10
    Then the response status code should be 409
    And the response message should be "User profile already exists"

  Scenario: Get all profiles successfully
    Given multiple profiles exist
    When I send GET request to "/profiles"
    Then the response status code should be 200
    And the response should be a list of profiles

  Scenario: Get profile by user ID successfully
    Given a profile exists for user ID 10
    When I send GET request to "/profiles/userid/10"
    Then the response status code should be 200
    And the response should contain user_id 10 and bio

  Scenario: Fail to get profile for non-existing user
    When I send GET request to "/profiles/userid/9999"
    Then the response status code should be 404
    And the response message should be "User not exists"

  Scenario: Get profile by profile ID successfully
    Given a profile exists with profile ID 7
    When I send GET request to "/profiles/profileid/7"
    Then the response status code should be 200
    And the response should contain profile ID 7

  Scenario: Update profile successfully
    Given a profile exists for user ID 2
    When I send PUT request to "/profiles/id/2" with bio "Updated Bio"
    Then the response status code should be 200
    And the response should contain updated bio "Updated Bio"

  Scenario: Fail to update profile for non-existing user
    When I send PUT request to "/profiles/id/9999" with bio "Updated Bio"
    Then the response status code should be 404

  Scenario: Delete profile by user ID
    Given a profile exists for user ID 2
    When I send DELETE request to "/profiles/userid/2"
    Then the response status code should be 200

  Scenario: Delete profile by profile ID
    Given a profile exists with profile ID 8
    When I send DELETE request to "/profiles/profileid/8"
    Then the response status code should be 200

  Scenario: Fail to delete non-existing profile
    When I send DELETE request to "/profiles/profileid/9999"
    Then the response status code should be 404