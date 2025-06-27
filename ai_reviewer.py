import google.generativeai as genai


def story_review(story, chapter_title):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    You are a professional Editorial Reviewer.
    Review the rewritten chapter titled "{chapter_title}" and provide:
    - Constructive feedback
    - Clarity improvements
    - Emotional tone suggestions
    - Language issues or awkwardness
    - Any structural problems
    Chapter Text:
    {story}
    """
    response = model.generate_content(prompt)
    return response.text.strip()
