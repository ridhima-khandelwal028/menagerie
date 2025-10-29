# Menagerie - FastAPI REST Service
A small Pet Menagerie REST API built with FastAPI, Pydantic, and SQLAlchemy.

# Clone Repository
git clone https://github.com/ridhima-khandelwal028/menagerie.git
cd menagerie

# Create Virtual Environment
python -m venv env
env\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Application
uvicorn app.main:app --reload