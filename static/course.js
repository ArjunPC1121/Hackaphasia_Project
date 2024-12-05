function gt() {
    const category = "General Technology";
    const difficulty = "Beginner";
    window.location.href = `/gtBeg?category=${encodeURIComponent(category)}&difficulty=${encodeURIComponent(difficulty)}`;
}
