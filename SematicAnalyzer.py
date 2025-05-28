import sqlite3
from openai import OpenAI

# 1. Set your API key
client = OpenAI(api_key=)

# 2. Fetch statement-action pairs from DB
def fetch_statement_action_pairs(db_path="output_database.db", table_name="country_statements"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Make sure your table and columns are named correctly!
    query = f"SELECT Statement, Action_Taken FROM {table_name} LIMIT 3"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows  # list of (statement, action)

# 3. Ask GPT-4o-mini to evaluate truthfulness of statement given action
def evaluate_truthfulness(statement, action):
    prompt = (
        f"Country made this statement: \"{statement}\"\n"
        f"Country took this action: \"{action}\"\n"
        "Based on the statement and action, is the statement TRUE, FALSE, or MISLEADING? "
        "Explain briefly."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# 4. Main flow
if __name__ == "__main__":
    pairs = fetch_statement_action_pairs(db_path="output_database.db", table_name="country_statements")

    for i, (statement, action) in enumerate(pairs, start=1):
        print(f"\nPair {i}:")
        print(f"Statement: {statement}")
        print(f"Action: {action}")
        evaluation = evaluate_truthfulness(statement, action)
        print(f"GPT Evaluation:\n{evaluation}")
