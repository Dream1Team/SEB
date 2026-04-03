from enum import Enum


class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"
    STICKER = "sticker"
    VOICE = "voice"
    VIDEO_NOTE = "video_note"
    LOCATION = "location"
    POLL = "poll"
    CONTACT = "contact"


class MemberRole(str, Enum):
    CREATOR = "creator"
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"
    RESTRICTED = "restricted"


class EventType(str, Enum):
    # События чатов
    CHAT_CREATED = "chat_created"
    CHAT_UPDATED = "chat_updated"
    CHAT_DELETED = "chat_deleted"

    # События участников
    MEMBER_ADDED = "member_added"
    MEMBER_REMOVED = "member_removed"
    MEMBER_UPDATED = "member_updated"

    # События сообщений
    MESSAGE_SENT = "message_sent"
    MESSAGE_UPDATED = "message_updated"
    MESSAGE_DELETED = "message_deleted"
    MESSAGE_READ = "message_read"

    # События приглашений
    INVITE_CREATED = "invite_created"
    INVITE_USED = "invite_used"
