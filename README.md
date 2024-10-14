# EnglishAI

這個程式是使用大型語言模型的API，並將提示詞使用sqlite儲存，以便日後儲存對話紀錄


### 檔案結構

```bash
├───main
│   ├───database
│       └───example.db
│   ├───eng_ai.py
│   ├───env_settings.py
│   └───model.py
│
```

### 環境配置

運行程式時會需要使用到：langchain, langchain-groq, nanoid, sqlalchemy，須事先安裝

以下環境確定可以運行：
```poetry
python = "^3.12"
langchain = "^0.3.1"
langchain-groq = "^0.2.0"
nanoid = "^2.0.0"
sqlalchemy = "^2.0.35"
```


### 取得Groq api key

Groq是生產AI加速硬體的公司，專門製作推理晶片，有提供免費的API來跑一些開源模型，而且速度非常快

到[Groq](https://console.groq.com/keys)註冊登入後即可取得 Api key。

也可自行換成openai、google等其他公司的模型，也可使用本地模型，只要有LangChain支援的都可以



### 修改配置文件

`env_settings.py`:

```Python
# 將Api key輸入在這裡
GROQ_API_KEY = 'your_api_key'

# 儲存對話紀錄的檔案路徑
db_path = 'sqlite:///database/english_correcting.db'

# 可自行切換模型種類
model_name = "llama-3.1-70b-versatile"
```

可以查看Groq Api支援哪些[模型](https://console.groq.com/docs/models)。



### 新增對話紀錄(可選)
如果想跳過這裡，可以在env.settings.py裡讓db_path使用example.db，這是先前創建的資料庫

到`model.py`裡的`creat()` 輸入想要的提示詞；ChatLog裡等於是對話紀錄，可以在創建時就讓模型知道你的資訊。

```Python
def create():
    
    ...

    # 修改這裡設定你的人設
    session.add(ChatLog(
        nano_id=generate(), 
        question="我是ＯＯＯ，我愛爆肝寫程式", 
        answer="收到，你好，我是烏薩奇，你最得意的助手。"
    ))
    ...
```

也可以修改`ChatLogSystem`的部分，讓模型成為其他方面的角色。



### 開始使用

執行`eng_ai.py`後即可與模型開始對話
![截圖 2024-10-14 上午10 18 26](https://github.com/user-attachments/assets/b950e3e8-3a95-4173-ab91-48dd80466c11)

#### 額外指令
`save_conversation` ： 在對話時輸入 `save_conversation` 可將對話儲存至 db_path

`quit` ： 儲存對話紀錄並離開對話



## Reference

[Day 03 - 讓語言模型有記憶 - 連續對話 _ 初探 Langchain 與 LLM：打造簡易問診機器人系列 第 3 篇](https://ithelp.ithome.com.tw/articles/10352230)
