import os
from dotenv import load_dotenv

# Sub-agent factories

# Load environment variables (for GOOGLE_API_KEY)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
