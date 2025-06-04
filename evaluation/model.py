import time
import openai


def get_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)


def eval_model(client, evaluator_model, system_prompt, main_prompt):
    # Generate a model response based on the system and main prompts.
    # This is a placeholder function. In a real implementation, this would call a model API.

    # please use this function if you want to use OpenAI model
    while True:
        try:
            response = client.chat.completions.create(
                model = evaluator_model,
                messages = [
                    # {"role": "system", "content": system_prompt},
                    {"role": "user", "content": main_prompt}
                ],
                temperature = 0,    # 0 for deterministic output
            )
            break
        except Exception as e:
            print(f"Error generating response: {e}")
            print("Retrying...")
            time.sleep(30)
            
    return response.choices[0].message.content