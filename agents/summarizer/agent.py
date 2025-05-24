from dotenv import load_dotenv
import os

# Load environment variables (for GOOGLE_API_KEY)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
