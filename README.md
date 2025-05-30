# Document Archiver Project

This `README.md` summarizes the development session for the Document Archiver project.

## Project Goal

The overall project goal is to create an AI agent / agentic workflow which for a large number of photos of documents:
a) categorizes photo / document (like contractor invoice, health prescription, health insurance information, etc.) and 
b) stores the images in a folder structure reflecting the categories (like health/prescriptions/ and health/insurance etc.) with appropriate naming and meta data while also making sure that several pages of the same document have the same name with date as prefix and page number as suffix in name (like 2025-04-03_invoice_car_tires_001, 2025-04-03_invoice_car_tires_002, etc.).

## Accomplished Tasks

*   Environment setup.
*   OCR processor implementation.
*   LLM classifier development with robust JSON parsing.

## Current Status and Next Steps

*   **Current Focus:** Verifying the LLM classifier and debugging the OCR processor.
*   **Next Steps:** 
    1.  Proceed with the file organizer implementation.
    2.  Set up the LangGraph for workflow orchestration.

## Relevant File Paths

The following files have been created or modified during the development process:

*   `src/document_archiver/llm_classifier.py`
*   `src/document_archiver/ocr_processor.py` 
*   `requirements.txt`
*   `app.py` 
*   (Potentially others as the project progresses)

