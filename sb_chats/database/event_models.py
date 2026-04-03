# import uuid
# from datetime import datetime
# from typing import List, Optional, Dict, Any
#
# from sqlalchemy import String, Boolean, JSON, Integer, DateTime, ForeignKey, Text, BigInteger, Index
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.sql import func
#
# from database.base_models import Base
# from database.enums import EventType, ChatType, MemberRole, MessageType
#
#
#
# class ChatEventModel(Base):
#     """
#     Модель для хранения событий чата.
#     События публикуются в Kafka и сохраняются локально для восстановления
#     """
#     __tablename__ = "chat_events"
#
#     event_id: Mapped[str] = mapped_column(String(36),
#                                           unique=True,
#                                           nullable=False,
#                                           default=lambda: str(uuid.uuid4()))
#
#     event_type: Mapped[EventType] = mapped_column(String(50),
#                                                   nullable=False,
#                                                   index=True)
#
#     aggregate_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
#     aggregate_type: Mapped[str] = mapped_column(String(50), nullable=False)
#     event_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
#     meta_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
#     version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
#     is_published: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
#     published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#     initiated_by_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
#
#     __table_args__ = (
#         Index('ix_chat_events_aggregate', 'aggregate_type', 'aggregate_id'),
#         Index('ix_chat_events_published', 'is_published', 'created_at')
#     )
#
#     @classmethod
#     def create_chat_event(
#             cls,
#             event_type: EventType,
#             aggregate_id: int,
#             aggregate_type: str,
#             event_data: Dict[str, Any],
#             initiated_by_user_id: Optional[int] = None,
#             metadata: Optional[Dict[str, Any]] = None
#     ) -> 'ChatEventModel':
#         """Создать новое событие"""
#         return cls(
#             event_type=event_type.value if isinstance(event_type, EventType) else event_type,
#             aggregate_id=aggregate_id,
#             aggregate_type=aggregate_type,
#             event_data=event_data,
#             initiated_by_user_id=initiated_by_user_id,
#             metadata=metadata or {}
#         )
#
#
# class ChatSnapshotModel(Base):
#     """Снапшоты состояния чата для оптимизации восстановления"""
#     __tablename__ = "chat_snapshots"
#
#     chat_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
#
#     # Текущее состояние чата
#     snapshot_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
#
#     # Последнее временное событие
#     last_event_id: Mapped[str] = mapped_column(String(36), nullable=True)
#     last_event_version: Mapped[int] = mapped_column(Integer, nullable=True)
#
#     # Когда был сделан снапшот
#     snapshot_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         nullable=False
#     )
#
#
# class ChatStateModel(Base):
#     """
#     Модель состояния чата (Projection/Read Model).
#     """
#     __tablename__ = "chat_states"
#
#     # Основная информация
#     name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
#     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     chat_type: Mapped[ChatType] = mapped_column(String(50), nullable=False, default=ChatType.PRIVATE)
#
#     # Владелец (из внешнего сервиса)
#     created_by_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
#
#     # Метаданные
#     avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
#
#     # Настройки
#     settings: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
#
#     # Статистика (вычисляется из событий)
#     member_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
#     message_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
#     last_message_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#
#     # Версия состояния (для optimistic locking)
#     version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
#
#     # Индексы
#     __table_args__ = (
#         Index('ix_chat_states_type_active', 'chat_type', 'is_active'),
#         Index('ix_chat_states_last_message', 'last_message_at'),
#     )
#
#     # Связи с другими состояниями
#     members: Mapped[List['ChatMemberStateModel']] = relationship(
#         'ChatMemberStateModel',
#         back_populates='chat',
#         cascade='all, delete-orphan',
#         lazy='select'
#     )
#
#     # Метод для обновления состояния на основе события
#     def apply_event(self, event: Dict[str, Any]) -> None:
#         """Применить событие к состоянию"""
#         event_type = event.get('event_type')
#
#         if event_type == EventType.CHAT_CREATED:
#             self._apply_chat_created(event)
#         elif event_type == EventType.CHAT_UPDATED:
#             self._apply_chat_updated(event)
#         elif event_type == EventType.MEMBER_ADDED:
#             self._apply_member_added(event)
#         elif event_type == EventType.MEMBER_REMOVED:
#             self._apply_member_removed(event)
#         elif event_type == EventType.MESSAGE_SENT:
#             self._apply_message_sent(event)
#
#         self.version += 1
#
#     def _apply_chat_created(self, event: Dict[str, Any]) -> None:
#         """Применить событие создания чата"""
#         data = event.get('event_data', {})
#         self.name = data.get('name')
#         self.description = data.get('description')
#         self.chat_type = ChatType(data.get('chat_type', 'private'))
#         self.created_by_user_id = data.get('created_by_user_id')
#         self.settings = data.get('settings', {})
#         self.is_active = True
#
#     def _apply_chat_updated(self, event: Dict[str, Any]) -> None:
#         """Применить событие обновления чата"""
#         data = event.get('event_data', {})
#         if 'name' in data:
#             self.name = data['name']
#         if 'description' in data:
#             self.description = data['description']
#         if 'settings' in data:
#             self.settings.update(data['settings'])
#
#     def _apply_member_added(self, event: Dict[str, Any]) -> None:
#         """Применить событие добавления участника"""
#         self.member_count += 1
#
#     def _apply_member_removed(self, event: Dict[str, Any]) -> None:
#         """Применить событие удаления участника"""
#         self.member_count = max(0, self.member_count - 1)
#
#     def _apply_message_sent(self, event: Dict[str, Any]) -> None:
#         """Применить событие отправки сообщения"""
#         self.message_count += 1
#         self.last_message_at = datetime.now()
#
#
# class ChatMemberStateModel(Base):
#     """
#     Состояние участника чата (Projection).
#     """
#     __tablename__ = "chat_member_states"
#     __table_args__ = (
#         # Уникальность комбинации чат-пользователь
#         Index('ix_chat_member_states_unique', 'chat_id', 'user_id', unique=True),
#     )
#
#     chat_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey('chat_states.id', ondelete='CASCADE'),
#         nullable=False,
#         index=True
#     )
#
#     user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
#
#     role: Mapped[MemberRole] = mapped_column(String(50), nullable=False, default=MemberRole.MEMBER)
#
#     joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
#     last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#
#     # Настройки
#     notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
#     is_muted: Mapped[bool] = mapped_column(Boolean, default=False)
#
#     # Последнее прочитанное сообщение (ID из событий)
#     last_read_message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#
#     # Связи
#     chat: Mapped['ChatStateModel'] = relationship('ChatStateModel', back_populates='members')
#
#     # Метод для обновления состояния
#     def update_from_event(self, event: Dict[str, Any]) -> None:
#         """Обновить состояние на основе события"""
#         event_type = event.get('event_type')
#         data = event.get('event_data', {})
#
#         if event_type == EventType.MEMBER_UPDATED:
#             if 'role' in data:
#                 self.role = MemberRole(data['role'])
#             if 'notifications_enabled' in data:
#                 self.notifications_enabled = data['notifications_enabled']
#             if 'is_muted' in data:
#                 self.is_muted = data['is_muted']
#
#         elif event_type == EventType.MESSAGE_READ:
#             self.last_seen_at = datetime.now()
#             self.last_read_message_id = data.get('message_id')
#
#
# class MessageStateModel(Base):
#     """
#     Состояние сообщения (Projection).
#     """
#     __tablename__ = "message_states"
#
#     # Идентификаторы
#     external_message_id: Mapped[str] = mapped_column(
#         String(36),
#         unique=True,
#         nullable=False,
#         index=True,
#         default=lambda: str(uuid.uuid4())
#     )
#
#     chat_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey('chat_states.id', ondelete='CASCADE'),
#         nullable=False,
#         index=True
#     )
#
#     sender_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
#
#     # Содержимое
#     content: Mapped[str] = mapped_column(Text, nullable=False)
#     message_type: Mapped[MessageType] = mapped_column(String(50), nullable=False, default=MessageType.TEXT)
#
#     # Статус
#     is_edited: Mapped[bool] = mapped_column(Boolean, default=False)
#     edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#
#     is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
#     deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#
#     # Медиа
#     media_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
#     media_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
#
#     # Для ответов
#     reply_to_message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#
#     # Метрики
#     read_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
#
#     # Версия
#     version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
#
#     # Индексы
#     __table_args__ = (
#         Index('ix_message_states_chat_created', 'chat_id', 'created_at'),
#         Index('ix_message_states_sender', 'sender_user_id', 'created_at'),
#     )
#
#     # Связи
#     chat: Mapped['ChatStateModel'] = relationship('ChatStateModel')
#
#     # Методы
#     def apply_event(self, event: Dict[str, Any]) -> None:
#         """Применить событие к состоянию сообщения"""
#         event_type = event.get('event_type')
#         data = event.get('event_data', {})
#
#         if event_type == EventType.MESSAGE_SENT:
#             self._apply_message_sent(data)
#         elif event_type == EventType.MESSAGE_UPDATED:
#             self._apply_message_updated(data)
#         elif event_type == EventType.MESSAGE_DELETED:
#             self._apply_message_deleted(data)
#         elif event_type == EventType.MESSAGE_READ:
#             self._apply_message_read()
#
#         self.version += 1
#
#     def _apply_message_sent(self, data: Dict[str, Any]) -> None:
#         """Применить событие отправки сообщения"""
#         self.content = data.get('content', '')
#         self.message_type = MessageType(data.get('message_type', 'text'))
#         self.sender_user_id = data.get('sender_user_id')
#         self.media_url = data.get('media_url')
#         self.media_type = data.get('media_type')
#         self.reply_to_message_id = data.get('reply_to_message_id')
#
#     def _apply_message_updated(self, data: Dict[str, Any]) -> None:
#         """Применить событие обновления сообщения"""
#         if 'content' in data:
#             self.content = data['content']
#             self.is_edited = True
#             self.edited_at = datetime.now()
#
#     def _apply_message_deleted(self, data: Dict[str, Any]) -> None:
#         """Применить событие удаления сообщения"""
#         self.is_deleted = True
#         self.deleted_at = datetime.now()
#
#     def _apply_message_read(self) -> None:
#         """Применить событие прочтения сообщения"""
#         self.read_count += 1
#
#
# # ==================== KAFKA EVENT SCHEMAS ====================
# class KafkaEventSchemas:
#     """
#     Схемы для событий Kafka между микросервисами.
#     """
#
#     @staticmethod
#     def chat_created_event(chat_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Создать событие 'чат создан' для Kafka"""
#         return {
#             "event_id": str(uuid.uuid4()),
#             "event_type": EventType.CHAT_CREATED.value,
#             "aggregate_id": chat_data["id"],
#             "aggregate_type": "chat",
#             "timestamp": datetime.now().isoformat(),
#             "data": {
#                 "chat_id": chat_data["id"],
#                 "name": chat_data.get("name"),
#                 "chat_type": chat_data.get("chat_type"),
#                 "created_by_user_id": chat_data["created_by_user_id"],
#                 "settings": chat_data.get("settings", {}),
#                 "member_ids": chat_data.get("member_ids", []),
#             },
#             "metadata": {
#                 "service": "chat-service",
#                 "version": "1.0",
#                 "initiated_by": chat_data.get("initiated_by_user_id"),
#             }
#         }
#
#     @staticmethod
#     def message_sent_event(message_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Создать событие 'сообщение отправлено' для Kafka"""
#         return {
#             "event_id": str(uuid.uuid4()),
#             "event_type": EventType.MESSAGE_SENT.value,
#             "aggregate_id": message_data["id"],
#             "aggregate_type": "message",
#             "timestamp": datetime.now().isoformat(),
#             "data": {
#                 "message_id": message_data["id"],
#                 "external_message_id": message_data.get("external_message_id"),
#                 "chat_id": message_data["chat_id"],
#                 "sender_user_id": message_data["sender_user_id"],
#                 "content": message_data["content"],
#                 "message_type": message_data.get("message_type", "text"),
#                 "media_url": message_data.get("media_url"),
#                 "reply_to_message_id": message_data.get("reply_to_message_id"),
#             },
#             "metadata": {
#                 "service": "chat-service",
#                 "version": "1.0",
#             }
#         }
#
#     @staticmethod
#     def member_added_event(
#             chat_id: int,
#             user_id: int,
#             added_by_user_id: Optional[int] = None
#     ) -> Dict[str, Any]:
#         """Создать событие 'участник добавлен' для Kafka"""
#         return {
#             "event_id": str(uuid.uuid4()),
#             "event_type": EventType.MEMBER_ADDED.value,
#             "aggregate_id": chat_id,
#             "aggregate_type": "chat",
#             "timestamp": datetime.now().isoformat(),
#             "data": {
#                 "chat_id": chat_id,
#                 "user_id": user_id,
#                 "added_by_user_id": added_by_user_id,
#                 "role": "member",
#             },
#             "metadata": {
#                 "service": "chat-service",
#                 "version": "1.0",
#             }
#         }
#
#     @staticmethod
#     def user_online_event(user_id: int) -> Dict[str, Any]:
#         """Создать событие 'пользователь онлайн' для Kafka"""
#         return {
#             "event_id": str(uuid.uuid4()),
#             "event_type": "user_online",
#             "aggregate_id": user_id,
#             "aggregate_type": "user",
#             "timestamp": datetime.now().isoformat(),
#             "data": {
#                 "user_id": user_id,
#                 "status": "online",
#                 "last_seen": datetime.now().isoformat(),
#             },
#             "metadata": {
#                 "service": "user-service",
#                 "version": "1.0",
#             }
#         }
#
#
# # ==================== CQRS COMMAND MODELS ====================
# class ChatCommand:
#     """Базовый класс для команд чата"""
#
#     def __init__(self, initiated_by_user_id: Optional[int] = None):
#         self.command_id = str(uuid.uuid4())
#         self.initiated_by_user_id = initiated_by_user_id
#         self.timestamp = datetime.now()
#
#
# class CreateChatCommand(ChatCommand):
#     """Команда создания чата"""
#
#     def __init__(
#             self,
#             name: Optional[str],
#             chat_type: ChatType,
#             created_by_user_id: int,
#             member_ids: List[int],
#             settings: Optional[Dict[str, Any]] = None,
#             **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.name = name
#         self.chat_type = chat_type
#         self.created_by_user_id = created_by_user_id
#         self.member_ids = member_ids
#         self.settings = settings or {}
#
#
# class SendMessageCommand(ChatCommand):
#     """Команда отправки сообщения"""
#
#     def __init__(
#             self,
#             chat_id: int,
#             sender_user_id: int,
#             content: str,
#             message_type: MessageType = MessageType.TEXT,
#             reply_to_message_id: Optional[int] = None,
#             media_url: Optional[str] = None,
#             **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.chat_id = chat_id
#         self.sender_user_id = sender_user_id
#         self.content = content
#         self.message_type = message_type
#         self.reply_to_message_id = reply_to_message_id
#         self.media_url = media_url
#
#
# class AddMemberCommand(ChatCommand):
#     """Команда добавления участника"""
#
#     def __init__(
#             self,
#             chat_id: int,
#             user_id: int,
#             role: MemberRole = MemberRole.MEMBER,
#             **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.chat_id = chat_id
#         self.user_id = user_id
#         self.role = role
#
#
# # ==================== OUTBOX PATTERN ====================
# class KafkaOutboxModel(Base):
#     """
#     Модель Outbox для надежной доставки сообщений в Kafka.
#     Паттерн Transactional Outbox.
#     """
#     __tablename__ = "kafka_outbox"
#
#     message_id: Mapped[str] = mapped_column(
#         String(36),
#         unique=True,
#         nullable=False,
#         default=lambda: str(uuid.uuid4())
#     )
#
#     topic: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
#     key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
#
#     # Сериализованное сообщение
#     payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
#
#     # Статус отправки
#     status: Mapped[str] = mapped_column(String(50), default='pending', index=True)  # pending, sent, failed
#     attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
#
#     # Временные метки
#     scheduled_for: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         nullable=False
#     )
#     sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#
#     # Ошибки при отправке
#     error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#
#     # Индексы
#     __table_args__ = (
#         Index('ix_kafka_outbox_status_scheduled', 'status', 'scheduled_for'),
#     )
#
#     @classmethod
#     def create_outbox_message(
#             cls,
#             topic: str,
#             payload: Dict[str, Any],
#             key: Optional[str] = None
#     ) -> 'KafkaOutboxModel':
#         """Создать сообщение для отправки в Kafka"""
#         return cls(
#             topic=topic,
#             key=key,
#             payload=payload,
#             status='pending',
#             scheduled_for=datetime.now()
#         )
#
#
# # ==================== INTEGRATION MODELS ====================
# class UserSyncStateModel(Base):
#     """
#     Модель для синхронизации состояния пользователей из внешнего сервиса.
#     """
#     __tablename__ = "user_sync_states"
#
#     user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
#
#     # Данные из внешнего сервиса
#     username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
#     first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
#     last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
#     avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
#
#     # Статус из Kafka событий
#     last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#     is_online: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
#
#     # Временные метки синхронизации
#     last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#     version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
#
#     # Связи (для быстрого доступа)
#     chat_memberships: Mapped[List['ChatMemberStateModel']] = relationship(
#         'ChatMemberStateModel',
#         primaryjoin='UserSyncStateModel.user_id == ChatMemberStateModel.user_id',
#         viewonly=True
#     )
#
#
# class ExternalServiceEventModel(Base):
#     """
#     Модель для хранения событий из внешних сервисов.
#     """
#     __tablename__ = "external_service_events"
#
#     event_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
#     source_service: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
#     event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
#
#     # Данные события
#     payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
#
#     # Обработка
#     is_processed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
#     processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#     processing_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#
#     # Для дедупликации
#     deduplication_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
#
#     __table_args__ = (
#         Index('ix_external_events_dedup', 'source_service', 'deduplication_key', unique=True),
#     )