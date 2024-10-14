from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from nanoid import generate
from env_settings import db_path

# 定義模型
Base = declarative_base()


class ChatLogSystem(Base):
    __tablename__ = 'chat_system_message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nano_id = Column(String)
    system_message = Column(String)
    extend_existing = True

class ChatLog(Base):
    __tablename__ = 'chat_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nano_id = Column(String)
    question = Column(String)
    answer = Column(Integer)
    extend_existing = True


def create():
    Base.metadata.create_all(engine)

    session.add(ChatLogSystem(
        nano_id = generate(),
        system_message = """
                你是一個繁體中文機器人，會理解使用者的提問並使用繁體中文回答。
                並且會隨時注意我的英文文法，如果發現任何文法錯誤及時給出修正。
                """
    ))

    session.add(ChatLog(
        nano_id=generate(), 
        question="我是Joloan，一名資料分析師，就讀哈爾濱佛學院，目前居住於加拿大的多倫多", 
        answer="收到，你好，我是烏薩奇，你最得意的助手。"
    ))

    session.commit()

def check(table = 'log'):
    if table == 'log':
        students = session.query(ChatLog).all()
        for student in students:
            print(f"id: {student.id}")
            print(f"nanoid: {student.nano_id}")
            print(f"q: {student.question}")
            print(f"a: {student.answer}")
            print("===========================")
    
    elif table == 'sys_log':
        students = session.query(ChatLogSystem).all()
        for student in students:
            print(f"id: {student.id}")
            print(f"nanoid: {student.nano_id}")
            print(f"SystemMessage: {student.system_message}")
            print("===========================")


if __name__ == '__main__':
    engine = create_engine(db_path, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    create()
    # check(table='log')



    

