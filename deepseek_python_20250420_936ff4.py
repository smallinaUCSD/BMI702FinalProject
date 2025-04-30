import pandas as pd
import os
import re

def extract_drugs_from_ann(ann_content, txt_content):
    # Regex to parse T/A/R lines
    entity_pattern = re.compile(r'^(T\d+)\t(\S+) (\d+ \d+)\t(.+)$', re.MULTILINE)
    attribute_pattern = re.compile(r'^(A\d+)\t(\S+) (\S+) (.+)$', re.MULTILINE)
    
    entities = {}
    attributes = {}
    discontinued_drugs = set()

    # Parse entities (T tags)
    for match in entity_pattern.finditer(ann_content):
        entity_id, entity_type, span, text = match.groups()
        start, end = map(int, span.split())
        entities[entity_id] = {
            'type': entity_type,
            'start': start,
            'end': end,
            'text': text
        }
    
    # Parse attributes (A tags) for discontinued status
    for match in attribute_pattern.finditer(ann_content):
        attr_id, attr_type, target_entity, value = match.groups()
        if "DISCONTINUED" in value or "discontinued" in value.lower():
            if target_entity in entities:
                discontinued_drugs.add(entities[target_entity]['text'].split()[0].lower())
    
    # Extract medications from TREATMENT entities
    medications = []
    for entity in entities.values():
        if entity['type'] == "TREATMENT" and "Medication" in entity['text']:
            # Get the full prescription line from text
            snippet = txt_content[entity['start']:entity['end']]
            
            # Skip discontinued medications
            drug_name = entity['text'].split()[0].lower()
            if drug_name in discontinued_drugs:
                continue
            
            # Extract dosage/frequency using regex
            dosage = re.search(r'(\d+\s*mg|\d+\s*unit)', snippet, re.IGNORECASE)
            frequency = re.search(r'(daily|bid|tid|q\d+h|every\s*\d+\s*hours?)', snippet, re.IGNORECASE)
            
            medications.append({
                'drug': entity['text'].split('(')[0].strip(),
                'dosage': dosage.group(0) if dosage else '',
                'frequency': frequency.group(0).lower() if frequency else '',
                'text_snippet': snippet
            })
    
    return pd.DataFrame(medications)

# Example usage
ann_folder = "test/ann"
txt_folder = "test/txt"

for ann_file in os.listdir(ann_folder):
    if not ann_file.endswith(".ann"):
        continue
    
    # Read files
    with open(os.path.join(ann_folder, ann_file), 'r') as f:
        ann_content = f.read()
    
    txt_file = ann_file.replace(".ann", ".txt")
    with open(os.path.join(txt_folder, txt_file), 'r') as f:
        txt_content = f.read()
    
    # Process
    df = extract_drugs_from_ann(ann_content, txt_content)
    df.to_csv(f"{ann_file}_medications.csv", index=False)

print("Extraction complete! Check CSV files.")