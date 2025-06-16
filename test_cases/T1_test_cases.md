# Test Cases for T1 - E-Commerce Website Project Development

Okay, I'm ready to write some detailed test cases for the E-commerce Website Project Development, focusing on core e-commerce functionality. I'll assume we have some basic infrastructure in place (site loads, database is connected, etc.).

Here are two test cases that cover critical areas of the e-commerce functionality:

**Test Case 1:  Product Search Functionality - Exact Match**

*   **Title:** Verify Product Search Returns Expected Results for Exact Matches

*   **Description:** This test case validates the product search functionality by searching for a specific product name and verifying that the correct product is displayed in the search results. This ensures accurate information retrieval and a good user experience. This test is important as search functionality is a core component.

*   **Steps:**

    1.  **Pre-Condition:**
        *   The E-commerce website is accessible in a supported browser.
        *   A product with a known, unique name exists in the product catalog. For example, a product named "Ergonomic Office Chair - Model X1000".
        *   The user is not logged in to the website. (Test as a Guest User).
    2.  **Action:** Navigate to the homepage of the E-commerce website.
    3.  **Action:** Locate the search bar (usually at the top of the page).
    4.  **Action:** Enter the complete and exact product name, "Ergonomic Office Chair - Model X1000", into the search bar.
    5.  **Action:** Press the "Enter" key or click the search button.
    6.  **Action:** Observe the search results page.

*   **Expected Result:**

    1.  The search results page should load successfully.
    2.  The search results should display the product "Ergonomic Office Chair - Model X1000" as the primary result (ideally the first or only result).
    3.  The displayed product should include the correct product name ("Ergonomic Office Chair - Model X1000"), a relevant image, and a brief description matching the product in the catalog.
    4.  There should be no other irrelevant or unrelated products displayed in the search results. (Ideally, other related products are shown after the exact match, but that is outside of this test case's scope.)
    5.  If no match, the page should display a "No results found" message or a suggestion for similar products. It should not error out.

*   **Priority:** High (P1) - This is a core e-commerce function, and a broken search functionality severely impacts the user's ability to find and purchase products.
    **Test Case 2:  Add to Cart Functionality - Successfully Adding a Product**

*   **Title:** Verify Adding a Product to Cart Functionality

*   **Description:** This test case validates the "Add to Cart" functionality by adding a specific product to the cart and verifying that the product is successfully added and reflected in the cart summary. This confirms a fundamental aspect of the shopping process.

*   **Steps:**

    1.  **Pre-Condition:**
        *   The E-commerce website is accessible in a supported browser.
        *   A product with a known name and price exists in the product catalog (e.g., "Wireless Mouse - Silver Edition" priced at $25.00).
        *   The user is not logged in to the website. (Test as a Guest User).
        *   The product has available inventory.
    2.  **Action:** Navigate to the product page for the "Wireless Mouse - Silver Edition". This can be done by searching for it (using the previous test case!) or browsing the product catalog.
    3.  **Action:** Locate the "Add to Cart" button on the product page.
    4.  **Action:** Click the "Add to Cart" button.
    5.  **Action:** Observe the website's response.

*   **Expected Result:**

    1.  The website should provide visual feedback indicating that the product has been added to the cart. This could be a confirmation message (e.g., "Product added to cart!"), a change in the cart icon's appearance (e.g., a number indicating the number of items in the cart), or a mini-cart pop-up.
    2.  Navigate to the shopping cart (usually by clicking on a cart icon in the header).
    3.  The shopping cart page should load successfully.
    4.  The "Wireless Mouse - Silver Edition" should be listed in the shopping cart with the correct name, image (if available), quantity (defaulting to 1 unless the user specifies otherwise), and price ($25.00).
    5.  The subtotal should reflect the correct price of the added product.
    6.  If the inventory is at 0, the 'Add to Cart' button should be disabled.

*   **Priority:** High (P1) - This is another core e-commerce function. Without the ability to add items to the cart, users cannot make purchases.
These two test cases are a starting point. Further test cases would be required to test for more comprehensive coverage. For example: search with misspellings, partial search terms, different quantities, logged in users, various browser types, etc.