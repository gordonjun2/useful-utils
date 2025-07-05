import markdown
from weasyprint import HTML
from datetime import datetime

sys_msg = """
I will provide you with a segment of a transcription from a spoken discussion. The transcription may not be perfect, but please do your best to make sense of it.

Please analyze the content and extract the following:

------
Key Discussion Points:
List the main points or topics being discussed in this segment. Capture important ideas, arguments, or themes. Keep them concise but informative.

Mentioned Projects / Products / Tools:
Identify all specific projects, products, tools, companies, or technologies mentioned in the text. For each one, provide a short description based on the context, or from external knowledge if the context is unclear or transcription appears inaccurate.
Some names or terms may be misspelled. Use your knowledge of known technologies, companies, and tools to infer the most likely intended references and replace or correct them as needed. Aim for accuracy and relevance.

Notable Quotes or Opinions:
Extract any statements that reflect strong opinions, insightful comments, or notable quotes. Attribute them to the speaker if speaker names or labels are present.
------

The transcript will be sent in batches, so treat each batch as part of a larger conversation. Do not summarize or conclude; just extract structured information for the current segment.
"""

sys_msg_final_summary = """
You will be provided with a series of structured insights extracted from multiple transcription segments. Your task is to combine them into a single, cohesive markdown document that summarizes the discussion as a whole.

Please follow this structure exactly:

------
# Executive Summary
Provide a concise overview of the key themes and takeaways from the entire discussion. Focus on overarching insights, decisions, and purpose of the conversation.

# Key Discussion Points
Combine and deduplicate the main discussion points from all segments. Group similar ideas and arrange them logically to reflect the flow of the conversation. Use bullet points and preserve clarity.

# Mentioned Projects / Products / Tools
List all unique projects, products, tools, companies, or technologies that were mentioned across segments. If any were repeated, merge context where relevant. Include short descriptions if they were provided.

# Notable Quotes or Opinions (optional)
Include a curated list of the most insightful or opinionated quotes. Attribute them if speaker names or labels were available. Only include quotes that add meaningful perspective.
------

Guidelines:
- Do not summarize the original paragraphs again. Only work with the structured outputs you were given.
- Ensure **no key points or tools mentioned are lost** during merging.
- Focus on **clarity, conciseness, and logical organization**.
- Output only markdown content — do not explain or add commentary.
- Do not add the '------' separator at the start and the end of the output.

The final result should be ready for presentation in a document or report.
"""


def convert_text_to_md(markdown_text, output_file=None):
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"discussion_insight_{timestamp}.md"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(markdown_text)


def convert_text_to_pdf(markdown_text, output_file=None):
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"discussion_insight_{timestamp}.pdf"

    html_text = markdown.markdown(markdown_text, output_format='html5')

    html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            h1, h2, h3 {{ color: #333; }}
            ul {{ margin-left: 1em; }}
        </style>
    </head>
    <body>
    {html_text}
    </body>
    </html>
    """

    HTML(string=html_document).write_pdf(output_file)
