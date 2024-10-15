import pandas as pd

def process_data(df):
    # merge remote and in
    df['Status'] = df['Status'].replace('Remote', 'In')
    # drop useless attributes
    df = df.drop(["Status ID", "User ID","Details","Groups","Comment","Application","Changed By Admin","Automatic"], axis=1)

    # Only look at clock in and out information
    df_filtered = df[df['Status'].isin(['In', 'Out'])].copy()
    # Formatting the type of attribute
    df_filtered['Created At'] = pd.to_datetime(df_filtered['Created At'], format='%d %B %Y %I:%M %p')
    df_filtered['Date'] = df_filtered['Created At'].dt.date
    
    # aggregate by user and date so that duplicate entries in a day can be handled
    # only keep the earliest clock in and the latest clock out
    df_grouped = df_filtered.groupby(['Name', 'Date']).agg(
        Clock_In=('Created At', lambda x: x[df_filtered.loc[x.index, 'Status'] == 'In'].min()),
        Clock_Out=('Created At', lambda x: x[df_filtered.loc[x.index, 'Status'] == 'Out'].max())
    ).reset_index()
    df_grouped.rename(columns={'Clock_In': 'Clock In', 'Clock_Out': 'Clock Out'}, inplace=True)

    # create day of the week column
    df_grouped['Day'] = pd.to_datetime(df_grouped['Date']).dt.strftime('%a')

    # drop na to avoid Teams synchronization glitches
    df_grouped.dropna(subset=['Clock In', 'Clock Out'], inplace=True)
    # format time
    df_grouped['Clock In'] = df_grouped['Clock In'].dt.strftime('%H:%M')
    df_grouped['Clock Out'] = df_grouped['Clock Out'].dt.strftime('%H:%M')

    df_grouped['Hours'] = (
        pd.to_datetime(df_grouped['Clock Out'], format='%H:%M') - pd.to_datetime(df_grouped['Clock In'], format='%H:%M')
    ).dt.total_seconds() / 3600

    df_final = df_grouped[['Name', 'Day', 'Date', 'Clock In', 'Clock Out', 'Hours']]
    df_final['Hours'] = df_final['Hours'].round(2)

    # create blank lines in between users for better visual
    rows_with_blank = []

    previous_name = None
    for index, row in df_final.iterrows():
        # If the name has changed, insert a blank row
        if previous_name and previous_name != row['Name']:
            # Append a blank row
            rows_with_blank.append(pd.Series([None] * len(df_final.columns), index=df_final.columns))
        
        # Append row data
        rows_with_blank.append(row)
        previous_name = row['Name']

    # Convert the list of rows back into a DataFrame
    df_with_blank = pd.DataFrame(rows_with_blank)

    return df_with_blank