def recommend_by_difficulty(data, difficulty_level,category):
    filtered_courses = data[(data['course_difficulty'] == difficulty_level) & (data['course_category'] == category)]
    return filtered_courses[['course_title', 'course_difficulty']]
