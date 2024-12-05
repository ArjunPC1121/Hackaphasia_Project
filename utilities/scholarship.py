import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def train():
    # Dummy data for scholarships and students
    scholarship_data = {
        'scholarship_id': [1, 2, 3, 4, 5],
        'name': ['National Scholarship Portal (NSP)', 'Vanier Canada Graduate Scholarships', 'Gates Cambridge Scholarship', 'Fulbright Foreign Student Program', 'Rotary Foundation Global Scholarship Grants'],
        'min_cgpa': [3.0, 3.5, 3.2, 3.8, 2.5],
        'required_citizen': ['India', 'Canada', 'Any', 'USA', 'Any'],
        'max_income': [50000, 60000, 100000, 70000, 80000],
        'preferred_degree': ['Bachelors', 'Masters', 'Bachelors', 'Bachelors', 'Any']
    }

    scholarships_df = pd.DataFrame(scholarship_data)

    # Eligibility criteria column
    scholarships_df['eligibility_criteria'] = scholarships_df.apply(
        lambda row: f"Minimum CGPA: {row['min_cgpa']}, Required Citizen: {row['required_citizen']}, "
                    f"Maximum Income: {row['max_income']}, Preferred Degree: {row['preferred_degree']}",
        axis=1
    )

    # Vectorize eligibility criteria
    vectorizer = TfidfVectorizer()
    scholarship_vectors = vectorizer.fit_transform(scholarships_df['eligibility_criteria'])

    return scholarships_df, scholarship_vectors, vectorizer

def scholarship(scholarships_df, scholarship_vectors, vectorizer, cgpa, income, citizen, degree):
    # Create a profile for the student's input
    student_profile = f"Minimum CGPA: {cgpa}, Required Citizen: {citizen}, Maximum Income: {income}, Preferred Degree: {degree}"

    # Transform the profile using the same vectorizer
    student_vector = vectorizer.transform([student_profile])

    # Calculate similarity
    similarity_matrix = cosine_similarity(student_vector, scholarship_vectors)

    # Fetch top scholarships based on similarity
    similarities = similarity_matrix[0]
    top_indices = np.argsort(similarities)[-3:][::-1]

    # Prepare recommendations
    recommendations = []
    for index in top_indices:
        recommendations.append(f'''Name: {scholarships_df.iloc[index]['name']},
            Similarity: {similarities[index]:.2f}'''
        )


    return recommendations
