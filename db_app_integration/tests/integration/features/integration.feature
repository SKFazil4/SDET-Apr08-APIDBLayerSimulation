Feature: Full system integration tests (API + DB)

  ########################################
  # CREATE + FULL FLOW
  ########################################

  Scenario: Create a user, profile, and orders successfully
    Given I have a user payload with name "kate" and email "kate@example.com"
    When I create the user via the API
    Then the user should exist in the database with the correct name and email

    When I create a profile for the user with bio "Hello, I'm kate"
    Then the profile should exist in the database with the correct user_id and bio

    When I create two orders for the user "[{"item":"Laptop","price":1200},{"item":"Mouse","price":50}]"
    Then the orders should exist in the database with correct details

    When I fetch the user details via the API
    Then the API response should include correct user info

  ########################################
  # USER APIs
  ########################################

  Scenario: Get all users
    Given multiple users exist
    When I fetch all users via the API
    Then the API response should return all users
    And the database should contain the same number of users

  Scenario: Get user by name and email
    Given a user exists with name "john" and email "john@example.com"
    When I fetch user by name "john"
    Then the API response of user should match the database record
    When I fetch user by email "john@example.com"
    Then the API response of user should match the database record

  Scenario: Update user and validate DB sync
    Given a user exists with ID 8
    When I update the user with name "jake" and email "jake@gmail.com"
    Then the API response should reflect updated values
    And the database should reflect updated values

  Scenario: Fail to update user with duplicate name/email
    Given 3 users exist
    When I try to update one user Id 9 with duplicate name "jake" or email "kate@email.com"
    Then the API should return appropriate error
    And the database should remain unchanged

#  ########################################
#  # PROFILE APIs
#  ########################################

  Scenario: Get all profiles
    Given multiple profiles exist
    When I fetch all profiles via the API
    Then the API response should return all profiles
    And the database should match the response

  Scenario: Get profile by profile ID
    Given a profile exists with profile ID 8
    When I fetch the profile via the API using profile ID
    Then the API response of profile should match the database record

  Scenario: Update profile and validate DB
    Given a profile exists for user ID 8
    When I update the profile bio to "Hi I'm jake"
    Then the API response should reflect updated bio
    And the database should reflect updated bio

#  ########################################
#  # ORDER APIs
#  ########################################

  Scenario: Get all orders
    Given multiple orders exist
    When I fetch all orders via the API
    Then the API response should return all orders
    And the database should match the response

  Scenario: Get order by order ID
    Given an order exists with ID 11
    When I fetch the order via the API
    Then the API response of order should match the database record

  Scenario: Update order and validate DB
    Given an order exists with ID 11
    When I update the order with item "Mobile" and price 42000
    Then the API response should reflect updated order
    And the database should reflect updated order

#  ########################################
#  # DELETE OPERATIONS
#  ########################################

  Scenario: Delete profile by profile ID
    Given a profile exists with profile ID 10
    When I delete the profile using profile ID via API
    Then the profile should not exist in the database

  Scenario: Delete orders by order ID
    Given an order exists with ID 11
    When I delete the order via API
    Then the order should not exist in the database

  Scenario: Delete user by name
    Given a user exists with name "jake"
    When I delete the user using name via API
    Then the user should not exist in the database

#  ########################################
#  # CASCADE VALIDATION (CRITICAL)
#  ########################################

  Scenario: Deleting user should cascade delete profile and orders
    Given a user exists with ID 11 and with profile and orders
    When I delete the user via the API
    Then the user should not exist in the database
    And the profile should not exist in the database
    And the orders should not exist in the database

#  ########################################
#  # NEGATIVE CASES
#  ########################################

  Scenario: Fail to create profile for non-existing user
    Given no user exists with ID 9999
    When I try to create a profile
    Then the API response should return status code 409

  Scenario: Fail to create order for non-existing user
    Given no user exists with ID 9999
    When I try to create an order
    Then the API response should return status code 404

  Scenario: Fail to fetch non-existing resources
    When I fetch user/profile/order with invalid IDs
    Then the API should return 404 responses

#  ########################################
#  # CONSISTENCY VALIDATION
#  ########################################

  Scenario: Cross validate API and DB consistency
    Given a user exists with ID 11 and with profile and orders
    When I fetch user, profile, and orders via APIs
    Then all responses should match database records

#  ########################################
#  # EMPTY DATA EDGE CASES
#  ########################################

  Scenario: Handle empty database responses
    Given no users, profiles, or orders exist
    When I fetch all users, profiles, and orders
    Then the API should return appropriate responses or errors