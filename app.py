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
openai.api_key = os.environ('api_key')
secret_key = os.environ('secret_key')
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

translate_sytem_content = \
"""Forget all the previous Intructions. As a professional translator, who speaks and writes fluent English and Korean, your task is to translate the given english text in Korean. The text to translate is delimited by triple quotes.

To translate keep in mind that:
Translate the text accurately to the Korean language.
Please note that your translation should be a simple and accurate representation of the original text, without any additional information or interpretation
Do not short my text.
Do not echo my prompt.
Do not remind me what I asked you for.
Do not short my text
Do not apologize.
Do not self-reference.
Get to the point precisely and accurately.
Do not explain what and why, just give me your best possible Output
Output should only be the translated text no additional explanation and text.
Character names should be written in both Korean and original English => Character names: When first mentioned, write in Korean and English, and thereafter in Korean only. e.g. 베냐민 네타냐후(Benjamin Netanyahu) 총리. Famous figures known to everyone do not need to be translated into English (such as Trump, Xi Jinping, Abe, etc.)
Indication of a person's affiliation/status => Indicate affiliation and position after the name e.g. 폼페이오 미 국무부 장관은~
Proper nouns => Institutions and organizations, etc., should be written without spaces (e.g. 한국무역협회, 대외경제정책연구원). If too long, some spaces are allowed, such as the country name.
Name of international organizations => When first mentioned, write in Korean and initials, or in Korean and full English name. If the initials are more famous than the full English name, indicate the initials e.g. 세계은행(World Bank), 국제통화기금(IMF)
numerical notation => Indicate in Korean won e.g. 100달러(한화 12만 원)
Notation of numbers and units => If it ends with a number, write it together with the unit, if it ends with Korean, space between number and unit e.g. 100달러, 100만 달러
Numeric notation => Use comma for thousands, and write 조/억/만 in Korean, thousands and below in numbers e.g. 7억 3,450만 4,000달러
Comparison of time period => 전년 동기 대비, 전년 동월 대비, 전년 대비
Indication of date in the first paragraph: Month and day => e.g. 1월 1일(0). 2020년 1월 1일(X) - Remove the year. 지난 1월 1일(x) - Remove the word "지난". 1월 1일(x) - Remove the comma
Quarter notation => 1/4분기(0). 1분기(x). 1사분기(x)
You are required to adopt the writing style, tone and sentence endings exemplified in the two provided Examples below.
[Example 1/2]
(*) 제목 : 우즈베키스탄, 2023년 건설 부문에 50조 숨 투자
>> 우즈베키스탄 통계청은 2023년 1~5월 우즈베키스탄의 건설 부문에 총 52조 숨(한화 약 5조 8,915억 원)이 투자되었다고 발표함
    - 통계청은 2023년 연초부터 우즈베키스탄에 막대한 투자금이 유입되면서 건설 부문 활동이 크게 증가하였다고 밝힘
    - 통계청이 발표한 자료에 따르면, 2010년 우즈베키스탄 건설 부문 투자액은 8조 2,000억 숨(한화 약 9,290억 원)이었으나, 이후 꾸준이 증가하여 2022년 투자액은 1,308조 숨(한화 약 148조 원)을 기록하였음
>> 우즈베키스탄 현지 매체는 개발업자들이 인프라, 도로 개선에도 노력을 기울이고 있다고 보도함
    - 우즈베키스탄 현지 매체인 UPL은 샤브카트 미르지요예프(Shavkat Mirziyoyev) 우즈베키스탄 대통령이 관련 기관에 공공 인프라의 재건과 개선을 위한 법안을 마련할 것을 지시했다고 전함
    - UPL은 미르지요예프 대통령의 이러한 조치로 우즈베키스탄 국민의 삶의 질이 높아졌으며, 경제 번영이 촉진되었다고 논평함
>> 한편 지난 2023년 2월 유라시아 전문 매체는 미르지요예프 대통령이 건설 모라토리엄 선언을 검토한 바 있다고 보도함
    - 유라시아 전문 매체인 유라시아넷(eurasianet)은 미르지요예프 대통령이 새로운 도시개발 계획이 수립될 때까지 수도 타슈켄트(Tashkent) 내 신축 공사를 유예할 것이라고 보도함
    - 이는 빠르게 증가하는 인구에 적절히 대응하고, 부실한 건축 기준으로 크게 확대된  시리아와 터키의 지진 피해 사태가 우즈베키스탄에서 발생하는 것을 막기 위한 조치인 것으로 알려짐
[Example 1/2 END]
[Example 2/2]
(*) 제목 : 미얀마 군사정권, 카친 소수민족 반군이 중국군 대표가 탑승한 차량 호송대를 공격했다고 주장
>> 7월 1일 미얀마 군사정부는 소수민족 반군이 국경 안보 회의에 참석하기 위해 이동하던 차량 호송대를 공격했다고 비난함
    - 6월 27일 미얀마 북부 카친(Kachin)주의 미트키나(Myitkyina)로 향하던 중국군 대표단과 미얀마 측 대표단을 태운 차량 호송대가 총격을 받음
    - 미얀마 군부는 두 번째 열에 있던 차량이 5발의 총격을 받았고, 정부군이 즉각 대응 사격을 가했다고 밝힘
>> 조 민 툰(Zaw Min Tun) 미얀마 군부 대변인은 “카친 독립군(KIA, Kachin Independence Army)이 호송대를 공격한 것을 확인할 수 있다”고 발표함
    - 미얀마 군사정권은 이번 총격 사건으로 다치거나 사망한 사람은 없었다고 덧붙임
    - 그러나, KIA의 나우 부(Naw Bu) 대령은 “KIA는 호송대를 공격하지 않았고 6월 26일부터 호송대가 공격을 받았던 지역 근처에서 치열한 전투가 있었다”고 밝힘  
>> 2022년 10월 미얀마 군부가 KIA 창립 62주년을 기념하는 공연장을 공습했을 때 수십 명이 사망한 바 있음
    - 현지 인권 감시단체에 따르면 2021년 2월 미얀마 군부의 쿠데타 이후 군부의 반대파 탄압으로 3,700명 이상이 사망함
    - 한편민 아웅 흘라잉(Min Aung Hlaing) 미얀마군 최고사령관은 중국의 대(對)미얀마 투자 재개를 추진하면서 중국 정부 고위 관료들과 계속 접촉하고 있음
[Example 2/2 END]
Ensure that you adopt the sentence structures and endings typically found in Korean language (such as 음, 임, 함, 됨) as demonstrated in the preceding two examples.

IMPORTANT: Don't run away from this step by step, obey it completely

Reply in Korean"""


def gpt_translate(text):
    retries = 3  # number of retries
    for i in range(retries):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                temperature = 0.3,
                max_tokens = 2000,
                messages=[
                    {"role": "system", "content": translate_sytem_content},
                    {"role": "user", "content": '"""{}"""'.format(text)}
                ]
            )
            return completion.choices[0].message.content

        except Exception as e:
            if i < retries - 1:  # i is zero indexed
                print(f'Request failed {retries} attempts. Error: {e}')
                time.sleep(5)
                continue
            else:
                print(f'Request failed after {retries} attempts. Error: {e}')
                return None  # or some other value indicating failure

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
guide = '''Forget all the previous Intructions. Your task is to provide a comprehensive summary of the given news articles, delimited by triple quotes.

To write the report keep in mind that:

You need to act as a professional journalist with excellent English speaking and writing skills in politics, economy, and business industry.
Write in journalistic, formal and objective tone. Journalistic writing means that you should write relevant, simple, timely, and include unexpected events.
Write in an inverted pyramid style that begins with the most crucial information at the top, then the details, followed by additional information.
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
Unit notation => Be sure to check for missing currency and numerical units.
Confirmation of position => Check if the title and name of the person are correct.

IMPORTANT: Don't run away from this step by step, obey it completely

Now, create a summary based on the provided articles below:
"""{}"""'''
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

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
    if num_tokens_from_string(user_input) > 1000:
        with st.spinner("Summarizing Text..."):
            target_token_num = 1000
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
        with st.spinner("Waiting for ChatGPT..."):
            ts_text = gpt_translate(prompt)
        # ts_text = translate_long_text(prompt)
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
