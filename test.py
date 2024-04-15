# import pandas as pd

# # Read the CSV file into a DataFrame
# df = pd.read_csv('output1.csv')

# # Get unique values of the 'symptom' column
# unique_symptoms = df['symptom'].unique()

# # Create a new DataFrame with unique symptoms
# unique_symptoms_df = pd.DataFrame({'symptom': unique_symptoms})

# # Write the unique symptoms DataFrame to a CSV file
# unique_symptoms_df.to_csv('unique_symptoms.csv', index=False)

# print("Unique symptoms have been stored in 'unique_symptoms.csv'.")


import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('unique_symptoms.csv')

# Get unique values of the 'symptom' column
unique_symptoms = df['symptom'].unique()

# Reshape the unique symptoms into a DataFrame with five symptoms per row
symptoms_chunks = [unique_symptoms[i:i+5] for i in range(0, len(unique_symptoms), 5)]
unique_symptoms_df = pd.DataFrame(symptoms_chunks)

# Write the unique symptoms DataFrame to a CSV file
unique_symptoms_df.to_csv('unique_symptoms1.csv', index=False)

print("Unique symptoms have been stored in 'unique_symptoms.csv' with five symptoms per row.")
