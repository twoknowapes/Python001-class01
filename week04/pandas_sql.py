import pandas as pd

sql = "select * from data;"

df_table = pd.read_sql_query(sql)

# 1. SELECT * FROM data;
df = df_table
print(df)

# 2. SELECT * FROM data LIMIT 10;
df = df_table.head(10)
print(df)

# 3. SELECT id FROM data;
df = df_table['id']
print(df)

# 4. SELECT COUNT(id) FROM data;
df = df_table['id'].size
print(df)

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
df = df_table[(df_table['id'] < 1000) & (df_table['age'] > 30)]
print(df)

sql1 = "select * from table1;"
sql2 = "select * from table2;"

df_table1 = pd.read_sql_query(sql1)
df_table2 = pd.read_sql_query(sql2)

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
df = df_table1.groupby(by='id', as_index=False).agg(
    {'order_id': pd.Series.nunique})
print(df)

# #7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
df = pd.merge(df_table1, df_table2, on='id')
print(df)

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
df = pd.concat([df_table1, df_table2], ignore_index=True).drop_duplicates()
print(df)

# 9. DELETE FROM table1 WHERE id=10;
df = df_table1.drop(df_table1[df_table1.id == 10].index)
print(df)

# 10. ALTER TABLE table1 DROP COLUMN column_name;
df = df_table1.drop(['column_name'], axis=1)
print(df)