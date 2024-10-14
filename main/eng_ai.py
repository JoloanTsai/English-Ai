from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from model import ChatLog, ChatLogSystem
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from env_settings import env_init, db_path, model_name
from langchain_groq import ChatGroq
from nanoid import generate
import os

env_init()

llm = ChatGroq(
    groq_api_key = os.environ.get("GROQ_API_KEY"),
    model=model_name
)
engine = create_engine(db_path, echo=True)
session = sessionmaker(bind=engine)()
chat_logs = session.execute(select(ChatLog)).scalars().all()
chat_logs_sys = session.execute(select(ChatLogSystem)).scalars().all()

print(chat_logs_sys[0].system_message)

def messages_in(sys_logs, logs) -> list:
    messages_local = []
    for sys_m in sys_logs:
        messages_local.append(SystemMessage(content=sys_m.system_message))
    for chat_log in logs:
        messages_local.append(HumanMessage(content=chat_log.question))
        messages_local.append(AIMessage(content=chat_log.answer))

    return messages_local

messages = messages_in(chat_logs_sys, chat_logs)

def conversation(your_question: str):
    messages.append(HumanMessage(content=your_question))
    ai_message = llm.invoke(messages)
    messages.append(AIMessage(content=ai_message.content))
    print(ai_message.content)


class UseCommands():
    def __init__(self):
        pass

    def history(self):
        print(messages)

    def hello(self):
        print("Hello!")

    def save_conversation(self):
        try:
            def get_new_chat_for_chatlog(different_messages) -> list:
                new_chat = []
                for message in different_messages :
                    if isinstance(message, SystemMessage):
                        new_chat.append(ChatLogSystem(nano_id = generate(), system_message = message.content))
                        different_messages.remove(message)

                for i in range(0, len(different_messages), 2):
                    new_chat.append(ChatLog(
                        nano_id=generate(), 
                        question=different_messages[i].content, 
                        answer=different_messages[i+1].content
                    ))

                return new_chat

            original_messages = messages_in(chat_logs_sys, chat_logs)
            different_messages = [x for x in messages if x not in original_messages]

            new_chat = get_new_chat_for_chatlog(different_messages)
            session.add_all(new_chat)
            session.commit()
            print(f"\n成功儲存對話！  ({db_path})")
        except : 
                print("儲存失敗！！ Erorr! \nSave Failed!")
        
    def quit(self):
        self.save_conversation()
        raise StopIteration

if __name__ == '__main__':
    print(f"\n\n\n\n\n\n我是幫你學習英文的AI，目前使用的模型是： {model_name} \n你可以傳入英文句子，我會給你修改成正確文法的建議")
    commands = UseCommands()
    commands_lib = [func for func in dir(UseCommands) if callable(getattr(UseCommands, func)) and not func.startswith("__")]
    print('commands_lib: ', commands_lib, end="\n\n ======================================== \n")

    while True :
        input_text = input("\nYou: ")

        if input_text not in commands_lib :
            print("\nEnglish AI: ", end="")
            conversation(input_text)
        else :
            excute_str = "commands." + input_text + "()"
            eval(excute_str)

        
