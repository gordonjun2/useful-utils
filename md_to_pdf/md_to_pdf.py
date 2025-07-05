import pypandoc

input_md = "../discussion_insight_extractor/discussion_insight_20250705_212652.md"
output_pdf = "output.pdf"

# Convert markdown to pdf
pypandoc.convert_file(input_md, 'pdf', outputfile=output_pdf)

print(f"Converted {input_md} to {output_pdf}")
