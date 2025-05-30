import polars as pl
import re

def fill_oil_pl(df, column_name):
    df = df.sort("date")
    forward_filled = df[column_name].fill_null(strategy="forward")
    backward_filled = df[column_name].fill_null(strategy="backward")
    avg = (forward_filled + backward_filled) / 2
    avg = avg.fill_null(strategy="backward").fill_null(strategy="forward")
    return df.with_columns(avg.alias(column_name))

def remove_plusmin_pl(df):
    new_col_names = {}
    for col in df.columns:
        new_name = col.replace("+","_plus").replace("-","_min")
        new_name = re.sub(r"[^\w]", "_", new_name)

        # if new_name in new_col_names.values():
        #     i = 1
        #     while f"{new_name}_{i}" in new_col_names.values():
        #         i += 1
        #     new_name = f"{new_name}_{i}"
        orig = new_name
        i = 1
        while new_name in new_col_names.values():
            new_name = f"{orig}_{i}"
            i += 1
        new_col_names[col] = new_name
    return(df.rename(new_col_names))

def lag_cols_pl(df, periods, cols_to_lag):
    df = (df.sort(["store_nbr","family","date"])
          .with_columns(
              [
                  pl.col(col).shift(p).over(["store_nbr", "family"]).fill_null(strategy="backward").alias(f"{col}_lag{p}")
                  for col in cols_to_lag
                  for p in periods
              ]
          )
    )
    return df

def MA_pl(df, periods, cols):
    expressions = []
    for col in cols:
        for p in periods:
            avg_expr = pl.col(col).rolling_mean(p).over(["store_nbr", "family"]).fill_null(strategy="backward").alias(f"{col}_avg_t{p}")
            std_expr = pl.col(col).rolling_std(p).over(["store_nbr", "family"]).fill_null(strategy="backward").alias(f"{col}_std_t{p}")

            expressions.extend([avg_expr, std_expr])
    return(df.sort(["store_nbr", "family", "date"]).with_columns(expressions))
    