def clean(input,output):
    with open(input, 'r') as file, open(output, 'w') as f:
            prev_line = ''
            for line in file:
                if '<Media omitted>' in line or 'This message was deleted' in line:
                     continue
                line = line.strip()
                if '-' in line:
                    if prev_line:
                        f.write(prev_line + '\n')
                    prev_line = line
                else:
                    prev_line += ' ' + line
            if prev_line:
                f.write(prev_line + '\n')


def parse_chat(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    messages = []
    for line in lines:
        messages.append(line)
    return messages

def chunk_messages(messages,chunk_size=10):
    chunks=[]
    for i in range(0,len(messages),7):
        block = messages[i:i+chunk_size]
        text = ""
        for m in block:
            text += m + '\n'
        chunks.append(text)  
    return chunks                     



