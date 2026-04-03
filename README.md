# 🚀 AI Startup Outreach Automation

This project helps you find startups and generate personalized cold emails using AI.

## 🔧 What it does

- Gets startup data from public sources  
- Filters startups with working websites  
- Uses AI to understand their business  
- Generates personalized outreach emails  
- Saves everything into CSV files  

## 📁 Output Files

### startup_raw.csv
Contains:
- name  
- idea  
- website  

### generated_outreach.csv
Contains:
- name  
- idea  
- website  
- generated_email  

## 🛠️ Setup

1. Clone the repo
git clone https://github.com/your-username/ai-outreach-tool.git
cd ai-outreach-tool

2. Create virtual environment
python -m venv myenv

Activate it:
- Mac/Linux: source myenv/bin/activate  
- Windows: myenv\Scripts\activate  

3. Install dependencies
pip install -r requirements.txt

4. Add API key

Create a file named config.py and add:
GEMINI_API_KEY = "your_api_key_here"

## ▶️ Run

python main.py

Optional UI:
streamlit run app.py

## ⚠️ Notes

- AI emails may not always be perfect  
- API limits can slow things down  
- Website data depends on source accuracy  

## ⚖️ Disclaimer

- Uses only public data  
- For learning and testing only  
- Do not use for spam  
- Follow laws like GDPR and email rules  

## 👨‍💻 Author

Ayush  
AI Automation / Data Science