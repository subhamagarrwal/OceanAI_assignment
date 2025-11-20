Product Specifications: E-Shop Checkout System

1. Discount Codes

The system supports specific promotional codes.

Rule: The code SAVE15 applies a 15% discount to the subtotal of items in the cart.

Rule: Any other code entered is considered invalid and should display an error message ("Invalid Code").

Rule: Discounts apply only to the item subtotal, not to shipping costs.

2. Shipping Logic

Users can select between two shipping methods:

Standard Shipping: This method is free ($0.00).

Express Shipping: This method costs a flat rate of $10.00.

Rule: Changing the shipping method must immediately update the "Total" price displayed.

Rule: Standard shipping is selected by default when the page loads.

3. Cart Functionality

The "Add to Cart" buttons increase the "Items in Cart" count by 1.

The Total Price is calculated as: (Sum of Item Prices * (1 - Discount Rate)) + Shipping Cost.

Users cannot complete a purchase (click Pay Now) if the cart total is $0.00 (i.e., the cart is empty).

4. Payment Methods

Supported payment types:

Credit Card (Default selection)

PayPal

No actual payment processing occurs; this is a frontend simulation.