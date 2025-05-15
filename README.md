# SportStats Pipeline 📊 (in progress)

SportStats Pipeline is a data pipeline project designed to collect, process, and store sports-related data. This project aims to automate the extraction and transformation of sports events, results, and statistics, providing structured and reliable datasets for analysis.

## 🚀 Features

- ⏱️ Daily automated extraction of sports events
- 🔄 ETL process (Extract, Transform, Load)
- 💾 Storage of structured data in a database or file system
- 🧹 Data cleaning and transformation logic
- 🔁 Scheduled execution with Apache Airflow

## 🛠️ Technologies Used

- **Python**
- **Apache Airflow**
- **Pandas / NumPy**
- **Requests**
- **MySQL** (adaptable)
- **TheSportsDB API** *(or other public sports API)*

## ⚙️ How to Run

1. Clone the repository:
  ```bash
  git clone https://github.com/An4PDM/SportStats-Pipeline.git
  cd SportStats-Pipeline
   ```

2. Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  ```

3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

4. Set up and start Apache Airflow (basic setup):
  
  ```bash
  export AIRFLOW_HOME=$(pwd)/airflow
  airflow db init
  airflow users create \
    --username admin \
    --password admin \
    --firstname First \
    --lastname Last \
    --role Admin \
    --email admin@example.com
  airflow webserver --port 8080
  airflow scheduler
  ```
5. Open http://localhost:8080 and trigger the sports DAG.

## Tests

You can test individual components (e.g., scripts in scripts/) by running them directly:

  ```bash
  python scripts/extract.py
  python scripts/transform.py
  ```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
