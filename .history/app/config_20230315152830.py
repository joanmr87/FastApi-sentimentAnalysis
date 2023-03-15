import os
from dotenv import load_dotenv

load_dotenv()

def get_credentials():
    """
    Read the user and password from an environment variable.

    Args:
        None

    Returns:
        Tuple[str, str]: A tuple containing the user and password.

    """
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    return user, password

def get_imap_url():
    """
    Returns the IMAP URL for the email server.

    Args:
        None

    Returns:
        str: The IMAP URL.

    """
    return "imap.gmail.com"

def get_nltk_resources():
    """
    Download the necessary NLTK resources if they are not already present.

    Args:
        None

    Returns:
        None

    """
    import nltk

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')

get_nltk_resources()
