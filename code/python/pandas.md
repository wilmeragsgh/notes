---
description: Frequently used code for pandas related code snippets
---

# Pandas

**plot columns**

```python
df.plot(figsize=(20,10))
```

**fill na**

```python
dt.fillna(0)
```

**Reading data from Postgresql**

```python
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("postgresql://user@localhost:5432/mydb")
df = pd.read_sql_query("select * from table", con=engine)
```

**Add rows**

```python
dt.append({"col1":[1,2,3], "coln":[4,5,6]})
```

**pivoting dataframe**

```python
df.pivot(columns="col_with_columns",values="col_with_values")
```

**getting index of max/min values**

```python
df['column'].idxmax()
```

**Count instances of values in column**

```python
df['target'].value_counts().sort_values(ascending=False)
```

**Filtering by column's value len**

```python
df[df['itemsets'].map(len) > 2]
```

**Iterate by rows**

```python
for index, row in df.iterrows():
    print(row['c1'], row['c2'])
```

**Subsetting columns**

```python
df[['col1', 'col2']]
```

**Parse datetimes**

```python
# errors = ['coerce','raise','ignore'] # default: 'raise'
df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d')
```

**Group by dates**

```python
df[df.date.dt.day == 8] #(or hour or minute)
```

**Plot evolution over time**

```python
%matplotlib inline 
import matplotlib.pyplot as plt
fig=plt.figure(figsize=(18, 13), dpi= 80, facecolor='w', edgecolor='k')

ax = plt.gca()
hist_dt[hist_dt["target_community"]==0].groupby([hist_dt.created_at.dt.day,hist_dt.created_at.dt.hour]).size().plot(ax=ax)
# if multiple samples: hist_dt[hist_dt["target_community"]==1].groupby([hist_dt.created_at.dt.day,hist_dt.created_at.dt.hour]).size().plot(ax=ax)
# if not the subsetting part could be removed
plt.xlabel('Dia,Hora de publicación')
plt.ylabel('Cantidad de tweets')
```

**New column A based on column B**

```python
df['Discounted_Price'] = df.apply(lambda row: row.Cost - 
                                  (row.Cost * 0.1), axis = 1)
#if row.property == 1 else None # for conditional setting
```

**To select rows whose column value equals a scalar, some\_value, use ==:**

```python
df.loc[df['column_name'] == some_value]
```

**To select rows whose column value is in an iterable, some\_values, use isin:**

```python
df.loc[df['column_name'].isin(some_values)]
```

**To select  rows whose column value is in another column array**

```python
df.apply(lambda x: x['Responsibility Type'] in x['Roles'], axis=1)
```

**Combine multiple conditions with &:**

```python
df.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]
```

**Note the parentheses. Due to Python's operator precedence rules, & binds more tightly than &lt;= and &gt;=. Thus, the parentheses in the last example are necessary. Without the parentheses**

```python
df['column_name'] >= A & df['column_name'] <= B
```

is parsed as

```python
df['column_name'] >= (A & df['column_name']) <= B
```

**To select rows whose column value does not equal some\_value, use !=:**

```python
df.loc[df['column_name'] != some_value]
```

**To select rows whose value is not in some\_values**

```python
df.loc[~df['column_name'].isin(some_values)]
```

**Improve query efficiency by setting an index**

```python
df = df.set_index(['colname'])
```

**Remove duplicates** (distinct)

```python
df.drop_duplicates()# subset=["col1", "col2"] use only those columns for distinction
```

**Check if a field exists**

```python
df[df['column'].isnull()]
#or
df[df['column'].notnull()]
```

**Replacing column values**

```python
w['female'] = w['female'].map({'female': 1, 'male': 0})
#or
dt.loc[dt['ccLeadtime'] == -1, 'ccLeadtime'] = 0
```

**One-hot encoding**

```python
dfDummies = pd.get_dummies(df['categorical'], prefix = 'category')
df = pd.concat([df, dfDummies], axis=1)
```

**Rename column**

```python
df = df.rename(columns={"A": "a", "B": "c"})
```

**Remove column from list**

```python
df.drop(['pop'], axis=1)
```

**Join dataframes**

```python
pd.merge(df1,df2,on='key')
```

**Iterate by groups**

```python
grouped = df.groupby('A')
for name, group in grouped:
```

**Group data by year**

```python
data.groupby(data.date.dt.year)
```

**Count unique by group**

```python
df.groupby('location')['user'].nunique()
```

**Get normalized values from groupby count**

```python
df2 = df.groupby(['subset_product', 'subset_close']).size().reset_index(name='prod_count')
a = df2.groupby('subset_product')['prod_count'].transform('sum')
df2['prod_count'] = df2['prod_count'].div(a)
```

**Generate csv from dataframe**

```python
df.to_csv('filename.csv',index=False)
```

**Sum to date column**

```python
df['date'] = df['created'] + pd.to_timedelta(7, unit='d')
```

**Replace character in column**

```python
df["column"] = df["column"].str.replace('foo', 'bar')
```

## References

* [PDF version](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
* [conference-school-notes/2019-12-NeuRIPS at master · RobertTLange/conference-school-notes · GitHub](https://github.com/RobertTLange/conference-school-notes/tree/master/2019-12-NeuRIPS)

