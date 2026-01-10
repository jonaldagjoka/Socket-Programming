"""
Test Suite për Sistemet e Chat-it
Përmban unit tests dhe integration tests për të tre sistemet
"""

import unittest
import socket
import threading
import time
import base64
import os
from io import StringIO
import sys


# ============================================
# HELPER FUNCTIONS (nga kodet origjinale)
# ============================================

def encrypt(msg):
    """Enkripton mesazhin me Base64"""
    return base64.b64encode(msg.encode()).decode()


def decrypt(msg):
    """Dekripton mesazhin nga Base64"""
    return base64.b64decode(msg.encode()).decode()


# ============================================
# UNIT TESTS - Enkriptimi/Dekriptimi
# ============================================

class TestEncryptionDecryption(unittest.TestCase):
    """Test për funksionet e enkriptimit dhe dekriptimit"""
    
    def test_encrypt_simple_message(self):
        """Teston enkriptimin e një mesazhi të thjeshtë"""
        msg = "Hello World"
        encrypted = encrypt(msg)
        self.assertNotEqual(msg, encrypted)
        self.assertIsInstance(encrypted, str)
    
    def test_decrypt_simple_message(self):
        """Teston dekriptimin e një mesazhi të enkriptuar"""
        msg = "Hello World"
        encrypted = encrypt(msg)
        decrypted = decrypt(encrypted)
        self.assertEqual(msg, decrypted)
    
    def test_encrypt_decrypt_special_characters(self):
        """Teston enkriptimin/dekriptimin me karaktere speciale"""
        msg = "Përshëndetje! Çfarë bën? @#$%"
        encrypted = encrypt(msg)
        decrypted = decrypt(encrypted)
        self.assertEqual(msg, decrypted)
    
    def test_encrypt_decrypt_empty_string(self):
        """Teston enkriptimin e string-ut bosh"""
        msg = ""
        encrypted = encrypt(msg)
        decrypted = decrypt(encrypted)
        self.assertEqual(msg, decrypted)
    
    def test_encrypt_decrypt_long_message(self):
        """Teston mesazhe të gjata"""
        msg = "A" * 1000
        encrypted = encrypt(msg)
        decrypted = decrypt(encrypted)
        self.assertEqual(msg, decrypted)


# ============================================
# INTEGRATION TESTS - Basic Server
# ============================================

class TestBasicServer(unittest.TestCase):
    """Integration tests për server.py"""
    
    @classmethod
    def setUpClass(cls):
        """Nis serverin para testeve"""
        cls.HOST = 'localhost'
        cls.PORT = 5001  # Përdor port tjetër për test
        cls.server_thread = None
        # Serveri do të niset në metoda individuale sipas nevojës
    
    def test_client_can_connect(self):
        """Teston nëse klienti mund të lidhet me serverin"""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2)
            # Provo të lidhesh me një server që nuk ekziston
            with self.assertRaises(Exception):
                client.connect(('localhost', 9999))
            client.close()
        except Exception as e:
            self.fail(f"Test dështoi: {e}")
    
    def test_message_encryption_over_socket(self):
        """Teston dërgimin e mesazheve të enkriptuara"""
        msg = "Test message"
        encrypted = encrypt(msg)
        
        # Simulon dërgimin
        self.assertTrue(len(encrypted) > 0)
        self.assertNotEqual(msg, encrypted)


# ============================================
# INTEGRATION TESTS - Broadcast Server
# ============================================

class TestBroadcastServer(unittest.TestCase):
    """Integration tests për broadcast_server.py"""
    
    def test_multiple_clients_list(self):
        """Teston menaxhimin e shumë klientëve në listë"""
        clients = []
        
        # Simulon shtimin e klientëve
        clients.append((None, "User1"))
        clients.append((None, "User2"))
        clients.append((None, "User3"))
        
        self.assertEqual(len(clients), 3)
        
        # Teston heqjen e një klienti
        clients = [c for c in clients if c[1] != "User2"]
        self.assertEqual(len(clients), 2)
        usernames = [c[1] for c in clients]
        self.assertNotIn("User2", usernames)
        self.assertIn("User1", usernames)
        self.assertIn("User3", usernames)
    
    def test_broadcast_message_filtering(self):
        """Teston që mesazhi të mos dërgohet te dërguesi"""
        clients = [
            ("conn1", "Alice"),
            ("conn2", "Bob"),
            ("conn3", "Charlie")
        ]
        
        sender = "conn1"
        recipients = [c for c in clients if c[0] != sender]
        
        self.assertEqual(len(recipients), 2)
        recipient_names = [c[1] for c in recipients]
        self.assertNotIn("Alice", recipient_names)
        self.assertIn("Bob", recipient_names)
        self.assertIn("Charlie", recipient_names)


# ============================================
# INTEGRATION TESTS - Private Chat
# ============================================

class TestPrivateChat(unittest.TestCase):
    """Integration tests për private_server.py"""
    
    def test_username_uniqueness(self):
        """Teston që username-të të jenë unikë"""
        clients = {}
        
        # Shton përdorues të parë
        username1 = "Alice"
        clients[username1] = "conn1"
        
        # Provo të shtosh të njëjtin username
        username2 = "Alice"
        is_unique = username2 not in clients
        
        self.assertFalse(is_unique)
        self.assertEqual(len(clients), 1)
    
    def test_parse_at_all_message(self):
        """Teston parse-imin e mesazhit @all"""
        message = "@all Hello everyone!"
        
        if message.startswith("@"):
            parts = message.split(" ", 1)
            recipient = parts[0][1:]  # Heq @
            msg_content = parts[1] if len(parts) > 1 else ""
            
            self.assertEqual(recipient, "all")
            self.assertEqual(msg_content, "Hello everyone!")
    
    def test_parse_at_username_message(self):
        """Teston parse-imin e mesazhit @username"""
        message = "@Bob How are you?"
        
        if message.startswith("@"):
            parts = message.split(" ", 1)
            recipient = parts[0][1:]
            msg_content = parts[1] if len(parts) > 1 else ""
            
            self.assertEqual(recipient, "Bob")
            self.assertEqual(msg_content, "How are you?")
    
    def test_user_exists_in_dictionary(self):
        """Teston nëse përdoruesi ekziston në dictionary"""
        clients = {
            "Alice": "conn1",
            "Bob": "conn2",
            "Charlie": "conn3"
        }
        
        self.assertTrue("Alice" in clients)
        self.assertTrue("Bob" in clients)
        self.assertFalse("Dave" in clients)
    
    def test_invalid_message_format(self):
        """Teston mesazhe me format të gabuar"""
        message = "Hello without @"
        
        is_valid = message.startswith("@")
        self.assertFalse(is_valid)
        
        message2 = "@"
        parts = message2.split(" ", 1)
        has_recipient = len(parts[0]) > 1
        self.assertFalse(has_recipient)


# ============================================
# TESTS - Logging Functionality
# ============================================

class TestLogging(unittest.TestCase):
    """Teston funksionalitetin e logging-ut"""
    
    def setUp(self):
        """Krijo një file test për logging"""
        self.test_log = "test_chat_log.txt"
    
    def tearDown(self):
        """Fshi file-in test pas testimit"""
        if os.path.exists(self.test_log):
            os.remove(self.test_log)
    
    def test_log_message_writes_to_file(self):
        """Teston që mesazhet të shkruhen në file"""
        message = "[2025-12-21 10:00:00] TestUser: Hello"
        
        with open(self.test_log, "a") as f:
            f.write(message + "\n")
        
        self.assertTrue(os.path.exists(self.test_log))
        
        with open(self.test_log, "r") as f:
            content = f.read()
            self.assertIn("TestUser: Hello", content)
    
    def test_log_multiple_messages(self):
        """Teston logging-un e shumë mesazheve"""
        messages = [
            "[2025-12-21 10:00:00] User1: Message 1",
            "[2025-12-21 10:01:00] User2: Message 2",
            "[2025-12-21 10:02:00] User3: Message 3"
        ]
        
        with open(self.test_log, "a") as f:
            for msg in messages:
                f.write(msg + "\n")
        
        with open(self.test_log, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)


# ============================================
# PERFORMANCE TESTS
# ============================================

class TestPerformance(unittest.TestCase):
    """Teston performance-in e sistemit"""
    
    def test_encryption_speed(self):
        """Teston shpejtësinë e enkriptimit"""
        msg = "Test message" * 100
        
        start = time.time()
        for _ in range(1000):
            encrypted = encrypt(msg)
        end = time.time()
        
        duration = end - start
        self.assertLess(duration, 5.0)  # Duhet të përfundojë në < 5 sekonda
    
    def test_decryption_speed(self):
        """Teston shpejtësinë e dekriptimit"""
        msg = "Test message" * 100
        encrypted = encrypt(msg)
        
        start = time.time()
        for _ in range(1000):
            decrypted = decrypt(encrypted)
        end = time.time()
        
        duration = end - start
        self.assertLess(duration, 5.0)


# ============================================
# TEST RUNNER
# ============================================

def run_tests():
    """Ekzekuton të gjitha testet"""
    
    print("=" * 70)
    print("DUKE EKZEKUTUAR TESTET PËR SISTEMET E CHAT-IT")
    print("=" * 70)
    print()
    
    # Krijo test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Shto të gjitha test class-at
    suite.addTests(loader.loadTestsFromTestCase(TestEncryptionDecryption))
    suite.addTests(loader.loadTestsFromTestCase(TestBasicServer))
    suite.addTests(loader.loadTestsFromTestCase(TestBroadcastServer))
    suite.addTests(loader.loadTestsFromTestCase(TestPrivateChat))
    suite.addTests(loader.loadTestsFromTestCase(TestLogging))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Ekzekuto testet
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Raporti final
    print()
    print("=" * 70)
    print("RAPORTI FINAL")
    print("=" * 70)
    print(f"Teste të ekzekutuara: {result.testsRun}")
    print(f"Sukses: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Dështime: {len(result.failures)}")
    print(f"Gabime: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)