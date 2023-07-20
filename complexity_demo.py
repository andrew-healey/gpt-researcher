import complexity

url = "https://www.glassdoor.com/Overview/Working-at-OpenAI-EI_IE2210885.11,17.htm"

simple_text,simple_html = complexity.visit(url,as_markdown=True)

with open("openai.md","w") as f:
    f.write(simple_text)

print("Done")