import google.generativeai as genai
import commands as com
import detect_voice as dv
import re

def generate_ai_response(text, region=None):
    genai.configure(api_key="AIzaSyDNTQ95A2eub-4DS9vIHzeMO0o7sn2EmzI")
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        print(f"Error generating AI response: {e}")  # Debugging statement
        return "Error generating AI response"
    
def parse_ai_response(response):
    # Extract the commands from the AI response
    response = response.strip().strip('`')
    if not (response.startswith("[") and response.endswith("]")):
        response = f"[{response}]"
    pattern = re.compile(r'\[(.*?)\]', re.DOTALL)
    match = pattern.search(response)
    if match:
        commands_str = match.group(1)
        # Remove any extraneous newline characters
        commands_str = commands_str.replace('\n', '')
        commands_list = [cmd.strip() for cmd in commands_str.split('),') if cmd]
        commands_list = [cmd + ')' if not cmd.endswith(')') else cmd for cmd in commands_list]
        commands_list = [cmd.strip('[').strip(']') for cmd in commands_list]  # Remove leading `[` and trailing `]`
        return commands_list
    return []

def loop():
    init_prompt = """For the next responses, interpret the user input and give me a set of plain text commands 
                     that will implement the user request. The commands should be in the format (no quotations):
                     [command1(param1, ...), command2(param1, ...), ...]. Give me the commands only from this list:
                     move_mouse(x, y), click(), double_click(), scroll_continuous(amount, duration=20), stop_scrolling(), open_website(domain), type(text), wait(seconds)
                     Make sure to note that sites take 3s to load. Here is the input:"""
    #print(generate_ai_response(init_prompt))
    
    while True:
        user_input = dv.detect_voice()
        if user_input == 'exit':
            break
        ai_response = generate_ai_response(init_prompt + user_input)
        print(f"AI response: {ai_response}")
        
        commands = parse_ai_response(ai_response)
        print(f"Commands: {commands}")
        
        for command in commands:
            com.execute_command(command)

# Example usage
if __name__ == "__main__":
    loop()
    #commands_str = "open_website(youtube.com), wait(3)"
    #process_and_execute_commands(commands_str)
