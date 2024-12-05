def recommend_by_difficulty(data, difficulty_level):
    filtered_courses = data[data['course_difficulty'] == difficulty_level]
    return filtered_courses[['course_title', 'course_difficulty']]
