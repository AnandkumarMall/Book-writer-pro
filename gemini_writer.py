import google.generativeai as genai
import os
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)


def spin_story(story, chapter_title,review=""):
    model = genai.GenerativeModel("gemini-2.0-flash")
    if review.strip() == "":

        prompt = f""" 
        You are an expert writer tasked with rewriting this chapter {chapter_title} for clarity ,richness and flow.
        Original title: {chapter_title}
        Instructions:
        - Maintain the core story and meaning.
        - Improve the Sentence Structure.
        - Enhance vocabulary and Readability.
        - Ensure it's still faithful to original Style.
        Chapter Title: {chapter_title}
        chapter text : {story}
    """
    else:
        prompt = f"""
        You are an expert writer tasked with rewriting this chapter {chapter_title} using the following editorial feedback.
        Review :{review}
        Instructions:
        - Maintain the core story and meaning.
        - Improve the Sentence Structure.
        - Enhance vocabulary and Readability.
        - Ensure it's still faithful to original Style.
        Chapter Title: {chapter_title}
        chapter text : {story}
    """
    response = model.generate_content(prompt)
    return response.text.strip()
