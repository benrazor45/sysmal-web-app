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

### 📊 What is API calls sequences?
API call sequences are like a list of actions a program takes while it's running. By analyzing these sequences, we can understand its behavior. This website compares the behavior of an uploaded file against known patterns of malware and safe programs.

Below are the top 20 key patterns frequently found in both malware and benign software that this system uses for detection.

**🔥 Top 20 Malware Key Patterns**
| No. | API Call Sequence |
|:---:|---|
| 1 | `createbindctx cotaskmemalloc` |
| 2 | `propvarianttostringalloc propvariantclear` |
| 3 | `coinitializeex systemfunction036` |
| 4 | `getmartaextensioninterface setsecuritydescriptordacl` |
| 5 | `cotaskmemalloc cogetapartmenttype coregisterinitializespy` |
| 6 | `cogetapartmenttype coregisterinitializespy` |
| 7 | `cotaskmemalloc cogetapartmenttype` |
| 8 | `initializesecuritydescriptor setentriesinaclw` |
| 9 | `coregisterinitializespy cotaskmemfree` |
| 10| `pscreatememorypropertystore propvarianttobuffer` |
| 11| `sortgethandle sortclosehandle` |
| 12| `createbindctx cotaskmemalloc cogetapartmenttype` |
| 13| `cotaskmemfree cogetmalloc` |
| 14| `cogetapartmenttype coregisterinitializespy cotaskmemfree` |
| 15| `propvarianttouint64 propvarianttoboolean` |
| 16| `setentriesinaclw getmartaextensioninterface` |
| 17| `setentriesinaclw getmartaextensioninterface setsecuritydescriptordacl` |
| 18| `themeinitapihook isprocessdpiaware` |
| 19| `coregisterinitializespy cotaskmemfree cogetmalloc` |
| 20| `initializesecuritydescriptor setentriesinaclw getmartaextensioninterface` |

**✅ Top 20 Benign Key Patterns**
| No. | API Call Sequence |
|:---:|---|
| 1 | `regopenkeyexw regqueryinfokeyw` |
| 2 | `regclosekey regqueryvalueexw` |
| 3 | `getlayout gdirealizationinfo` |
| 4 | `getlayout gdirealizationinfo fontislinked` |
| 5 | `sortgethandle sortclosehandle` |
| 6 | `coregisterinitializespy corevokeinitializespy` |
| 7 | `gettextfacealiasw regenumvaluew` |
| 8 | `getfontassocstatus regqueryvalueexa` |
| 9 | `regqueryinfokeyw gettextfacealiasw regenumvaluew` |
| 10| `regqueryvalueexw getfontassocstatus` |
| 11| `regqueryinfokeyw gettextfacealiasw` |
| 12| `getfontassocstatus regqueryvalueexa regenumkeyexw` |
| 13| `regqueryvalueexa regenumkeyexw` |
| 14| `fontislinked regopenkeyexw regqueryinfokeyw` |
| 15| `themeinitapihook isprocessdpiaware` |
| 16| `fontislinked regopenkeyexw` |
| 17| `regenumvaluew regclosekey` |
| 18| `gdirealizationinfo fontislinked` |
| 19| `gdirealizationinfo fontislinked regopenkeyexw` |
| 20| `regopenkeyexw regqueryinfokeyw gettextfacealiasw` |

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
