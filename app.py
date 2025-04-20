import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 現在のファイルのディレクトリパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# .envファイルへのパスを構築
env_path = os.path.join(current_dir, '.env')

# パスを明示して.envファイルをリロード
load_dotenv(dotenv_path=env_path, override=True)

# APIキーが環境変数にない場合はエラーメッセージを表示
if "OPENAI_API_KEY" not in os.environ:
    st.error("環境変数 'OPENAI_API_KEY' が設定されていません。.env ファイルを確認してください。")
    st.stop()

st.title("Chapter 6 【提出課題】LLM機能を搭載したWebアプリを開発しよう")
st.write("##### 動作モード1: 食生活に関する専門家への質問")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで、ダイエット目指す人に適切な食生活のアドバイスをします。")
st.write("##### 動作モード2: 筋トレに関する専門家への質問")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで、ダイエット目指す人に適切な筋トレ法のアドバイスをします。")

selected_item = st.radio(
    "専門家を選んでください",
    ["食生活に関する専門家への質問", "筋トレに関する専門家への質問"]
)

if selected_item == "食生活に関する専門家への質問":
    input_message = st.text_input(label="アドバイスを求める食生活に関する質問を入力してください。")
elif selected_item == "筋トレに関する専門家への質問":
    input_message = st.text_input(label="アドバイスを求める筋トレに関する質問を入力してください。")

st.divider()

if st.button("実行"):
    st.divider()
    
    if not input_message:
        st.warning("質問を入力してください。")
    else:
        # プレースホルダーを作成
        result_placeholder = st.empty()
        result_placeholder.info("AIが回答を生成中です...")
        
        # プログレスバーを表示
        progress_bar = st.progress(0)
        
        # OpenAI APIリクエストの前に少しプログレスバーを進める
        for i in range(30):
            time.sleep(0.05)
            progress_bar.progress(i)
        
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        
        try:
            # APIリクエストの準備中
            progress_bar.progress(35)
            time.sleep(0.2)
            
            if selected_item == "食生活に関する専門家への質問":
                system_message = "あなたは食生活の専門家です。"
            else:
                system_message = "あなたは筋トレの専門家です。"
            
            # APIリクエスト送信前
            progress_bar.progress(40)
            time.sleep(0.3)
            
            # APIリクエスト開始
            first_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": input_message},
                ],
                temperature=0.5
            )
            
            # APIからレスポンスを受け取った状態
            progress_bar.progress(80)
            time.sleep(0.2)
            
            # 結果の処理
            progress_bar.progress(90)
            time.sleep(0.1)
            
            # 完了
            progress_bar.progress(100)
            time.sleep(0.2)
            
            # プレースホルダーをクリアして結果を表示
            result_placeholder.empty()
            st.write("### 回答")
            st.write(first_completion.choices[0].message.content)
            
        except Exception as e:
            result_placeholder.error(f"エラーが発生しました: {e}")
        finally:
            # 少し待ってからプログレスバーを削除
            time.sleep(0.5)
            progress_bar.empty()