# Building an Amharic E-commerce Data Extractor

This project focuses on fine-tuning  LLMs for an Amharic Named Entity Recognition (NER) system that extracts key business entities, such as product names, prices, and Locations, from text, images, and documents shared across Telegram channels. The extracted data will be used to populate EthioMart's centralised database, making it a comprehensive e-commerce hub
---

## 📊 Project Objectives

- Develop a repeatable workflow that begins with data ingestion from Telegram channels, proceeds through preprocessing and labeling, and results in structured, machine-readable data.
- Fine-tune a transformer-based model to achieve high accuracy (measured by F1-score) in identifying Product, Price, and Location entities within unstructured Amharic text.
- Go beyond just building a model by comparing multiple approaches, interpreting your model’s predictions with tools like SHAP/LIME, and delivering a final analysis that recommends the best model for EthioMart's business case.

---



## 📁 Project Structure

```plaintext
ethio-llm-challenge-week4/
│
├── data/                  # Contains raw and cleaned datasets
├── notebooks/             # Jupyter notebooks with EDA and analysis
├── scripts/               # Python scripts for modularized code
├── src/                   # Python classes 
├── README.md              # Project documentation (this file)
└── requirements.txt       # Python dependencies


```

## 🛠️ Tools and Libraries

- **Python**: Programming language used for analysis.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical computations.
- **Jupyter Notebook**: Interactive coding environment.
- **telethon**: Telegram Scraping.
- **Google Colab**: Fine tuning model
---

## 📈 Methodology

1. **Data Scraping**: Scrape e-commerce data from telegram channels.
2. **Date Labeling**: Label processed data using the CONLL format.
3. **Fine Tune NER model**: Fine-Tune a Named Entity Recognition (NER) model to extract key entities (e.g., products, prices, and location) from Amharic Telegram messages.
4. **Model Comparison & Selection**: Compare different models and select the best-performing one for the entity extraction task.
5. **Model Interpretability**: Use model interpretability tools to explain how the NER model identifies entities, ensuring transparency and trust in the system.
6. **FinTech Vendor Scorecard for Micro-Lending**: combining the entities extracted by your NER model with the metadata available on each Telegram post (like views and timestamps) to create a much richer profile of each vendor.


---

## 🚀 How to Run This Project

Follow the steps below to set up and run the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://https://github.com/metasebiya/ethiomart-llm-challenge-week4.git
cd ethiomart-llm-challenge-week4
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

jupyter notebook

google colab
```

## 👤 Author

- **Name**: Metasebiya Akililu
- **GitHub**: [@metasebiya](https://github.com/metasebiya)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For questions or feedback, please reach out via [GitHub Issues](https://github.com/metasebiya/solar-challenge-week1/issues).

