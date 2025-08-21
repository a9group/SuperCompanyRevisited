import csv, os

# read persona table
def read_persona_table(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f, delimiter='|')
        return [row for row in reader]

def read_interaction_details(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f, delimiter='|')
        return {row['persona']: row for row in reader}

def read_rasci(path):
    with open(path) as f:
        return f.read()

template = (
    "As a {persona}, you operate within the Tetrix Prism model where Strategy, Culture, and Execution form a balanced triad. "
    "You are responsible for {resourcing} and ensuring {key_metrics}. Your capacity is {capacity}. "
    "Company goals: {company_goals}. Core values: {values}. Key tools: N/A.\n\n"
    "When interacting with {relevant_roles}, highlight {key_points_of_interaction_and_collaboration}. "
    "Ensure that {specific_actions_or_behaviors}. This framework mirrors a fractal pyramid so changes at the strategic level "
    "cascade cleanly through execution."
)

personas = read_persona_table('persona_table.csv')
interactions = read_interaction_details('interaction_details.csv')
rasci_content = read_rasci('rasci_table.csv')

for p in personas:
    persona = p['persona']
    detail = interactions.get(persona, {})
    prompt = template.format(
        persona=persona,
        resourcing=p['resourcing'],
        key_metrics=p['key_metrics'],
        capacity=p['capacity'],
        company_goals=p['company_goals'],
        values=p['values'],
        relevant_roles=detail.get('relevant_roles', 'N/A'),
        key_points_of_interaction_and_collaboration=detail.get('key_points_of_interaction_and_collaboration', 'N/A'),
        specific_actions_or_behaviors=detail.get('specific_actions_or_behaviors', 'N/A'),
    )
    dir_name = os.path.join('persona_prompts', persona.replace(' ', '_'))
    os.makedirs(dir_name, exist_ok=True)
    with open(os.path.join(dir_name, 'prompt.txt'), 'w') as f:
        f.write(prompt)
    with open(os.path.join(dir_name, 'persona.txt'), 'w') as f:
        f.write(f"Persona: {persona}\n\nPrompt:\n{prompt}\n")
    with open(os.path.join(dir_name, 'rasci_table.csv'), 'w') as f:
        f.write(rasci_content)

print("Persona prompts generated")
