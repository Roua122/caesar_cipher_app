# General Caesar Cipher Studio (PySide6)

A professional, animated, dark-mode desktop GUI application built in Python for encrypting, decrypting, and cracking text using the **General Caesar Cipher (Additive Cipher)** algorithm.

---

## 📁 Project Architecture & Modular Separation

This codebase is organized following strict **Separation of Concerns**:

```
caesar_cipher_app/
│
├── core/                           # 🧠 ALGORITHM LOGIC (NO GUI DEPENDENCIES)
│   ├── __init__.py
│   ├── caesar_cipher.py            # Encrypt, Decrypt, & Brute-force Math
│   └── validator.py                # Input validation & stats helper
│
├── ui/                             # 🎨 USER INTERFACE & ASSETS LAYER
│   ├── assets/                     # 💎 DESIGN SYSTEM & STYLING
│   │   ├── theme.py                # Dark Cyberpunk Colors (QSS) & Fonts
│   │   └── icons.py                # Crisp Vector Icon Factory (QPainter)
│   ├── components/                 # 🧩 REUSABLE ANIMATED WIDGETS
│   │   ├── animated_card.py        # Container Card with Hover Glow & Shadow
│   │   ├── cipher_wheel.py        # Rotating Concentric Caesar Disk (QPropertyAnimation)
│   │   └── toast.py                # Floating Feedback Toast Notification
│   └── views/                      # 🖥️ SCREEN VIEWS & LAYOUTS
│       ├── encrypt_decrypt_view.py # Encrypt/Decrypt interactive screen
│       ├── brute_force_view.py     # Brute-force cracker & frequency analysis table
│       └── main_window.py          # Primary application frame
│
├── tests/                          # 🧪 AUTOMATED TESTS
│   └── test_caesar.py              # Unit tests for core algorithm
│
├── main.py                         # 🚀 Entry Point
├── requirements.txt                # Dependencies (PySide6)
└── README.md                       # Documentation
```

---

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**:
   ```bash
   python main.py
   ```

3. **Run Unit Tests**:
   ```bash
   python -m unittest discover -s tests
   ```

---

## ✨ Features

- **Interactive Animated Caesar Wheel**: Concentric outer (Plaintext) and inner (Ciphertext) alphabetic rings that rotate smoothly in real-time when shift key $K$ changes.
- **Explicit Shift Key Controls**: Numeric box, slider, and quick presets ($K=3, 5, 13$).
- **Live Transformation**: Text encrypts/decrypts instantaneously as you type or adjust $K$.
- **Automated Brute-Force Cracker**: Evaluates all 26 shift candidates using English letter frequency matching ($\chi^2$ scoring) to automatically crack unknown ciphers.
- **Micro-Interactions**: Custom vector icons, copy feedback toasts, card hover glows, and text swap actions.
