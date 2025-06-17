import streamlit as st

st.header("❓ Help Page")

hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
        footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.markdown("""
Here you can find descriptive information about what ransomware is, why it's dangerous, and how this website helps detect it.

---

### 🧨 What is Malware and Ransomware?

**Malware** (short for *malicious software*) is any kind of software that is made to harm your computer or steal your data. It includes things like viruses, spyware, and ransomware.

**Ransomware** is a special type of malware that locks your files or computer and asks you to pay money (a ransom) to get access back. This can happen to anyone—individuals, companies, even hospitals. In 2024, ransomware attacks increased by more than 38%, causing millions of dollars in damages around the world.

---

### 🌍 Why Ransomware is Dangerous

Ransomware can:
- Lock your important files (photos, documents, etc.)
- Make your business or computer unusable
- Cost you a lot of money
- Damage your reputation if private data is leaked

That’s why detecting ransomware early is so important.

---

### 🧠 How This Website Detects Ransomware

This website uses **Artificial Intelligence (AI)** to help detect whether a program is dangerous or not.

Here's how it works, step by step:

1. **You upload a `.exe` file** (a Windows program).
2. The file is run in a **safe virtual environment** (so it doesn’t harm your real computer).
3. While the file runs, the system watches what it does behind the scenes—like opening files, using the internet, or accessing your system. These actions are called **API calls**.
4. All those actions are collected into a list that shows how the program behaves.
5. That behavior is sent into a **deep learning model** (a kind of smart program) that has learned to tell the difference between normal programs and ransomware.
6. The system gives you a result: whether the file is **safe (benign)** or **dangerous (malware)**.

This method looks at how the program behaves—not just what it looks like—so it can even detect **new or hidden threats** that traditional antivirus software might miss.

---

### 🔒 Stay Safe

Early detection is key. With tools like this, powered by AI, we can detect threats before they cause damage.

""", unsafe_allow_html=True)
