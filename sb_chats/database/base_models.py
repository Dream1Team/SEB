from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class ChatsModel(Base):
    __tablename__ = 'chats'

    name: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default='private', index=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # ✅ УБИРАЕМ это явное отношение
    # chat_members: Mapped[List['ChatMemberModel']] = relationship(back_populates='chat')

    messages: Mapped[List['MessagesModel']] = relationship(
        back_populates='chat',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )


class MessagesModel(Base):
    __tablename__ = 'messages'

    content: Mapped[str] = mapped_column(Text)
    sender_id: Mapped[int] = mapped_column()
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'))
    message_type: Mapped[str] = mapped_column(String(50), default='text', nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default='false')
    read_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    chat: Mapped['ChatsModel'] = relationship(back_populates='messages')


class ChatMemberModel(Base):
    __tablename__ = 'chat_members'

    chat_id: Mapped[int] = mapped_column(
        ForeignKey('chats.id', ondelete='CASCADE'),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="ID пользователя из внешнего сервиса"
    )

    # ✅ Используем backref - он автоматически создаст отношение в ChatsModel
    chat: Mapped['ChatsModel'] = relationship(backref='chat_members')