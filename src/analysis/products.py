import pandas as pd


def calc_product_cancellation_rates(df: pd.DataFrame, min_quantity_percentile: float = 0.25) -> pd.DataFrame:
    canc_df = df[df['Invoice'].str.startswith('C', na=False)]
    canc_qnt = canc_df.groupby(['Description'])['Quantity'].sum().abs()

    sales_df = df[~df['Invoice'].str.startswith('C', na=False)]
    sales_qnt = sales_df.groupby(['Description'])['Quantity'].sum()

    product_df = sales_qnt.reset_index().merge(
        canc_qnt.reset_index(),
        on='Description',
        how='left'
    )
    product_df.columns = ['Description', 'Ordered', 'Cancelled']
    product_df['Cancelled'] = product_df['Cancelled'].fillna(0)
    product_df['Cancellation Rate'] = (product_df['Cancelled'] / product_df['Ordered'] * 100).round(2)

    threshold = product_df['Ordered'].quantile(min_quantity_percentile)

    product_df = product_df[product_df['Ordered'] >= threshold]

    product_df = product_df[product_df['Cancellation Rate'] < 100]
    return product_df.sort_values('Cancellation Rate', ascending=False).reset_index(drop=True)