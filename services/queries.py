QUERIES = {
    "funnel_by_category": """
        SELECT category_code, SUM(view) AS views, SUM(cart) AS carts, SUM(purchase) AS purchases
        FROM conversion_categorias
        GROUP BY category_code
    """,
}
