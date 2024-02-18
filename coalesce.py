import json

messages = []
with open("nikki.json", "r") as f:
    messages = json.load(f)

processed_messages = []
delimiter = '|'

for message in messages:
    if processed_messages:
        last_message = processed_messages[-1]
        if last_message['is_from_me'] == message['is_from_me']:
            last_message['text'] += delimiter + message['text']
        else:
            processed_messages.append(message)
    else:
        processed_messages.append(message)

# Save the processed messages in a new JSON file
# with open('nikki_c.json', 'w') as f:
#     json.dump(processed_messages, f)

conversations = []

for idx, message in enumerate(processed_messages[:-1]):
    if message['is_from_me']:
        continue

    input_text = message['text']
    output_text = processed_messages[idx + 1]['text']
    
    if not processed_messages[idx + 1]['is_from_me']:
        continue
    
    conversation_pair = {
        'input': input_text,
        'output': output_text
    }
    conversations.append(conversation_pair)

# Save the conversation pairs in a new JSON file
with open('nikki_conversation_pairs.json', 'w') as f:
    json.dump(conversations, f)