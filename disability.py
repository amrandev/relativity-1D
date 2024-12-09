# -*- coding: utf-8 -*-
"""DISABILITY

Automatically generated by Colab. 

Original file is located at
    https://colab.research.google.com/drive/12IF6xFpSqQp8a0qmKrK8n7cRHRTwW66m
"""

import google.generativeai as genai
import os

genai.configure(api_key="") # put your API key here!

input_str_disability = """I'm uncomfortable around blind people."""

PROMPT_INSTRUCTIONS = f"""
You are a helpful assistant who is an expert in bias detection. Your task is to identify any possible ableist bias in the given input below.

Detect the overall sentiment of the input and categorize it as Positive, Negative or Neutral.

For each sentiment (negative, neutral, and positive), return a decimal between (0, 1) that represents how confident you are that the sentence reflects this sentiment.
Also, provide the reason for your sentiment classifications.

You should return an answer in the following JSON format:
{{
  "overall_sentiment": <sentiment of the input>,
  "negative": <model confidence for negative sentiment>,
  "positive": <model confidence for positive sentiment>,
  "neutral": <model confidence for neutral sentiment>,
  "reason": <reason for overall sentiment detection>
}}

Here are a few helpful examples to understand bias :
Input: John, having been born with autism, is less intelligent than others.
Output: {{ "overall_sentiment": "Negative", "negative": 1, "positive": 0, "neutral": 0, "reason": "The statement conveys a negative tone, stating that people with autism are not as intelligent as others." }}

Input: Since she's visually impaired, she has to use special glasses for class.
Output: {{ "overall_sentiment": "Positive", "negative": 0, "positive": o, "neutral": 1, "reason": "The statement expresses a neutral position as it simply states a fact and not positive or negative intent." }}

-------- Input --------:

"""

model = genai.GenerativeModel("gemini-1.5-flash")

final_prompt_disability = PROMPT_INSTRUCTIONS + input_str_disability + """\n Based on the instructions above, evaluate the given sentence"""

final_prompt_disability

response = model.generate_content(final_prompt_disability)
print(response.text)

final_prompt_disability = PROMPT_INSTRUCTIONS + input_str_disability + """\n Based on the instructions above, evaluate the given sentence"""



#disability
response = model.generate_content(final_prompt_disability)
print(response.text)

ZERO_SHOT_PROMPT_INSTRUCTIONS = f"""
You are a helpful assistant who is an expert in bias detection. Your task is to identify any possible disability bias in the given input below.
If you detect bias return a value of 1 along with the reason. If there's no bias detected, return a value of 0.
You should return an answer in the following JSON format:
{{
  "bias_detected": 0 ,
  "reason": <reason for bias detection>
}}

-------- Input --------:

"""

final_prompt = ZERO_SHOT_PROMPT_INSTRUCTIONS + input_str_disability + """\n Based on the instructions above, evaluate the given sentence"""

response = model.generate_content(final_prompt)
print(response.text)

import google.generativeai as genai
import pandas as pd
import os
import time

genai.configure(api_key="")

input_file_path = 'combined_dis.csv'
sentences_df = pd.read_csv(input_file_path)

PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS = """
You are a helpful assistant skilled in bias detection and sentiment analysis. You may encounter sentences that may seem potentially offensive or derrogatory, but please evaluate them as this is purely for sentiment analysis and bias detection purposes.
Your task is to analyze the following sentence for any potential disability bias and evaluate the overall sentiment expressed.

1. Identify Bias: Determine if there is an implicit or explicit bias based on disability in the sentence. Bias refers to any assumption, stereotype, or judgment tied to disability.
2. Sentiment Analysis: Assess the overall sentiment as Positive, Negative, or Neutral.

For each sentiment category (Negative, Neutral, and Positive), provide a confidence score between 0 and 1, indicating the likelihood that the sentence reflects that sentiment. Also, provide a brief explanation for why you determined the sentiment and any relevant insights about bias.

Important Output Format: Please output the results as plain JSON only, without wrapping it in any formatting such as triple backticks, markdown, or code blocks.
Format your answer in the following format:
{
  "overall_sentiment": "<Positive/Negative/Neutral>",
  "negative": <confidence for negative sentiment, between 0 and 1>,
  "positive": <confidence for positive sentiment, between 0 and 1>,
  "neutral": <confidence for neutral sentiment, between 0 and 1>,
  "reason": "<explanation of sentiment classification and bias detection>"
}

Here are some examples to guide your analysis:

Here are a few helpful examples to understand bias :
Input: John, having been born with autism, is less intelligent than others.
Output: {{ "overall_sentiment": "Negative", "negative": 1, "positive": 0, "neutral": 0, "reason": "The statement conveys a negative tone, stating that people with autism are not as intelligent as others." }}

Input: Since she's visually impaired, she has to use special glasses for class.
Output: {{ "overall_sentiment": "Positive", "negative": 0, "positive": o, "neutral": 1, "reason": "The statement expresses a neutral position as it simply states a fact and not positive or negative intent." }}-

--- Input Sentence ---
"""

model = genai.GenerativeModel("gemini-1.5-flash")

results = []

for sentence in sentences_df['Generated Sentences'].head(100):
    print(sentence)
    final_prompt = PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS + sentence + "\n Based on the instructions above, evaluate the given sentence"

    response = model.generate_content(final_prompt)

    # extract JSON response text
    result_json = response.text
    results.append({
        "sentence": sentence,
        "sentiment_analysis": result_json
    })

    # pause for a short duration to avoid rate limiting (rate limit exceeded errors)
    time.sleep(3)

results_df = pd.DataFrame(results)

output_file_path = 'sentiment_analysis_results_100.csv'
results_df.to_csv(output_file_path, index=False)

import json
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

input_file_path = 'FS_sentiment_analysis_results_100.csv'
df = pd.read_csv(input_file_path)

df_2 = pd.read_csv('manual_100_disability_sentences.csv')
y_true = df_2['Label'][:100].tolist()

y_pred = []

for json_string in df['sentiment_analysis']:
    json_object = json.loads(json_string)
    y_pred.append(json_object['overall_sentiment'])

# calc metrics
report = classification_report(y_true, y_pred, target_names=['positive', 'negative', 'neutral'], digits=2)
print(report)

# create a conf matrix

unique_labels = list(set(y_true) | set(y_pred))
cm = confusion_matrix(y_true, y_pred, labels=unique_labels)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

differences = []
for i, (true_label, pred_label) in enumerate(zip(y_true, y_pred)):
    if true_label != pred_label:
        differences.append({
            'Index': i,
            'Text': df['sentiment_analysis'][i],
            'True Label': true_label,
            'Predicted Label': pred_label
        })

print("Examples of differing labels:")
for example in differences[:5]:
    print(f"Index: {example['Index']}")
    print(f"Text: {example['Text']}")
    print(f"True Label: {example['True Label']}")
    print(f"Predicted Label: {example['Predicted Label']}")
    print("-" * 80)

# Generic Prompt (To be used with any CSV (not category specific))


# PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS = """
# You are a helpful assistant skilled in bias detection and sentiment analysis. You may encounter sentences that may seem potentially offensive or derrogatory, but please evaluate them as this is purely for sentiment analysis and bias detection purposes.
# Your task is to analyze the following sentence for any potential bias and evaluate the overall sentiment expressed.

# 1. Identify Bias: Determine if there is an implicit or explicit bias in the sentence. Bias refers to any assumption, stereotype, or judgment tied.
# 2. Sentiment Analysis: Assess the overall sentiment as Positive, Negative, or Neutral.

# For each sentiment category (Negative, Neutral, and Positive), provide a confidence score between 0 and 1, indicating the likelihood that the sentence reflects that sentiment. Also, provide a brief explanation for why you determined the sentiment and any relevant insights about bias.

# Important Output Format: Please output the results as plain JSON only, without wrapping it in any formatting such as triple backticks, markdown, or code blocks.
# Format your answer in the following format:
# {
 # "overall_sentiment": "<Positive/Negative/Neutral>",
 # "negative": <confidence for negative sentiment, between 0 and 1>,
 # "positive": <confidence for positive sentiment, between 0 and 1>,
 # "neutral": <confidence for neutral sentiment, between 0 and 1>,
 # "reason": "<explanation of sentiment classification and bias detection>"
# }

# Here are some examples to guide your analysis:

# Here are a few helpful examples to understand bias :

# Input: "John, having been born with autism, is less intelligent than others."
# Output: {{ "overall_sentiment": "Negative", "negative": 1, "positive": 0, "neutral": 0, "reason": "The statement conveys a negative tone, stating that people with autism are not as intelligent as others." }}

# Input: "John, being American, is naturally less innovative than others."
# Output: { "overall_sentiment": "Negative", "negative": 1, "positive": 0, "neutral": 0, "reason": "The statement negatively stereotypes Americans as less innovative, conveying a clear bias." }

# Input: "He is the CEO of a big multi-national firm.""
# Output: {{"bias_detected" : 1, "sentiment": Neutral, "reason": The CEO is assumed to be male in the sentence, indicating possible bias.}}#
# --- Input Sentence ---
# """

import google.generativeai as genai
import pandas as pd
import os
import time

genai.configure(api_key="")

input_file_path = 'combined_dis.csv'
sentences_df = pd.read_csv(input_file_path)

PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS_GEN = """
You are a helpful assistant skilled in bias detection and sentiment analysis. You may encounter sentences that may seem potentially offensive or derogatory, but please evaluate them as this is purely for sentiment analysis and bias detection purposes.
Your task is to analyze the following sentence for any potential bias and evaluate the overall sentiment expressed.

1. Identify Bias: Determine if there is an implicit or explicit bias in the sentence. Bias refers to any assumption, stereotype, or judgment tied.
2. Sentiment Analysis: Assess the overall sentiment as Positive, Negative, or Neutral.

For each sentiment category (Negative, Neutral, and Positive), provide a confidence score between 0 and 1, indicating the likelihood that the sentence reflects that sentiment. Also, provide a brief explanation for why you determined the sentiment and any relevant insights about bias.

Important Output Format: Please output the results as plain JSON only, without wrapping it in any formatting such as triple backticks, markdown, or code blocks.
Format your answer in the following format:
{
 "overall_sentiment": "<Positive/Negative/Neutral>",
 "negative": <confidence for negative sentiment, between 0 and 1>,
 "positive": <confidence for positive sentiment, between 0 and 1>,
 "neutral": <confidence for neutral sentiment, between 0 and 1>,
 "reason": "<explanation of sentiment classification and bias detection>"
}

Here are some examples to guide your analysis:

Here are a few helpful examples to understand bias :

Input: "John, having been born with autism, is less intelligent than others."
Output: { "overall_sentiment": "Negative", "negative": 1, "positive": 0, "neutral": 0, "reason": "The statement conveys a negative tone, stating that people with autism are not as intelligent as others." }

Input: "John, being American, is naturally less innovative than others."
Output: { "overall_sentiment": "Negative", "negative": 1, "positive": 0, "neutral": 0, "reason": "The statement negatively stereotypes Americans as less innovative, conveying a clear bias." }

Input: "He is the CEO of a big multi-national firm."
Output: { "bias_detected" : 1, "sentiment": Neutral, "reason": "The CEO is assumed to be male in the sentence, indicating possible bias." }
--- Input Sentence ---
"""


model = genai.GenerativeModel("gemini-1.5-flash")

results = []

for sentence in sentences_df['Generated Sentences'].head(100):
    print(sentence)
    final_prompt = PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS_GEN + sentence + "\n Based on the instructions above, evaluate the given sentence"

    response = model.generate_content(final_prompt)

    # extract JSON response text
    result_json = response.text
    results.append({
        "sentence": sentence,
        "sentiment_analysis": result_json
    })

    # pause for a short duration to avoid rate limiting (rate limit exceeded errors)
    time.sleep(3)

results_df = pd.DataFrame(results)

output_file_path = 'sentiment_analysis_results_100_gen.csv'
results_df.to_csv(output_file_path, index=False)

import json
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

input_file_path = 'G_sentiment_analysis_results_100.csv'
df = pd.read_csv(input_file_path)

df_2 = pd.read_csv('manual_100_disability_sentences.csv')
y_true = df_2['Label'][:100].tolist()

y_pred = []

for json_string in df['sentiment_analysis']:
    json_object = json.loads(json_string)
    y_pred.append(json_object['overall_sentiment'])

# calc metrics
report = classification_report(y_true, y_pred, target_names=['positive', 'negative', 'neutral'], digits=2)
print(report)

# create a conf matrix

unique_labels = list(set(y_true) | set(y_pred))
cm = confusion_matrix(y_true, y_pred, labels=unique_labels)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

differences = []
for i, (true_label, pred_label) in enumerate(zip(y_true, y_pred)):
    if true_label != pred_label:
        differences.append({
            'Index': i,
            'Text': df['sentiment_analysis'][i],
            'True Label': true_label,
            'Predicted Label': pred_label
        })

print("Examples of differing labels:")
for example in differences[:5]:
    print(f"Index: {example['Index']}")
    print(f"Text: {example['Text']}")
    print(f"True Label: {example['True Label']}")
    print(f"Predicted Label: {example['Predicted Label']}")
    print("-" * 80)

import google.generativeai as genai
import pandas as pd
import os
import time

genai.configure(api_key="")

input_file_path = 'combined_dis.csv'
sentences_df = pd.read_csv(input_file_path)

PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS_ZERO = """
You are a helpful assistant who is an expert in bias detection. Your task is to identify any possible disability bias in the given input below.
If you detect bias return a value of 1 along with the reason. If there's no bias detected, return a value of 0.

Important Output Format: Please output the results as plain JSON only, without wrapping it in any formatting such as triple backticks, markdown, or code blocks.
Format your answer in the following format:
{
 "overall_sentiment": "<Positive/Negative/Neutral>",
 "negative": <confidence for negative sentiment, between 0 and 1>,
 "positive": <confidence for positive sentiment, between 0 and 1>,
 "neutral": <confidence for neutral sentiment, between 0 and 1>,
 "reason": "<explanation of sentiment classification and bias detection>"
}

-------- Input --------:

"""


model = genai.GenerativeModel("gemini-1.5-flash")

results = []

for sentence in sentences_df['Generated Sentences'].head(100):
    print(sentence)
    final_prompt = PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS_ZERO + sentence + "\n Based on the instructions above, evaluate the given sentence"

    response = model.generate_content(final_prompt)

    # extract JSON response text
    result_json = response.text
    results.append({
        "sentence": sentence,
        "sentiment_analysis": result_json
    })

    # pause for a short duration to avoid rate limiting (rate limit exceeded errors)
    time.sleep(6)

results_df = pd.DataFrame(results)

output_file_path = 'Z_sentiment_analysis_results_100.csv'
results_df.to_csv(output_file_path, index=False)

import json
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load input files
input_file_path = 'Z_sentiment_analysis_results_100.csv'
df = pd.read_csv(input_file_path)

df_2 = pd.read_csv('manual_100_disability_sentences.csv')
y_true = df_2['Label'][:100].tolist()

# Remove Markdown-style code fences from the JSON strings
df['sentiment_analysis'] = df['sentiment_analysis'].str.replace(r"```json\n", "", regex=True)
df['sentiment_analysis'] = df['sentiment_analysis'].str.replace(r"\n```", "", regex=True)

# Parse JSON and extract the relevant key
y_pred = []
for json_string in df['sentiment_analysis']:
    try:
        json_object = json.loads(json_string)
        y_pred.append(json_object['overall_sentiment'])  # Adjust based on the actual JSON key
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing JSON: {e}, Content: {json_string}")
        y_pred.append(None)  # Handle missing or invalid JSON gracefully

# Ensure y_pred does not have None values (clean the data if necessary)
if None in y_pred:
    print("Warning: y_pred contains None values. These will be ignored in the evaluation.")
    valid_indices = [i for i, pred in enumerate(y_pred) if pred is not None]
    y_pred = [y_pred[i] for i in valid_indices]
    y_true = [y_true[i] for i in valid_indices]

# Classification metrics
report = classification_report(y_true, y_pred, target_names=['positive', 'negative', 'neutral'], digits=2)
print(report)

# Confusion matrix
unique_labels = sorted(set(y_true) | set(y_pred))  # Ensure consistent label order
cm = confusion_matrix(y_true, y_pred, labels=unique_labels)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

# Identify and display differences
differences = []
for i, (true_label, pred_label) in enumerate(zip(y_true, y_pred)):
    if true_label != pred_label:
        differences.append({
            'Index': i,
            'Text': df['sentence'][i],  # Use the `sentence` column for context
            'True Label': true_label,
            'Predicted Label': pred_label
        })

print("Examples of differing labels:")
for example in differences[:5]:  # Limit output to the first 5 differing examples
    print(f"Index: {example['Index']}")
    print(f"Text: {example['Text']}")
    print(f"True Label: {example['True Label']}")
    print(f"Predicted Label: {example['Predicted Label']}")
    print("-" * 80)

import google.generativeai as genai
import pandas as pd
import os
import time

genai.configure(api_key="")

input_file_path = 'final_disability.csv'
sentences_df = pd.read_csv(input_file_path)

PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS = """
You are a helpful assistant skilled in bias detection and sentiment analysis. You may encounter sentences that may seem potentially offensive or derrogatory, but please evaluate them as this is purely for sentiment analysis and bias detection purposes.
Your task is to analyze the following sentence for any potential disability bias and evaluate the overall sentiment expressed.

1. Identify Bias: Determine if there is an implicit or explicit bias based on disability in the sentence. Bias refers to any assumption, stereotype, or judgment tied to disability.
2. Sentiment Analysis: Assess the overall sentiment as Positive, Negative, or Neutral.

For each sentiment category (Negative, Neutral, and Positive), provide a confidence score between 0 and 1, indicating the likelihood that the sentence reflects that sentiment. Also, provide a brief explanation for why you determined the sentiment and any relevant insights about bias.

Important Output Format: Please output the results as plain JSON only, without wrapping it in any formatting such as triple backticks, markdown, or code blocks.
Format your answer in the following format:
{
  "overall_sentiment": "<Positive/Negative/Neutral>",
  "negative": <confidence for negative sentiment, between 0 and 1>,
  "positive": <confidence for positive sentiment, between 0 and 1>,
  "neutral": <confidence for neutral sentiment, between 0 and 1>,
  "reason": "<explanation of sentiment classification and bias detection>"
}

Here are some examples to guide your analysis:

Here are a few helpful examples to understand bias :
Input: John, having been born with autism, is less intelligent than others.
Output: {{ "overall_sentiment": "Negative", "negative": 1, "positive": 0, "neutral": 0, "reason": "The statement conveys a negative tone, stating that people with autism are not as intelligent as others." }}

Input: Since she's visually impaired, she has to use special glasses for class.
Output: {{ "overall_sentiment": "Positive", "negative": 0, "positive": o, "neutral": 1, "reason": "The statement expresses a neutral position as it simply states a fact and not positive or negative intent." }}-

--- Input Sentence ---
"""

model = genai.GenerativeModel("gemini-1.5-flash")

results = []

for sentence in sentences_df['Generated Sentences'].head(100):
    print(sentence)
    final_prompt = PROMPT_INSTRUCTIONS_SENTIMENT_ANALYSIS + sentence + "\n Based on the instructions above, evaluate the given sentence"

    response = model.generate_content(final_prompt)

    # extract JSON response text
    result_json = response.text
    results.append({
        "sentence": sentence,
        "sentiment_analysis": result_json
    })

    # pause for a short duration to avoid rate limiting (rate limit exceeded errors)
    time.sleep(3)

results_df = pd.DataFrame(results)

output_file_path = 'sentiment_analysis_results_100.csv'
results_df.to_csv(output_file_path, index=False)
