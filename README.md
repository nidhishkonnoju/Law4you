# Law4you ⚖️

**An AI-powered legal assistant to help you understand complex legal documents.**

---

> This project is a submission for the **Google Gen AI Hackathon**.

## 🚀 Live Demo

You can access the live application hosted on Streamlit Cloud:

**[➡️ Visit Law4you Live](https://law4you-wr2vcappznwhe4wsrxuaoay.streamlit.app)** 

## The Problem

Legal documents are often filled with complex jargon and convoluted sentences, making them difficult for the average person to understand. This can lead to confusion, risk, and a feeling of powerlessness. Law4you aims to bridge this gap by providing clear, concise, and actionable insights into your legal texts.

## ✨ Features

*   **📝 Plain English Summaries:** Get a simple, easy-to-understand summary of any legal clause.
*   **🔍 Jargon Buster:** Instantly get definitions for confusing legal terms.
*   **🚨 Risk Analysis:** A gauge provides an at-a-glance view of the potential risk level in a document.
*   **❓ Questions for Your Lawyer:** Generates a list of relevant questions to ask your legal counsel, empowering you to have more informed conversations.
*   **📂 Multiple Input Formats:** Analyze text by:
    *   Pasting it directly.
    *   Uploading a PDF file.
    *   Uploading an image of a document.
*   **💬 Chat History:** Keeps your analysis sessions organized and accessible.

## 🛠️ How It Works

Law4you is built with Python and leverages the power of Google's Gemini AI to provide its analysis.

*   **Frontend:** The user interface is a web application built with **Streamlit**.
*   **Backend & AI:**
    *   **Gemini 1.5 Pro:** Used for analyzing text-based inputs.
    *   **Gemini 1.5 Flash:** Used for its speed in transcribing and analyzing text from images.
*   **Document Processing:**
    *   **PyMuPDF** is used to extract text from PDF documents.
    *   **Pillow** is used to handle image files.
    *   **Plotly** is used to create the risk assessment gauge.

## ⚙️ Getting Started (for Local Development)

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

*   Python 3.8+
*   A Google API Key with the Gemini API enabled.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nidhishkonnoju/Law4you
    cd law4you
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    *   Create a file named `.env` in the root of the project directory.
    *   Add your Google API key to the `.env` file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

### Running the Application

1.  **Start the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

2.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

## 📄 License

This project is licensed under the MIT License.
