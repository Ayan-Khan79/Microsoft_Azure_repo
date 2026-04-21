import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

# Load credentials from .env file
load_dotenv()
endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("DOCUMENT_INTELLIGENCE_KEY")
model_id = os.getenv("CUSTOM_MODEL_ID")

print(f"Debug: Using endpoint {endpoint}")
print(f"Debug: Key starts with {key[:4]}...")
print(f"Debug: Model ID is {model_id}")

# The URL of the student document you want to test
formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

def analyze_student_doc(endpoint, key, model_id): # <-- Added arguments here
    # Initialize client
    client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )

    # Start analysis
    poller = client.begin_analyze_document(
        model_id, 
        AnalyzeDocumentRequest(url_source=formUrl)
    )
    result = poller.result()

    # Output the Structured Fields
    for idx, document in enumerate(result.documents):
        print(f"\n--- Analyzing Student Document #{idx + 1} ---")
        print(f"Confidence: {document.confidence:.2f}")
        
        for name, field in document.fields.items():
            # Get the content or the specific value if it exists
            val = field.get('valueString') or field.get('content')
            print(f"Found Field: {name} -> {val} (Confidence: {field.confidence})")

if __name__ == "__main__":
    # Pass the variables into the function call
    analyze_student_doc(endpoint, key, model_id)