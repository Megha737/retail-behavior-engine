# 🚀 Retail Behavior Engine

**Transform raw transaction data into actionable business intelligence with AI-powered customer segmentation.**

---

### 🌟 Project Overview
The **Retail Behavior Engine** is an intelligent SaaS platform designed to bridge the gap between raw e-commerce data and strategic marketing. By utilizing K-Means machine learning algorithms, the platform automatically identifies distinct customer personas—from "Champions" to "At-Risk" users—allowing businesses to optimize their campaigns with surgical precision.



### 🎯 Key Features
* **Machine Learning Pipeline:** Automated clustering to uncover hidden customer behavioral patterns.
* **Intuitive Bento-Grid UI:** A high-performance, dark-mode compatible dashboard for seamless data visualization.
* **Real-time Insights:** Instant processing of datasets via a FastAPI-powered backend.
* **Actionable Exports:** Direct CSV export functionality for integration with your CRM or marketing tools.
* **User Onboarding:** Integrated guided tour experience for immediate platform adoption.

### 🛠 Tech Stack
| Tier | Technology |
| :--- | :--- |
| **Frontend** | React.js, Recharts, React-Joyride |
| **Backend** | FastAPI, Pandas, Scikit-Learn |
| **Database** | SQLite |
| **UI/UX** | Modern Cyber-Grid & Bento-Box Design |

---

### 📦 Quick Start

**1. Clone the repository:**
```bash
git clone [https://github.com/your-username/retail-behavior-engine.git](https://github.com/your-username/retail-behavior-engine.git)
cd retail-behavior-engine
1. Launch the Backend:
cd backend
pip install -r requirements.txt
uvicorn api:app --reload
2. Launch the Dashboard:
cd frontend/dashboard
npm install
npm start