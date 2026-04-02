import asyncio
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import EncryptionService
from database.base_models import ChatsModel, MessagesModel
from database.dao import BaseDAO
from database.db_manager import connection

encrypt = EncryptionService()

class ChatsDAO(BaseDAO):
    model = ChatsModel


def get_messages(messages: tuple[MessagesModel] | Sequence[MessagesModel]) -> list:
    chats_dict = {}

    for cur_msg in messages:
        chat_id = cur_msg.chat_id

        # Если чата еще нет в словаре, создаем его
        if chat_id not in chats_dict:
            chats_dict[chat_id] = {
                'chat': {
                    'chat_id': chat_id,
                    'messages': []
                }
            }

        # Добавляем сообщение в соответствующий чат
        chats_dict[chat_id]['chat']['messages'].append({
            'sender_id': cur_msg.sender_id,
            'content': encrypt.decrypt_from_string(str(cur_msg.content))
        })

    # Возвращаем список словарей (по одному на каждый чат)
    return list(chats_dict.values())


class MessagesDAO(BaseDAO):
    model = MessagesModel

    @classmethod
    async def add_entry(cls, session: AsyncSession = None, **values):
        """Добавление зашифрованного сообщения"""


        if 'content' not in values:
            raise ValueError("Content is required")

        plaintext = values['content']

        encrypted_content = encrypt.encrypt_to_string(plaintext)

        values['content'] = encrypted_content

        new_entry = cls.model(**values)

        try:
            session.add(instance=new_entry)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return new_entry

    @classmethod
    async def get_msgs_by_chat(cls, chat_id: int, session: AsyncSession = None):
        """Шаблон для получения конкретной записи из таблицы"""
        transaction = select(cls.model).where(cls.model.chat_id == chat_id)

        result = await session.execute(transaction)

        return result.scalars().all()


class DBChats:
    @connection
    async def get_all_chats(self, session: AsyncSession = None):
        result = await ChatsDAO.get_all_entries(session=session)
        return result

    @connection
    async def get_chat_by_id(self, _id: int, session: AsyncSession = None):
        result = await ChatsDAO.get_entry(_id=_id, session=session)
        return result

    @connection
    async def create_chat(self, session: AsyncSession = None, **values):
        result = await ChatsDAO.add_entry(session=session, **values)
        return result

    @connection
    async def edit_chat(self, _id: int, session: AsyncSession = None, **values):
        result = await ChatsDAO.edit_entry(_id=_id, session=session, **values)
        return result

    @connection
    async def delete_chat(self, _id: int, session: AsyncSession = None):
        result = await ChatsDAO.del_entry(_id=_id, session=session)
        return result


class DBMessages:
    @connection
    async def get_all_messages(self, session: AsyncSession = None):
        result = await MessagesDAO.get_all_entries(session=session)

        all_msgs = get_messages(result)

        return all_msgs

    @connection
    async def get_messages_by_chat_id(self, chat_id: int, session: AsyncSession = None):
        result = await MessagesDAO.get_msgs_by_chat(chat_id=chat_id, session=session)

        all_msgs = get_messages(result)

        return all_msgs

    @connection
    async def get_message_by_id(self, _id: int, session: AsyncSession = None):
        result = await MessagesDAO.get_entry(_id=_id, session=session)
        return result

    @connection
    async def create_message(self, session: AsyncSession = None, **values):
        result = await MessagesDAO.add_entry(session=session, **values)
        return result

    @connection
    async def edit_message(self, _id: int, session: AsyncSession = None, **values):
        result = await MessagesDAO.edit_entry(_id=_id, session=session, **values)
        return result

    @connection
    async def delete_message(self, _id: int, session: AsyncSession = None):
        result = await MessagesDAO.del_entry(_id=_id, session=session)
        return result


db_chat = DBChats()
db_msg = DBMessages()


if __name__ == "__main__":
    # gotten_messages = asyncio.run(db_msg.get_messages_by_chat_id(chat_id=2))
    # print(asyncio.run(db_msg.create_message(content='Hi, Chuvi!',
    #                                         chat_id=2,
    #                                         message_type='private',
    #                                         sender_id=2,
    #                                         is_read=False)))

    msgs = asyncio.run(db_msg.get_messages_by_chat_id(2))

    for msg in msgs:
        for ms in msg['chat']['messages']:
            print(ms['content'])
            print(ms['sender_id'])


    # for msg in gotten_messages:
    #     print(encrypt.decrypt_from_string(str(msg.content)))
