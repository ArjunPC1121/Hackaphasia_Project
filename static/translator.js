async function translateText() {
    // Get the input text and selected language
    const inputText = document.getElementById("inputText").value;
    const languageSelect = document.getElementById("languageSelect");
    const targetLanguage = languageSelect.value;  // Corrected

    // Validate input
    if (!inputText.trim()) {
        alert("Please enter text to translate.");
        return;
    }

    try {
        // Send a request to the backend for translation
        const response = await fetch("/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text: inputText,
                language: targetLanguage,  // Corrected
            }),
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error("Failed to fetch translation.");
        }

        // Parse the JSON response
        const data = await response.json();
        console.log(data); // For debugging purposes

        // Display the translated text
        const translatedText = document.getElementById("translatedText");
        translatedText.textContent = data.translated_text; // Assumes backend sends { "translated_text": ... }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while translating the text.");
    }
}
