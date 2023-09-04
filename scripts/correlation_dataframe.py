import pandas as pd 

#only about Spearman correlation values 
df = pd.read_csv('/nfs/home/students/a.schuhe/scripts/splicingREMs/output_CorrelationShuffle/df_HM_SegSpearman.csv')
correlation_df = df[['Event','Significant Correlation Values Spearman','Class', 'Event type', 'Iteration']]
unlist_correlation_df = []

# Iterate through the original dataframe
for index, row in correlation_df.iterrows():
    value = row['Significant Correlation Values Spearman']
    value = value.rstrip().split(", ")
    value[0] = value[0].replace("[","")
    value[-1] = value[-1].replace("]","")
    for sub_value in value:   
        data = {'Event': row['Event'],
                'Significant Correlation Values Spearman': sub_value, 
                'Class': row['Class'],
                'Event type': row['Event type'],
                'Iteration': row['Iteration']}
        unlist_correlation_df.append(data) 

new_correlation_df = pd.DataFrame(unlist_correlation_df)
new_correlation_df.to_csv('/nfs/home/students/a.schuhe/scripts/splicingREMs/output_CorrelationShuffle/new_correlation_df.csv', index=False)

    
    
    
