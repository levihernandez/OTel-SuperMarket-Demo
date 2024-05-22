## Auto Instrumentation Sent to Datadog



* OTel auto instrumentation seems to capture high level resources

![](../img/otel-auto-01.png)

* Two spans were auto discovered (connect + SELECT marketdb)
* The transaction query from the API is missing (might need additional configs or libraries?):
  
```sql
SELECT products.id,
  products.name,
  products.category,
  products.quantity,
  products.price,
  products.supplier
FROM products
  WHERE products.supplier = ?
```

![](../img/otel-auto-02.png)
