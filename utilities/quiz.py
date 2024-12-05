def recommend_by_difficulty(dataset, difficulty, category):
    filtered_courses = dataset[
        (dataset['course_difficulty'] == difficulty) & 
        (dataset['course_category'] == category)
    ]
    return filtered_courses['course_title'].tolist()
