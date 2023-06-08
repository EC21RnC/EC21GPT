import streamlit as st
import openai

# https://docs.streamlit.io/library/api-reference
# streamlit run app.py

openai.api_key = st.secrets["api_key"]

def generate_answer(input_text, ft_model, temperature):
    # Code to access the GPT-3 API and generate a summary
    completions = openai.Completion.create(
        model = ft_model,
        prompt = input_text + '\n\n###\n\n',
        max_tokens = 500,
        stop = ' END',
        temperature = temperature,
        n = 1
    )
    message = completions.choices[0].text
    return message

models = {
    '파인튜닝_curie_513' : 'curie:ft-ec21rnc-2023-05-31-09-57-57',
    '파인튜닝_curie_1837' : 'curie:ft-ec21rnc-2023-06-07-06-37-34',
    '기본모델_GPT-4' : 'gpt-4'
}

guide = """Forget all the previous Intructions. As a professional journalist with exceptional English writing skills, your task is to provide a comprehensive summary of the given news articles. To accomplish this, you must first create a suitable title in a full sentence. Next, you must identify at least three main points from the articles. Your summary should cover all three of these main points, with each point accompanied by three explanatory sentences. It is essential that you present the main points and their corresponding explanations in a logical and chronological sequence, with a clear connection to the topic. Your summary must cover all aspects of the provided articles, and you should not include any information outside of the passage. Additionally, avoid repeating facts or writing similar sentences. Finally, your response should consist solely of the summary, without any supplementary commentary. When referring to numerical data, such as market size, growth, budget, or rate, be sure to use the provided index.
Now, create a summary based on the provided articles below:"""

#
#
#
st.title("EC21R&C SummaryGPT-v4")

with st.form("form"):
    user_input = st.text_area("Prompt")
    model = st.selectbox("GPT Model", ["파인튜닝_curie_1837", "기본모델_GPT-4", "파인튜닝_curie_513"])
    temperature = st.selectbox("temperature", ["0.5", "0", "0.3", "0.7", "1"])
    submit = st.form_submit_button("Submit")

if submit and user_input:
    with st.spinner("Waiting for ChatGPT..."):
        user_input = guide + '\n' + user_input
        prompt = generate_answer(user_input, models.get(model), float(temperature))
    st.write(prompt.replace('Title:', '').replace('(*)', '#').replace('>>', '##') )
    
    
# to-do
# 사업별 섹션 나누기
# 토큰수 카운트 만들기
# summarize 만들기