Feature: Order API

  Scenario: Create order successfully for user
    Given a user exists with ID 1
    And I have an order payload with item_name "Laptop" and price 1200
    When I send POST request to "/orders"
    Then the response status code should be 200
    And the response should contain item_name "Laptop" and price 1200

  Scenario: Fail to create order for non-existing user
    Given no user exists with ID 9999
    And I have an order payload with item_name "Mouse" and price 50
    When I send POST request to "/orders"
    Then the response status code should be 404
    And the response message should be "User profile does not exists"

  Scenario: Get order by user ID successfully
    Given an order exists with user ID 1
    When I send GET request to "/orders/1"
    Then the response status code should be 200
    And the response should contain user ID 1