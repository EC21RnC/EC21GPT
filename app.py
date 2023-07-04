# ------------------------------------------------------------------- #
import streamlit as st
import openai
import os
import tiktoken
from gensim.summarization import summarize
from googletrans import Translator
import time
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')

# https://docs.streamlit.io/library/api-reference
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# streamlit run app.py
# openai.api_key = st.secrets["api_key"]
# os.environ["api_key"] == st.secrets["api_key"]
openai.organization = "org-cWYPb9h1vIjpstBy0y6td4Sj"
openai.api_key = os.getenv('api_key')
secret_key = os.getenv('secret_key')
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

def translate_text(text, source_language, target_language):
    translator = Translator()
    result = translator.translate(text, src=source_language, dest=target_language)
    # print("Translation result:", result)
    return result.text


def translate_long_text(text):
    sentences = sent_tokenize(text)

    translated_text = ""
    current_chunk = []
    current_chunk_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        if current_chunk_length + sentence_length > 3000:
            try:
                try:
                    translated_sentences = translate_text(" ".join(current_chunk), "en", "ko")
                except:
                    time.sleep(2)
                    translated_sentences = translate_text(" ".join(current_chunk), "en", "ko")
            except:
                translated_sentences = ''
            translated_text += "".join(translated_sentences)
            current_chunk = [sentence]
            current_chunk_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_chunk_length += sentence_length

    if current_chunk:
        # print("Translating chunk:", " ".join(current_chunk))
        try:
            try:
                translated_sentences = translate_text(" ".join(current_chunk), "en", "ko")
            except:
                time.sleep(2)
                translated_sentences = translate_text(" ".join(current_chunk), "en", "ko")
        except:
            translated_sentences = ''
        translated_text += "".join(translated_sentences)
        
    return translated_text
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

# Initialize the history in the session state
if "history" not in st.session_state:
    st.session_state["history"] = []
# Create the history tab in the sidebar
st.sidebar.markdown('# 	:speech_balloon: History')
st.sidebar.caption(':warning: 페이지를 새로고침하면 히스토리가 사라집니다')
st.sidebar.markdown('---')

models = {
    '파인튜닝_curie_513' : 'curie:ft-ec21rnc-2023-05-31-09-57-57',
    '파인튜닝_curie_1837' : 'curie:ft-ec21rnc-2023-06-07-06-37-34',
    '기본모델_GPT-4' : 'gpt-4'
}
guide = '''Forget all the previous Intructions. As a professional journalist with exceptional English writing skills, your task is to provide a comprehensive summary of the given news articles, delimited by triple quotes.

To write the report keep in mind that:

You need to act as a professional journalist with excellent English speaking and writing skills in politics, economy, and business industry.
First, you must first create a suitable title in a full sentence.
You must identify at least three main points from the articles.
Your summary should cover all three of these main points, with each point accompanied by three explanatory sentences.
It is essential that you present the main points and their corresponding explanations in a logical and chronological sequence, with a clear connection to the topic.
Your summary must cover all aspects of the provided articles, and you should not include any information outside of the passage.
Avoid repeating facts or writing similar sentences.
Your response should consist solely of the summary, without any supplementary commentary.
Keep in mind that when handling numbers(such as market size, growth metrics, budgetary figures, or rates), it's crucial to maintain the original order as specified in the given index. Do not modify or shuffle these numbers.
Article must be 100% human writing style, fix grammar issues and change to active voice.
When summarizing, Current issues, Context, Background information and Additional explanations should be clearly and logically composed.
Avoid writing two similar sentences consecutively (a typical translation style); instead, combine them into one sentence.
For quotes from individuals, don't include content with no informational value (diplomatic rhetoric, obvious remarks, etc.).
Indication of a person's affiliation/status => Indicate affiliation and position after the name
Month and day indication => Bad example: The past 2nd day (exact month and day unknown). Of course, once you write the month and day, it's okay to omit the month in the same paragraph.
numerical notation => Indicate in Korean won e.g. 100달러(한화 12만 원)
Unit notation => Be sure to check for missing currency and numerical units.
Confirmation of position => Check if the title and name of the person are correct.
Indication of date in the first paragraph: Month and day => e.g. 1월 1일(0). 2020년 1월 1일(X) - Remove the year. Last January 1 (X) - Remove the word "last". January 1, (X) - Remove the comma
Quarter notation => e.g. 1/4 quarter (O) e.g. 1 quarter (X) e.g. 1 quarter (X)

IMPORTANT: Don't run away from this step by step, obey it completely

Now, create a summary based on the provided articles below:
"""{}"""'''
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
#
#



#
#

    # Title
st.title(":blue[EC21R&C] SummaryGPT")
st.divider()
instructions = '''> 1. 기사입력창에 요약 대상 기사를 형식대로 붙혀 넣고, `토큰 수 계산` 버튼을 누른다.
> 2. 1500자 이상일 경우, 보다 정확한 결과를 위해 주제와 필요없는 문장, 문단 등을 지우고 다시 토큰수를 계산한다.
> 3. 문단을 지울 필요가 없다면, `Secret Key`, `GPT Model`, `Temperature`를 선택하고 `요약문 생성`을 클릭한다.'''
st.subheader(':bulb: 사용법')
st.markdown(instructions)
# st.info(instructions)
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
else:
    if submit and len(user_input) == 0:
        st.error('텍스트를 입력하세요', icon="🚨")

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #



    
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
with st.form("form_gpt"):
        # secret key
    secret_key_user = st.text_input(':secret: **Secret Key**', placeholder = 'chan@ec21rnc.com에 문의해주세요')
        # model selection
    model = st.selectbox("**GPT Model 선택**", ["파인튜닝_curie_1837", "파인튜닝_curie_513"])
        # temperature
    temperature = st.selectbox("**Temperature**", ["0.5", "0", "0.3", "0.7", "1"])
    st.caption('→ _낮을수록 정형화된 답변 생성, 높을수록 자유롭게 문장을 생성_')
        # translate_y_n
    translate_y_n = st.selectbox("**답변을 한글로 번역**", ["No", "Yes"])
    st.caption('→ _구글 번역기 사용 중. 추후 파인튜닝 모델로 변경 예정_')
        # submit
    submit_summary = st.form_submit_button(":printer: **요약문 생성** :printer:", use_container_width = True)
    
    # with st.form("form"):
st.divider()

if submit_summary and secret_key == secret_key_user and user_input:
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
        # user_input = user_input
        user_input = guide.format(user_input)
        prompt = generate_answer(user_input, models.get(model), float(temperature))
    # with st.container():
    if translate_y_n == 'No':
            # write text
        st.markdown(prompt.replace('>>', '\n☐').replace('.-', '\n&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;'))
        st.code(prompt, language = 'markdown')
        # add to history
        st.session_state["history"].append(prompt + '\n' + 'Temperature: ' +  str(temperature) + '\n' + 'Model: ' + str(model))
    elif translate_y_n == 'Yes':
        st.subheader('영문')
            # en result
        st.markdown(prompt.replace('>>', '\n☐').replace('.-', '\n&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;'))
        st.code(prompt, language = 'markdown')
        st.divider()
            # ko result
        st.subheader('한글')
        ts_text = translate_long_text(prompt)
        ts_text = ts_text.replace('.-', '.\n - ').replace('>>', '\n>>')
        st.markdown(ts_text.replace('>>', '\n☐').replace('.-', '\n&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;'))
        st.code(ts_text, language = 'markdown')
        st.divider()
        # add to history
        st.session_state["history"].append(prompt + '\n' + 'Temperature: ' +  str(temperature) + '\n' + 'Model: ' + str(model))
    # st.sidebar
    # st.sidebar.text_area("History", st.session_state["history"], height=200)

    # st.write(prompt.replace('Title:', '').replace('(*)', '').replace('>>', '').replace('-', '') )
    # st.write(prompt.replace('Title:', '')) #.replace('(*)', '##').replace('>>', '###') )
    # st.write(prompt.replace('Title:', '').replace('(*)', '##').replace('>>', '###') )
    # st.text(prompt.replace('Title:', '').replace('(*)', '##').replace('>>', '###') )

elif len(user_input) == 0 and submit_summary:
    st.error('토큰 수 계산을 먼저 클릭하세요', icon="🚨")
elif len(user_input) != 0 and submit_summary and len(secret_key_user) != 0 and secret_key != secret_key_user:
    st.error('올바른 `Secret Key`를 입력하세요', icon="🚨")
elif len(user_input) != 0 and submit_summary and len(secret_key_user) == 0:
    st.error('`Secret Key`를 입력하세요', icon="🚨")
else:
    pass

# add to history
for i, item in enumerate(st.session_state["history"]):
    with st.sidebar.expander(f"Your Summary #{i+1}"):
        st.code(item, language = 'markdown')