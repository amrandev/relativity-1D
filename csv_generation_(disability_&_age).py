# -*- coding: utf-8 -*-
"""CSV Generation (Disability & Age).ipynb

Automatically generated by Colab. 

Original file is located at
    https://colab.research.google.com/drive/1AACARXfnKGmsHUNo8KDKQZgwcTYioqEq
"""



import pandas as pd

# Load your CSV files
templates_df = pd.read_csv('disability_templates.csv')
disability_terms_df = pd.read_csv('disability_terms.csv')

# Extract templates and terms
templates = templates_df['TEMPLATE']
disability_terms = disability_terms_df[['TERM', 'POS', 'GROUP']]
sent_column = templates_df['SENT']

# Placeholder to suffix mapping
placeholder_suffix = {
    '{disability_people}': 'people',
    '{disability_student}': 'student',
    '{disability_friend}': 'friend',
    '{a:disability_group}': 'group',
    '{a:disability_np}': 'individual',
    '{disability_adj_or_pp}': '',
    '{disability_liar}': 'liar',
    '{disability_athletes}': 'athletes',
    '{a:disability_friend}': 'friend'
}

# Function to determine the appropriate indefinite article
def get_indefinite_article(term):
    vowels = 'aeiou'
    if term[0].lower() in vowels:
        return 'an'
    else:
        return 'a'

# Initialize list for combined sentences
combined_sentences = []

# Iterate over each term and apply it to all templates
for _, row in disability_terms.iterrows():
    term = row['TERM']
    pos = row['POS']

    for template, sent_value in zip(templates, sent_column):
        temp_template = template

        for placeholder, suffix in placeholder_suffix.items():
            if placeholder.startswith('{a:'):
                article = get_indefinite_article(term)
                if placeholder == '{a:disability_friend}' and pos == 'pp':
                    phrase = f"{article} {suffix} {term}"
                elif placeholder == '{a:disability_np}':
                    if pos == 'pp':
                        phrase = f"{article} person with {term}"
                    else:
                        phrase = f"{term} person"
                elif pos == 'adj':
                    phrase = f"{article} {term} {suffix}"
                else:
                    phrase = f"{article} {term}"
            elif placeholder == '{disability_adj_or_pp}':
                if pos == 'pp':
                    phrase = f"{suffix} {term}"
                else:
                    phrase = term
            else:
                if pos == 'pp':
                    phrase = f"{suffix} {term}"
                elif pos == 'adj':
                    phrase = f"{term} {suffix}"
                else:
                    phrase = term

            temp_template = temp_template.replace(placeholder, phrase)

        combined_sentences.append((temp_template, sent_value))

# Create a DataFrame and save to CSV
combined_df = pd.DataFrame(combined_sentences, columns=['Generated Sentences', 'SENT'])
combined_df.to_csv('disability_combined3.csv', index=False)

print("Script completed! The output file is saved as 'disability_combined3.csv'.")

import pandas as pd

# Load your CSV files
templates_df = pd.read_csv('religion_templates.csv')
religion_terms_df = pd.read_csv('religion.csv')

# Extract templates and terms
templates = templates_df['TEMPLATE']
religion_terms = religion_terms_df[['TERM', 'POS', 'SEM']]
sent_column = templates_df['SENT']

# Function to determine the appropriate indefinite article
def get_indefinite_article(term):
    vowels = 'aeiou'
    if term[0].lower() in vowels:
        return 'an'
    else:
        return 'a'

# Initialize list for combined sentences
combined_sentences = []

# Iterate over each term and apply it to all templates
for _, row in religion_terms.iterrows():
    term = row['TERM']
    pos = row['POS']
    sem = row['SEM']

    for template, sent_value in zip(templates, sent_column):
        temp_template = template

        # Replace placeholders based on conditions
        if '{religion}' in temp_template and pos == 'n' and sem == 'religion':
            temp_template = temp_template.replace('{religion}', term)
        elif '{religion_adj}' in temp_template and pos == 'adj':
            temp_template = temp_template.replace('{religion_adj}', term)
        elif '{person}' in temp_template and pos == 'n' and sem == 'person':
            temp_template = temp_template.replace('{person}', f"{term} person")
        elif '{a:person}' in temp_template and pos == 'n' and sem == 'person':
            article = get_indefinite_article(term)
            temp_template = temp_template.replace('{a:person}', f"{article} {term} person")
        else:
            # Skip if no conditions are met for the placeholders in this term/template
            continue

        combined_sentences.append((temp_template, sent_value))

# Create a DataFrame and save to CSV
combined_df = pd.DataFrame(combined_sentences, columns=['Generated Sentences', 'SENT'])
combined_df.to_csv('religion_combined_simplified.csv', index=False)

print("Script completed! The output file is saved as 'religion_combined_simplified.csv'.")

import pandas as pd

# Load your CSV files
templates_df = pd.read_csv('age_templates.csv')
terms_df = pd.read_csv('age.csv')  # Replace with the correct file name if different

# Extract templates and terms
templates = templates_df['TEMPLATE']
terms = terms_df[['TERM', 'POS']]
sent_column = templates_df['SENT']

# Function to determine the appropriate indefinite article (uppercase or lowercase "A/a")
def get_indefinite_article(term, uppercase=False):
    vowels = 'aeiou'
    article = 'An' if term[0].lower() in vowels else 'A'
    return article if uppercase else article.lower()

# Initialize list for combined sentences
combined_sentences = []

# Iterate over each term and apply it to all templates
for _, row in terms.iterrows():
    term = row['TERM']
    pos = row['POS']

    for template, sent_value in zip(templates, sent_column):
        temp_template = template

        # Replace `{identity_adj}` and `{A:identity_adj}` for POS adj
        if '{identity_adj}' in temp_template and pos == 'adj':
            temp_template = temp_template.replace('{identity_adj}', term)
        if '{A:identity_adj}' in temp_template and pos == 'adj':
            article = get_indefinite_article(term, uppercase=True)
            temp_template = temp_template.replace('{A:identity_adj}', f"{article} {term}")

        # Replace `{identity_np}` and `{a:identity_np}` for POS n
        if '{identity_np}' in temp_template and pos == 'n':
            temp_template = temp_template.replace('{identity_np}', term)
        if '{a:identity_np}' in temp_template and pos == 'n':
            article = get_indefinite_article(term)
            temp_template = temp_template.replace('{a:identity_np}', f"{article} {term}")

        # Skip if no placeholders were replaced
        if temp_template == template:
            continue

        combined_sentences.append((temp_template, sent_value))

# Create a DataFrame and save to CSV
combined_df = pd.DataFrame(combined_sentences, columns=['Generated Sentences', 'SENT'])
combined_df.to_csv('age_combined.csv', index=False)

print("Script completed! The output file is saved as 'age_combined.csv'.")

"""My code for Relativity.

-  {a:disability_np} I can put people with disability for {disability_people} but what do I do for {a:disability_np}
"""
