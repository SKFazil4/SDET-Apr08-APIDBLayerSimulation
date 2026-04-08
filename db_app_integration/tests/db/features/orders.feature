Feature: Orders Table DB operations

  Scenario: Create an order successfully for a user
    Given a user exists with ID 1
    And I have an order payload with item_name "Laptop" and price 1200
    When I insert the order into the orders table
    Then the order should exist with the correct item_name, price, and user_id

  Scenario: Fail to create order for non-existing user
    Given no user exists with ID 9999
    When I try to insert an order with user_id 9999
    Then the database should raise a foreign key constraint error

  Scenario: Retrieve all orders for a user
    Given multiple orders exist for user ID 1
    When I query the orders table for user ID 1
    Then all orders should be returned correctly