from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import joblib
import numpy as np

# # Load the dataset
data = pd.read_csv('symptoms_modified_dataset.csv')

# Get unique symptoms
unique_symptoms = sorted(set(symptom for sublist in data["Symptoms"].str.split(", ") for symptom in sublist))

# Initialize an empty matrix
co_occurrence_matrix = pd.DataFrame(0, index=unique_symptoms, columns=unique_symptoms)

# Iterate through each row of the dataset
for _, row in data.iterrows():
    symptoms = row["Symptoms"].split(", ")
    for symptom1 in symptoms:
        for symptom2 in symptoms:
            co_occurrence_matrix.at[symptom1, symptom2] += 1

# Print the co-occurrence matrix
# print("Symptom Co-occurrence Matrix:")
# print(co_occurrence_matrix)

symptom_counts = co_occurrence_matrix.sum(axis=1)

# Normalize the co-occurrence matrix to obtain probabilities
symptom_co_occurrence_probabilities = co_occurrence_matrix.div(symptom_counts, axis=0)

# Print the normalized co-occurrence matrix (probabilities)
# print(symptom_co_occurrence_probabilities)



def suggest_symptoms(selected_symptoms, top_n=10):
        # Initialize an empty list to store suggested symptoms
        suggested_symptoms = []

        # Convert selected symptoms to lowercase
        selected_symptoms = [symptom.strip().lower() for s in selected_symptoms for symptom in s.split(", ")]

        # Check if all selected symptoms exist in the index of the co-occurrence matrix
        valid_selected_symptoms = [symptom for symptom in selected_symptoms if symptom in co_occurrence_matrix.index.str.lower()]

        # Compute the similarity scores only for valid selected symptoms
        if valid_selected_symptoms:
            similarity_scores = cosine_similarity([co_occurrence_matrix.loc[symptom] for symptom in valid_selected_symptoms],
                                                  [co_occurrence_matrix.loc[symptom] for symptom in co_occurrence_matrix.index])

            # Aggregate the similarity scores for all selected symptoms
            aggregated_scores = np.sum(similarity_scores, axis=0)

            # Sort the symptoms based on the aggregated scores in descending order
            sorted_indices = np.argsort(aggregated_scores)[::-1]

            # Extract the top N suggested symptoms
            for index in sorted_indices:
                symptom = co_occurrence_matrix.index[index]
                if symptom.lower() not in [s.lower() for s in valid_selected_symptoms]:
                    suggested_symptoms.append(symptom)
                    if len(suggested_symptoms) == top_n:
                        break
        else:
            print("No valid selected symptoms found.")

        return suggested_symptoms

    # Save the suggest_symptoms function using joblib
# joblib.dump(suggest_symptoms, 'suggest_symptoms_function.joblib')
# print("MODEL SAVED..")