import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage,HumanMessage
import streamlit as st

# 環境変数の読み込み
load_dotenv()

# LLMの初期化
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# LLMにプロンプトを渡して回答を取得する関数
def get_llm_response(input_text, selected_expert):
    if selected_expert == "犬猫の専門家":
        system_message = "あなたは犬猫の飼育についての専門家です。以下の質問に答えてください。"
    else:
        system_message = "あなたは鳥の飼育についての専門家です。以下の質問に答えてください。"

    prompt = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text)
    ]
    response = llm(prompt)
    # 応答をデコードして文字化けを防ぐ
    if isinstance(response, bytes):
        try:
            response = response.decode("utf-8")
        except UnicodeDecodeError:
            response = response.decode("shift_jis", errors="replace")
    return response

# Webアプリの概要と操作方法を表示
st.title("ペット飼育専門家に質問できるWebアプリ")
st.write("このアプリでは、犬猫または鳥の専門家に質問を投げかけ、回答を得ることができます。\nラジオボタンで専門家を選択し、入力フォームに質問を入力してください。")

# ラジオボタンで専門家を選択
selected_item = st.radio(
    "どちらに質問しますか？",
    ["犬猫の専門家", "鳥の専門家"]
)

# 入力フォーム
input_text = st.text_input(label="質問を入力してください:")

# 送信ボタン
if st.button("送信"):
    if input_text:
        # LLMからの回答を取得
        response = get_llm_response(input_text, selected_item)
        # 回答を表示
        st.write("回答:")
        st.write(response.content)
    else:
        st.write("質問を入力してください。")