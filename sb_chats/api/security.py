import os
from dotenv import load_dotenv
import base64
from typing import Tuple, Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag
import secrets

load_dotenv()

class EncryptionService:
    def __init__(self):
        """
        Инициализация сервиса шифрования

        Args:
            master_key: Основной ключ. Берется из env
        """
        self.master_key = os.getenv('ENCRYPTION_MASTER_KEY')
        if not self.master_key:
            raise ValueError("Encryption master key is required")

        self.app_salt = os.getenv('SALT', 'default_app_salt').encode()

        self.derived_key = self._derive_key(
            password=self.master_key.encode(),
            salt=self.app_salt,
            iterations=400000
            )

    @staticmethod
    def generate_random_salt(length: int = 16) -> bytes:
        """
        Генерация криптографически безопасной случайной соли

        Args:
            length: Длина соли в байтах (рекомендуется 16+)

        Returns:
            Случайная соль
        """
        return secrets.token_bytes(length)

    @staticmethod
    def _derive_key(password: bytes, salt: bytes = None, iterations: int = 400000) -> bytes:
        """
        Деривация ключа из пароля с использованием PBKDF2

        Args:
            password: Мастер-пароль/ключ
            salt: Соль для деривации
            iterations: Количество итераций (больше = медленнее)

        Returns:
            Деривированный ключ (32 байта для AES-256)
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 бит для AES-256
            salt=salt,
            iterations=iterations,
        )
        return kdf.derive(password)

    def encrypt(self, plaintext: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes, bytes, bytes]:
        """
        Шифрование текста с уникальной солью для каждого сообщения

        Args:
            plaintext: Текст для шифрования
            salt: Уникальная соль для этого сообщения (если None - генерируется)

        Returns:
            Tuple[salt, nonce, tag, ciphertext]
        """
        # Генерация уникальной соли для этого сообщения
        if salt is None:
            salt = self.generate_random_salt()

        # Деривация ключа для этого конкретного сообщения
        message_key = self._derive_key(
            password=self.master_key.encode(),
            salt=salt,
            iterations=400000
        )

        # Генерация случайного nonce (96 бит для GCM)
        nonce = secrets.token_bytes(12)

        # Создание шифра с ключом этого сообщения
        cipher = Cipher(
            algorithm=algorithms.AES(message_key),
            mode=modes.GCM(nonce)
        )

        encryptor = cipher.encryptor()

        # Шифрование
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        return salt, nonce, encryptor.tag, ciphertext

    def decrypt(self, salt: bytes, nonce: bytes, tag: bytes, ciphertext: bytes) -> str:
        """
        Дешифровка текста с использованием соли

        Args:
            salt: Соль, использованная при шифровании
            nonce: Nonce из шифрования
            tag: Аутентификационный тег
            ciphertext: Зашифрованный текст

        Returns:
            Расшифрованный текст

        Raises:
            ValueError: Если дешифровка не удалась
        """

        try:
            # Восстанавливаем ключ для этого сообщения
            message_key = self._derive_key(
                password=self.master_key.encode(),
                salt=salt,
                iterations=400000
            )

            # Создание шифра
            cipher = Cipher(
                algorithms.AES(message_key),
                modes.GCM(nonce, tag)
            )

            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            return plaintext.decode()
        except InvalidTag:
            raise ValueError("Invalid decryption tag - data may be corrupted or tampered with")
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def encrypt_to_string(self, plaintext: str) -> str:
        """
        Шифрование с возвратом единой строки в формате base64

        Формат: base64(salt + nonce + tag + ciphertext)
        Размеры: salt(16) + nonce(12) + tag(16) + ciphertext(?)

        Returns:
            Единая закодированная строка
        """
        salt, nonce, tag, ciphertext = self.encrypt(plaintext)

        # Объединяем все компоненты
        combined = salt + nonce + tag + ciphertext

        # Кодируем в base64 для хранения в текстовом поле
        return base64.b64encode(combined).decode()

    def decrypt_from_string(self, encrypted_str: str) -> str:
        """
        Дешифровка из единой строки base64

        Args:
            encrypted_str: Строка в формате base64(salt+nonce+tag+ciphertext)

        Returns:
            Расшифрованный текст
        """
        # Декодируем из base64
        combined = base64.b64decode(encrypted_str.encode())

        # Извлекаем компоненты
        # Предполагаем размеры: salt=16, nonce=12, tag=16
        salt = combined[:16]
        nonce = combined[16:28]
        tag = combined[28:44]
        ciphertext = combined[44:]

        return self.decrypt(salt, nonce, tag, ciphertext)

    def encrypt_with_app_key(self, plaintext: str) -> Tuple[bytes, bytes, bytes]:
        """
        Быстрое шифрование с использованием прикладного ключа
        (без уникальной соли для каждого сообщения)

        Returns:
            Tuple[nonce, tag, ciphertext]
        """
        # Генерация случайного nonce
        nonce = secrets.token_bytes(12)

        # Используем предварительно вычисленный ключ приложения
        cipher = Cipher(
            algorithms.AES(self.derived_key),
            modes.GCM(nonce)
        )

        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        return nonce, encryptor.tag, ciphertext

    def decrypt_with_app_key(self, nonce: bytes, tag: bytes, ciphertext: bytes) -> str:
        """
        Быстрая дешифровка с ключом приложения
        """
        try:
            cipher = Cipher(
                algorithms.AES(self.derived_key),
                modes.GCM(nonce, tag)
            )

            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            return plaintext.decode()
        except InvalidTag:
            raise ValueError("Decryption failed: invalid tag")

# # Утилитарные функции для удобства
# def generate_master_key() -> str:
#     """Генерация безопасного мастер-ключа"""
#     return secrets.token_urlsafe(32)  # 32 байта в URL-safe base64
#
# def generate_app_salt() -> str:
#     """Генерация соли для приложения"""
#     return base64.b64encode(secrets.token_bytes(16)).decode()
#
# # Фабрика для создания сервиса
# def create_encryption_service():
#     """
#     Создание EncryptionService с безопасными значениями по умолчанию
#     """
#     # Получаем или генерируем ключ
#     master_key = os.getenv('ENCRYPTION_MASTER_KEY')
#     if not master_key:
#         # В продакшене генерируем и сохраняем
#         master_key = generate_master_key()
#         print(f"⚠️  Generated master key (save this!): {master_key}")
#
#     # Получаем или генерируем соль
#     app_salt = os.getenv('ENCRYPTION_SALT')
#     if not app_salt:
#         app_salt = generate_app_salt()
#         print(f"⚠️  Generated app salt (save this!): {app_salt}")
#
#     return EncryptionService(master_key=master_key)

# Глобальный экземпляр
encryption_service = EncryptionService()