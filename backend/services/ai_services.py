import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def format_response(text: str) -> str:
    """Format AI response for better readability"""
    if not text:
        return text
    
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append('')
        # Remove markdown headers (###, ##, #) and make them bold
        elif line.startswith('###'):
            clean_text = line.replace('###', '').strip()
            formatted_lines.append(f'━━ {clean_text} ━━')
        elif line.startswith('##'):
            clean_text = line.replace('##', '').strip()
            formatted_lines.append(f'\n━━━ {clean_text} ━━━')
        elif line.startswith('#'):
            clean_text = line.replace('#', '').strip()
            formatted_lines.append(f'\n━━━━ {clean_text} ━━━━')
        # Keep numbered/bulleted lists clean
        elif line[0].isdigit() and '.' in line[:3]:
            formatted_lines.append(f'  {line}')
        elif line.startswith('-') or line.startswith('•'):
            formatted_lines.append(f'  {line}')
        # Remove markdown bold/italic markers but keep text
        elif '**' in line or '__' in line:
            clean_text = line.replace('**', '').replace('__', '')
            formatted_lines.append(clean_text)
        else:
            formatted_lines.append(line)
    
    # Join with newlines and clean up excessive spacing
    result = '\n'.join(formatted_lines)
    
    # Replace multiple newlines with max 2
    while '\n\n\n' in result:
        result = result.replace('\n\n\n', '\n\n')
    
    return result.strip()

def generate_chat_reply(message: str) -> str:
    if not message or not message.strip():
        return "Please enter a message."

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You are a helpful fitness assistant. Give safe, practical advice. Format responses with clear section breaks using line breaks. Use numbered lists for steps (1. 2. 3.) and dashes for bullet points. Do NOT use markdown formatting like #, ##, ***, or __ . Just use plain text with clean line breaks between sections."},
            {"role": "user", "content": message}
        ]
    )

    # Extract text
    text = ""
    for item in response.output:
        if item.type == "message":
            for c in item.content:
                if c.type == "output_text":
                    text += c.text

    formatted_text = format_response(text)
    return formatted_text or "No response returned."