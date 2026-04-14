Feature: Order Table DB operations

  Scenario: Create order successfully
    Given a user exists with ID 1
    When I insert an order with user_id 1 item_name "Laptop" and price 1000
    Then the order should exist in the database with correct details

  Scenario: Fail to create order for non-existing user
    Given no user exists with ID 9999
    When I try to insert an order with user_id 9999
    Then the database should raise a foreign key constraint error

  Scenario: Retrieve all orders
    Given multiple orders exist
    When I query all orders
    Then all orders should be returned

  Scenario: Retrieve orders by user ID
    Given multiple orders exist for user ID 1
    When I query orders by user ID 1
    Then all returned orders should belong to user ID 1

  Scenario: Retrieve order by order ID
    Given an order exists with ID 1
    When I query the order by ID 1
    Then the returned order should match stored values

  Scenario: Update order details
    Given an order exists with ID 1
    When I update the order item_name to "Tablet" and price to 500
    Then the database should reflect updated order details

  Scenario: Delete orders by user ID
    Given multiple orders exist for user ID 1
    When I delete orders using user ID 1
    Then no orders should exist for that user

  Scenario: Delete order by order ID
    Given an order exists with ID 1
    When I delete the order using order ID 1
    Then the order should not exist in the database