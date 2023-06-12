# ------------------------------------------------------------------- #
import streamlit as st
import openai
import os
import tiktoken
from gensim.summarization import summarize
# https://docs.streamlit.io/library/api-reference
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# streamlit run app.py
# openai.api_key = st.secrets["api_key"]
# os.environ["api_key"] == st.secrets["api_key"]
openai.organization = "org-cWYPb9h1vIjpstBy0y6td4Sj"
openai.api_key = os.getenv('api_key')
# os.environ[]
# ------------------------------------------------------------------- # 
# defs 
# ------------------------------------------------------------------- #
    # count words
def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model('curie')
    num_tokens = len(encoding.encode(string))
    return num_tokens


    # summarize
def textRank_summarize(text, ratio):
    # Summarize the text with TextRank
    summary = summarize(text, ratio=ratio)
    return summary

    # generate answer
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
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

models = {
    '파인튜닝_curie_513' : 'curie:ft-ec21rnc-2023-05-31-09-57-57',
    '파인튜닝_curie_1837' : 'curie:ft-ec21rnc-2023-06-07-06-37-34',
    '기본모델_GPT-4' : 'gpt-4'
}
guide = """Forget all the previous Intructions. As a professional journalist with exceptional English writing skills, your task is to provide a comprehensive summary of the given news articles. To accomplish this, you must first create a suitable title in a full sentence. Next, you must identify at least three main points from the articles. Your summary should cover all three of these main points, with each point accompanied by three explanatory sentences. It is essential that you present the main points and their corresponding explanations in a logical and chronological sequence, with a clear connection to the topic. Your summary must cover all aspects of the provided articles, and you should not include any information outside of the passage. Additionally, avoid repeating facts or writing similar sentences. Finally, your response should consist solely of the summary, without any supplementary commentary. When referring to numerical data, such as market size, growth, budget, or rate, be sure to use the provided index.
Now, create a summary based on the provided articles below:"""
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
    # Title
st.title(":robot_face: :blue[EC21R&C] SummaryGPT")
st.divider()
instructions = '''> 1. 기사입력창에 요약 대상 기사를 형식대로 붙혀 넣고, `토큰 수 계산` 버튼을 누른다.
> 2. 1500자 이상일 경우, 보다 정확한 결과를 위해 주제와 필요없는 문장, 문단 등을 지우고 다시 토큰수를 계산한다.
> 3. 문단을 지울 필요가 없다면, `Secret Key`, `GPT Model`, `Temperature`를 선택하고 `요약문 생성`을 클릭한다.

:warning: 반드시 `토큰수 계산` 버튼을 누르고 `요약문 생성`을 클릭
'''
st.subheader(':bulb: 사용법')
st.markdown(instructions)
st.divider()
    # pre-set
# st.header('토큰 수 계산')
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
placeholder = """[기사1 제목]
[기사1 내용]
[기사2 제목]
[기사2 내용]
...
"""

with st.form("form_count_tokens"):
    user_input = st.text_area("**Prompt (기사입력창)**", placeholder = placeholder, height = 500)
    user_input = user_input.replace('\n\n', ' ').replace('\n', ' ').strip()
    submit = st.form_submit_button(":moneybag: **토큰 수 계산** :moneybag:", use_container_width = True)
    

if submit and user_input:
    with st.spinner("calculating tokens..."):
        token_num = num_tokens_from_string(user_input)
    st.subheader( '토큰수 : ' + str(token_num) + ' tokens' )
    st.caption('_1500 토큰을 넘어가면 기사가 자동으로 요약되어서 GPT에 입력됩니다_')

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #


# with st.form("form_summarize"):
    
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
with st.form("form_gpt"):
        # secret key
    secret_key = st.text_input(':secret: **Secret Key**', placeholder = '힌트 : 와이파이 비밀번호')
        # model selection
    model = st.selectbox("**GPT Model 선택**", ["파인튜닝_curie_1837", "파인튜닝_curie_513"])
        # temperature
    temperature = st.selectbox("**Temperature**", ["0.5", "0", "0.3", "0.7", "1"])    
    st.caption('→ _낮을수록 정형화된 답변 생성, 높을수록 자유롭게 문장을 생성_')
    submit_summary = st.form_submit_button(":printer: **요약문 생성** :printer:", use_container_width = True)
    # with st.form("form"):

if secret_key == 'movefast' and submit_summary and user_input:
    user_input = user_input.replace('\n\n', ' ').replace('\n', ' ').strip()
    if num_tokens_from_string(user_input) > 1200:
        with st.spinner("Summarizing Text..."):
            target_token_num = 1200
            ratio = target_token_num / num_tokens_from_string(user_input)
            ratio = round(ratio, ndigits=1)

            while True:
                # Summarize the text
                summary = textRank_summarize(user_input, ratio)
                summary_tokens = num_tokens_from_string(summary)

                # If the summary is short enough, stop here
                if summary_tokens <= target_token_num:
                    break

                # Otherwise, reduce the ratio and try again
                ratio -= 0.1

            user_input = summary
    with st.spinner("Waiting for ChatGPT..."):
        user_input = guide + '\n' + user_input
        prompt = generate_answer(user_input, models.get(model), float(temperature))
    st.write(prompt.replace('Title:', '').replace('(*)', '##').replace('>>', '###') )
else:
    st.write('`Secret Key`를 입력하세요')
    
# to-do
# 사업별 섹션 나누기
# 토큰수 카운트 만들기
# summarize 만들기