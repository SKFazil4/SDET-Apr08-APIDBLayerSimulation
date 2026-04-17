Feature: Order API

  Scenario: Create order successfully
    Given a user exists with ID 1
    And I have an order payload with item_name "Laptop" and price 52500
    When I send POST request to "/orders"
    Then the response status code should be 200
    And the response should contain item_name "Laptop" and price 52500
    And the response should contain user_id 1

  Scenario: Fail to create order for non-existing user
    Given no user exists with ID 9999
    And I have an order payload with item_name "Mouse" and price 590
    When I send POST request to "/orders"
    Then the response status code should be 404
    And the response message should be "User does not exists"

  Scenario: Get all orders successfully
    Given multiple orders exist
    When I send GET request to "/orders"
    Then the response status code should be 200
    And the response should be a list of orders

  Scenario: Get orders by user ID successfully
    Given multiple orders exist for user ID 1
    When I send GET request to "/orders/userid/1"
    Then the response status code should be 200
    And all returned orders should contain user_id 1

  Scenario: Fail to get orders for non-existing user
    When I send GET request to "/orders/userid/9999"
    Then the response status code should be 404
    And the response message should be "User not exists"

  Scenario: Get order by order ID successfully
    Given an order exists with ID 1
    When I send GET request to "/orders/orderid/1"
    Then the response status code should be 200
    And the response should contain order ID 1

  Scenario: Update order successfully
    Given an order exists with ID 1
    When I send PUT request to "/orders/id/1" with item_name "Tablet" and price 500
    Then the response status code should be 200
    And the response should contain updated item_name "Tablet" and price 500

  Scenario: Fail to update non-existing order
    When I send PUT request to "/orders/id/9999" with item_name "Tablet" and price 500
    Then the response status code should be 404
    And the response message should be "Order does not exists"

  Scenario: Delete orders by user ID
    Given multiple orders exist for user ID 1
    When I send DELETE request to "/orders/userid/1"
    Then the response status code should be 200

  Scenario: Delete order by order ID
    Given an order exists with ID 1
    When I send DELETE request to "/orders/orderid/1"
    Then the response status code should be 200

  Scenario: Fail to delete non-existing order
    When I send DELETE request to "/orders/orderid/9999"
    Then the response status code should be 404