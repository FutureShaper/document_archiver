# LLM classification logic using LangChain and Ollama
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from typing import Dict, Any, Optional
import re
import json

class LLMClassifier:
    def __init__(self, model_name: str = "qwen3:14b", ollama_base_url: str = "http://localhost:11434"):
        """
        Initializes the LLMClassifier with a specified Ollama model.

        Args:
            model_name: The name of the Ollama model to use (e.g., "qwen3:14b", "llama3").
                        Ensure this model is pulled and available in your Ollama instance.
            ollama_base_url: The base URL for the Ollama API.
        """
        self.llm = Ollama(model=model_name, base_url=ollama_base_url)
        self.json_parser = JsonOutputParser()

        # Define a more sophisticated prompt for classification and metadata extraction
        # This prompt asks for a specific JSON structure for easier parsing.
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert document classification assistant. "
                    "Your task is to categorize the provided text and extract relevant metadata. "
                    "The categories could include, but are not limited to: "
                    "'contractor_invoice', 'health_prescription', 'health_insurance', 'receipt', 'letter', 'utility_bill', 'other'. "
                    "Based on the text, determine the most appropriate category. "
                    "Also, extract key pieces of information like dates, names, amounts, invoice numbers, or a brief summary. "
                    "VERY IMPORTANT: Respond *ONLY* with a single, valid JSON object. Do not include any other text, explanations, or conversational elements before or after the JSON object. "
                    "The JSON object must contain two keys: 'category' (a string) and 'metadata' (an object with extracted details or a summary string). "
                    "Example of the exact output format: {{ \"category\": \"invoice\", \"metadata\": {{ \"invoice_number\": \"INV123\", \"date\": \"2024-01-15\", \"total_amount\": \"$500\", \"summary\": \"Invoice for services rendered\" }} }} "
                    "If the document is multi-page, the metadata should reflect that this is part of a larger document if discernible. Ensure your output is a single, complete JSON object and nothing else."
                ),
                ("human", "Please classify the following document text:\\n\\n{document_text}"),
            ]
        )

        # Chain for classification and metadata extraction
        self.classification_chain = self.prompt_template | self.llm | self.json_parser

    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Classifies the given text using the LLM and extracts metadata.

        Args:
            text: The text extracted from the document.

        Returns:
            A dictionary containing the 'category' and 'metadata'.
            Example: {"category": "invoice", "metadata": {"invoice_number": "INV123", ...}}
        """
        if not text or not text.strip():
            print("LLMClassifier: Received empty text, cannot classify.")
            return {"category": "unknown_empty_text", "metadata": {"error": "Input text was empty"}}

        print(f"LLMClassifier: Classifying text (first 100 chars): {text[:100]}...")
        
        raw_llm_output_for_fallback = ""

        try:
            # Primary attempt: Invoke the chain to get a structured JSON response
            # The self.json_parser will attempt to parse the LLM output directly.
            response = self.classification_chain.invoke({"document_text": text})
            
            if isinstance(response, dict) and "category" in response and "metadata" in response:
                print(f"LLMClassifier: Successfully classified. Category: {response.get('category')}")
                return response
            else:
                # This case might be hit if json_parser somehow returns a non-dict or a dict without expected keys,
                # though typically it would raise an exception if parsing fails.
                print(f"LLMClassifier: Unexpected response structure from LLM after JSON parsing: {response}")
                raw_llm_output_for_fallback = str(response) # Save for more robust fallback
                # Proceed to a more robust fallback that tries to extract JSON from a string if direct parsing failed.
                raise ValueError("Initial JSON parsing did not yield expected dictionary structure.")

        except Exception as e:
            print(f"LLMClassifier: Error during primary LLM classification or JSON parsing: {e}")
            
            # If the primary attempt failed, it's possible the LLM included extra text (e.g., <think> tags).
            # We need the raw string output from the LLM to attempt to extract the JSON manually.
            # The self.classification_chain includes self.json_parser, so if it failed, 'e' is likely an OutputParserException.
            # We need to get the LLM's direct string output *before* the json_parser tried to parse it.
            
            # Let's get the raw string output first
            try:
                print("LLMClassifier: Attempting to get raw string output from LLM for manual JSON extraction...")
                raw_llm_output_chain = self.prompt_template | self.llm | StrOutputParser()
                raw_llm_output_for_fallback = raw_llm_output_chain.invoke({"document_text": text})
                print(f"LLMClassifier: Raw LLM output received: {raw_llm_output_for_fallback[:300]}...") # Print first 300 chars
            except Exception as raw_fetch_error:
                print(f"LLMClassifier: Could not even fetch raw string output from LLM: {raw_fetch_error}")
                return {"category": "unknown_severe_error", 
                        "metadata": {"summary": "Failed to fetch raw output from LLM.", "primary_error": str(e), "fetch_error": str(raw_fetch_error)}}

            # Attempt to extract JSON from the raw string output
            try:
                # Regex to find a JSON object, robust to surrounding text
                # It looks for text starting with { and ending with }, non-greedily.
                # This might need refinement if JSON strings themselves contain escaped braces.
                match = re.search(r'\{.*\}', raw_llm_output_for_fallback, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    print(f"LLMClassifier: Extracted potential JSON: {json_str[:300]}...")
                    parsed_fallback = json.loads(json_str)
                    if isinstance(parsed_fallback, dict) and "category" in parsed_fallback and "metadata" in parsed_fallback:
                        print("LLMClassifier: Successfully parsed extracted JSON from raw output.")
                        return parsed_fallback
                    else:
                        print("LLMClassifier: Extracted string was valid JSON but not the expected structure.")
                else:
                    print("LLMClassifier: No JSON object found in raw LLM output.")
            except json.JSONDecodeError as json_decode_error:
                print(f"LLMClassifier: Failed to parse extracted JSON string: {json_decode_error}")
            except Exception as extraction_error:
                print(f"LLMClassifier: Error during manual JSON extraction: {extraction_error}")

            # If all above fails, return a generic error with the raw output for debugging
            print("LLMClassifier: All parsing attempts failed.")
            return {"category": "unknown_parsing_failure_all_attempts", 
                    "metadata": {"summary": "Could not parse LLM response as JSON despite multiple attempts.", 
                                 "primary_error_message": str(e), 
                                 "raw_llm_output": raw_llm_output_for_fallback}}


# Example Usage (for testing - requires Ollama server running with a model like 'qwen3:14b')
if __name__ == '__main__':
    classifier = LLMClassifier(model_name="qwen3:14b") 

    sample_text_invoice = """
    INVOICE
    Date: January 15, 2024
    Invoice # INV001
    To: John Doe
    Description: Web Development Services
    Amount: $500.00
    """

    sample_text_prescription = """
    Dr. Smith - Health Clinic
    Patient: Jane Doe
    Date: 03/03/2024
    Rx: Amoxicillin 250mg
    Take one tablet three times a day for 7 days.
    """
    
    sample_text_unknown = "This is a random note about a meeting next Tuesday regarding project updates."

    print("\nTesting Invoice Classification:")
    result_invoice = classifier.classify_text(sample_text_invoice)
    print(f"Invoice Classification Result: {result_invoice}")

    print("\nTesting Prescription Classification:")
    result_prescription = classifier.classify_text(sample_text_prescription)
    print(f"Prescription Classification Result: {result_prescription}")
    
    print("\nTesting Unknown Text Classification:")
    result_unknown = classifier.classify_text(sample_text_unknown)
    print(f"Unknown Text Classification Result: {result_unknown}")
    
    print("\nTesting Empty Text Classification:")
    result_empty = classifier.classify_text("")
    print(f"Empty Text Classification Result: {result_empty}")

    complex_text = """
    Meeting Minutes - Project Phoenix
    Date: 2024-05-10
    Attendees: Alice, Bob, Charlie
    Agenda: Review Q1 performance, Plan Q2 roadmap
    Key Decisions: 
    - Increase marketing budget by 15%.
    - Launch new feature by end of July.
    Action Items: 
    - Alice to draft proposal for budget increase.
    - Bob to finalize feature specs.
    Notes: Discussion on resource allocation for new server infrastructure. Need to follow up with IT department regarding costs and timeline. This might impact the health insurance renewal process if budget is reallocated.
    """
    print("\nTesting Complex Text Classification:")
    result_complex = classifier.classify_text(complex_text)
    print(f"Complex Text Classification Result: {result_complex}")
