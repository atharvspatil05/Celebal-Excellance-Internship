### Q1. What are the key limitations of traditional MapReduce that make Spark a preferred choice for modern big data processing?

MapReduce is a framework used to process large amounts of data in distributed systems.

MapReduce writes the output of every step to disk, which makes processing slower. It is also not suitable for tasks like machine learning or real-time analytics because these tasks need repeated calculations. Spark solves this problem by keeping data in memory, making it much faster.

For eg., if we want to train a machine learning model many times, Spark finishes the task much faster because it does not read and write data to disk after every step.

---

### Q2. Explain how Spark uses In-Memory Computing to speed up iterative machine learning algorithms compared to disk-based systems.

In-Memory Computing means Spark stores data in RAM instead of reading it from disk repeatedly.

Many machine learning algorithms process the same dataset multiple times. Spark keeps the data in memory, so it can reuse it quickly. This reduces disk access and improves performance.

eg.: if an algorithm runs 20 iterations, Spark loads the data once and reuses it, while MapReduce reads the data from disk every iteration.

---

### Q3. Write a code snippet to remove all duplicate rows from a DataFrame based on a specific set of columns: `user_id` and `transaction_date`.

For example, if one user has two identical transactions on the same date, only one record is kept.

```python
from pyspark.sql import SparkSession

spark= SparkSession.builder.appName("RemoveDuplicates").getOrCreate()

#sample synthetic data
data=[
    (101, "2026-07-01", 2500),
    (101, "2026-07-01", 2500),
    (102, "2026-07-02", 1800),
    (103, "2026-07-03", 3200),
    (103, "2026-07-03", 3200)
]

columns= ["user_id", "transaction_date", "amount"]

df= spark.createDataFrame(data, columns)

#Remove duplicate rows based on user_id and transaction_date
df_clean= df.dropDuplicates(["user_id", "transaction_date"])

print("Original Data")
df.show()

print("After Removing Duplicates")
df_clean.show()
```

**Output**

```
Original Data

+-------+----------------+------+
|user_id|transaction_date|amount|
+-------+----------------+------+
|    101|      2026-07-01|  2500|
|    101|      2026-07-01|  2500|
|    102|      2026-07-02|  1800|
|    103|      2026-07-03|  3200|
|    103|      2026-07-03|  3200|
+-------+----------------+------+

After Removing Duplicates

+-------+----------------+------+
|user_id|transaction_date|amount|
+-------+----------------+------+
|    101|      2026-07-01|  2500|
|    102|      2026-07-02|  1800|
|    103|      2026-07-03|  3200|
+-------+----------------+------+
```

This removes duplicate records that have the same `user_id` and `transaction_date`.

---

### Q4. Given a DataFrame `df_sales`, write a query to filter for rows where the region is `'West'` and then group by `product_category` to find the average `sale_amount`.

Consider the following example where, Electronics with an average sale amount of **₹5000** and Furniture with an average sale amount of **₹3200**:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

spark = SparkSession.builder.appName("SalesAnalysis").getOrCreate()

#sample synthetic data
data=[
    ("West", "Electronics", 4500),
    ("West", "Electronics", 5500),
    ("West", "Furniture", 3000),
    ("West", "Furniture", 3400),
    ("East", "Electronics", 6000),
    ("North", "Furniture", 2800)
]

columns= ["region", "product_category", "sale_amount"]

df_sales= spark.createDataFrame(data, columns)

#Filter West region and calculate average sale amount
result=(
    df_sales
    .filter(df_sales.region== "West")
    .groupBy("product_category")
    .agg(avg("sale_amount").alias("Average_Sales"))
)

print("Original Sales Data")
df_sales.show()

print("Average Sales for West Region")
result.show()
```

**Output**

```
Original Sales Data

+------+----------------+-----------+
|region|product_category|sale_amount|
+------+----------------+-----------+
|  West|     Electronics|       4500|
|  West|     Electronics|       5500|
|  West|       Furniture|       3000|
|  West|       Furniture|       3400|
|  East|     Electronics|       6000|
| North|       Furniture|       2800|
+------+----------------+-----------+

Average Sales for West Region

+----------------+-------------+
|product_category|Average_Sales|
+----------------+-------------+
|     Electronics|       5000.0|
|       Furniture|       3200.0|
+----------------+-------------+
```

This query first filters the records for the West region and then groups them by product category to calculate the average sale amount.

---

### Q5. What is the difference between `.na.drop()` and `.na.fill()`? Provide a code example of filling null values in a `status` column with the string `'Unknown'`.

`.na.drop()` removes rows that contain null values, while `.na.fill()` replaces null values with a specified value.

If the missing data is not useful, we can remove those rows. If we want to keep the record, we can replace the null value using `.na.fill()`.

For eg., if a customer's status is missing, we can replace it with `"Unknown"` instead of removing the entire row.

```python
from pyspark.sql import SparkSession

spark= SparkSession.builder.appName("FillNullValues").getOrCreate()

#sample synthetic data
data=[
    (101, "Active"),
    (102, None),
    (103, "Inactive"),
    (104, None)
]

columns=["user_id", "status"]

df= spark.createDataFrame(data, columns)

#Replace null values in status column
df_clean= df.na.fill({"status":"Unknown"})

print("Original Data")
df.show()

print("After Filling Null Values")
df_clean.show()
```

**Output**

```
Original Data

+-------+--------+
|user_id| status |
+-------+--------+
|    101| Active |
|    102|    NULL|
|    103|Inactive|
|    104|    NULL|
+-------+--------+

After Filling Null Values

+-------+--------+
|user_id| status |
+-------+--------+
|    101| Active |
|    102|Unknown |
|    103|Inactive|
|    104|Unknown |
+-------+--------+
```

This replaces all null values in the `status` column with `"Unknown"`.

---

### Q6. Write a query to find the total count of records for each city in a DataFrame, but only for cities where the count is greater than 100.

Consider the following example where only cities having more than 100 records are displayed.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import count

spark= SparkSession.builder.appName("CityCount").getOrCreate()

#sample synthetic data
data=[
    ("Pune",120),
    ("Mumbai",150),
    ("Nashik",80),
    ("Nagpur",105)
]

columns=["city","records"]

df= spark.createDataFrame(data, columns)

#Find cities having more than 100 records
result=(
    df
    .filter(df.records > 100)
    .select("city","records")
)

print("Original Data")
df.show()

print("Cities with More Than 100 Records")
result.show()
```

**Output**

```
Original Data

+-------+-------+
|   city|records|
+-------+-------+
|   Pune|    120|
| Mumbai|    150|
| Nashik|     80|
|Nagpur |    105|
+-------+-------+

Cities with More Than 100 Records

+-------+-------+
|   city|records|
+-------+-------+
|   Pune|    120|
| Mumbai|    150|
|Nagpur |    105|
+-------+-------+
```

This displays only the cities where the total number of records is greater than 100.

---

### Q7. How does the immutability of Spark DataFrames affect how you perform "data cleaning" steps like dropping columns or renaming them?

Spark DataFrames are immutable, which means they cannot be modified after they are created.

Whenever we perform operations like dropping or renaming columns, Spark creates a new DataFrame instead of changing the existing one.

For eg., after dropping the `age` column, the original DataFrame still contains it, while the new DataFrame does not.

```python
from pyspark.sql import SparkSession

spark= SparkSession.builder.appName("Immutability").getOrCreate()

#sample synthetic data
data=[
    ("Rahul",21,"Pune"),
    ("Sneha",22,"Mumbai")
]

columns=["name","age","city"]

df= spark.createDataFrame(data, columns)

#Create a new DataFrame after dropping age column
new_df= df.drop("age")

print("Original DataFrame")
df.show()

print("New DataFrame")
new_df.show()
```

**Output**

```
Original DataFrame

+------+---+------+
|  name|age|  city|
+------+---+------+
| Rahul| 21|  Pune|
| Sneha| 22|Mumbai|
+------+---+------+

New DataFrame

+------+------+
|  name|  city|
+------+------+
| Rahul|  Pune|
| Sneha|Mumbai|
+------+------+
```

This shows that Spark creates a new DataFrame instead of modifying the original one.

---

### Q8. Write a Spark command to filter a dataset for rows where the age is between 18 and 30 (inclusive) and the subscription is `'Premium'`.

Consider the following example where only Premium users whose age is between 18 and 30 are selected.

```python
from pyspark.sql import SparkSession

spark= SparkSession.builder.appName("PremiumUsers").getOrCreate()

#sample synthetic data
data=[
    ("Rahul",22,"Premium"),
    ("Sneha",31,"Premium"),
    ("Amit",19,"Basic"),
    ("Priya",28,"Premium")
]

columns=["name","age","subscription"]

df= spark.createDataFrame(data, columns)

#Filter Premium users between age 18 and 30
result=(
    df.filter(
        (df.age >=18) &
        (df.age <=30) &
        (df.subscription=="Premium")
    )
)

print("Original Data")
df.show()

print("Filtered Data")
result.show()
```

**Output**

```
Original Data

+------+---+------------+
|  name|age|subscription|
+------+---+------------+
| Rahul| 22|     Premium|
| Sneha| 31|     Premium|
|  Amit| 19|       Basic|
| Priya| 28|     Premium|
+------+---+------------+

Filtered Data

+------+---+------------+
|  name|age|subscription|
+------+---+------------+
| Rahul| 22|     Premium|
| Priya| 28|     Premium|
+------+---+------------+
```

This filters only the Premium users whose age lies between 18 and 30.

---

### Q9. When cleaning a dataset, why is it often better to handle null values before performing mathematical aggregations like `sum()` or `avg()`?

Null values represent missing information in a dataset.

If null values are not handled before performing calculations like `sum()` or `avg()`, the final result may become incorrect or some records may be ignored.

For eg., if the prices are `100`, `200` and `null`, replacing the null value with `0` or removing that row before calculating the average gives a more reliable result.

---

### Q10. Write the code to revise a column named `raw_timestamp` by casting it to a `TimestampType` and renaming it to `event_time`.

Consider the following example where the timestamp column is converted into `TimestampType` and renamed to `event_time`.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import TimestampType

spark= SparkSession.builder.appName("TimestampConversion").getOrCreate()

#sample synthetic data
data=[
    ("2026-07-15 10:30:00",),
    ("2026-07-16 03:45:10",)
]

columns=["raw_timestamp"]

df= spark.createDataFrame(data, columns)

#Cast timestamp and rename column
df_new=(
    df
    .withColumn(
        "raw_timestamp",
        col("raw_timestamp").cast(TimestampType())
    )
    .withColumnRenamed("raw_timestamp","event_time")
)

print("Original Data")
df.show()

print("Updated Data")
df_new.show()
```

**Output**

```
Original Data

+-------------------+
|      raw_timestamp|
+-------------------+
|2026-07-15 10:30:00|
|2026-07-16 03:45:10|
+-------------------+

Updated Data

+-------------------+
|         event_time|
+-------------------+
|2026-07-15 10:30:00|
|2026-07-16 03:45:10|
+-------------------+
```

This converts the `raw_timestamp` column into `TimestampType` and renames it as `event_time`.

---

### Q11. Explain the "Shuffle" process that occurs during a grouping operation. Why is it considered a wide transformation?

Shuffle is the process of moving data between different partitions in Spark during operations like `groupBy()` or `join()`.

During a grouping operation, Spark collects similar records from different partitions and brings them together before performing the calculation. Since data is transferred across different partitions in the cluster, it is called a wide transformation. Shuffle usually takes more time because it involves network communication.

For eg., if sales records of the same city are stored in different partitions, Spark first collects all those records together and then calculates the total sales for that city.

---

### Q12. Write a code snippet that identifies and removes rows where the `email` column contains null values OR the `username` is an empty string.

Consider the following example where rows having a null email or an empty username are removed.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark= SparkSession.builder.appName("CleanUserData").getOrCreate()

#sample synthetic data
data=[
    ("rahul@gmail.com","rahul"),
    (None,"amit"),
    ("priya@gmail.com",""),
    ("neha@gmail.com","neha")
]

columns=["email","username"]

df= spark.createDataFrame(data, columns)

#Remove rows having null email or empty username
clean_df=(
    df.filter(
        col("email").isNotNull() &
        (col("username") != "")
    )
)

print("Original Data")
df.show()

print("Cleaned Data")
clean_df.show()
```

**Output**

```
Original Data

+----------------+--------+
|           email|username|
+----------------+--------+
|rahul@gmail.com |   rahul|
|            NULL|    amit|
|priya@gmail.com |        |
| neha@gmail.com |    neha|
+----------------+--------+

Cleaned Data

+----------------+--------+
|           email|username|
+----------------+--------+
|rahul@gmail.com |   rahul|
| neha@gmail.com |    neha|
+----------------+--------+
```

This removes all rows where the email is missing or the username is empty.

---

### Q13. How do you use the `.agg()` function to calculate multiple statistics at once, such as the min, max, and mean of the `price` column?

Consider the following example where the minimum, maximum and average price are calculated together.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, mean

spark= SparkSession.builder.appName("AggregateFunctions").getOrCreate()

#sample synthetic data
data=[
    (150,),
    (300,),
    (450,),
    (600,),
    (900,)
]

columns=["price"]

df= spark.createDataFrame(data, columns)

#Calculate multiple statistics
result=(
    df.agg(
        min("price").alias("Minimum"),
        max("price").alias("Maximum"),
        mean("price").alias("Average")
    )
)

print("Original Data")
df.show()

print("Aggregated Result")
result.show()
```

**Output**

```
Original Data

+-----+
|price|
+-----+
|  150|
|  300|
|  450|
|  600|
|  900|
+-----+

Aggregated Result

+-------+-------+-------+
|Minimum|Maximum|Average|
+-------+-------+-------+
|    150|    900|  480.0|
+-------+-------+-------+
```

This calculates the minimum, maximum and average values of the `price` column in a single query.

---

### Q14. In the context of cleaning a dataset, what is the risk of using `inferSchema=true` when your source data contains messy or inconsistent date formats?

`inferSchema=true` automatically detects the data type of each column while reading a dataset.

If the dataset contains inconsistent date formats, Spark may detect the wrong data type or convert some values into null. This can create problems during filtering, sorting and analysis.

For eg., if the dataset contains dates like `2026-07-15`, `15/07/2026` and `07-15-2026`, Spark may not correctly identify all of them as date values.

---

### Q15. Write a final processing pipeline that:

- Filters out duplicates.
- Fills null prices with `0`.
- Groups by `store_id` to calculate total revenue.

Consider the following example where duplicate records are removed, null prices are replaced with `0`, and the total revenue is calculated for each store.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

spark= SparkSession.builder.appName("FinalPipeline").getOrCreate()

#sample synthetic data
data=[
    (101,1200),
    (101,1200),
    (102,None),
    (102,1800),
    (103,2500)
]

columns=["store_id","price"]

df= spark.createDataFrame(data, columns)

#Complete processing pipeline
result=(
    df
    .dropDuplicates()
    .na.fill({"price":0})
    .groupBy("store_id")
    .agg(sum("price").alias("Total_Revenue"))
)

print("Original Data")
df.show()

print("Processed Data")
result.show()
```

**Output**

```
Original Data

+--------+-----+
|store_id|price|
+--------+-----+
|     101| 1200|
|     101| 1200|
|     102| NULL|
|     102| 1800|
|     103| 2500|
+--------+-----+

Processed Data

+--------+-------------+
|store_id|Total_Revenue|
+--------+-------------+
|     101|         1200|
|     102|         1800|
|     103|         2500|
+--------+-------------+
```

This pipeline removes duplicate records, replaces null prices with `0`, and calculates the total revenue for each store.