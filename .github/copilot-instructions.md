# Intro
I need an AI agent / agentic workflow which for a large number of photos of documents a) categorizes photo / document (like contractor invoice, health prescription, health insurance information, etc.) and b) stores the images in a folder structure reflecting the categories (like health/prescriptions/ and health/insurance etc.) with appropriate naming and meta data while also making sure that several pages of the same document have the same name with date as prefix and page number as suffix in name (like 2025-04-03_invoice_car_tires_001, 2025-04-03_invoice_car_tires_002, etc.)?

# Guard Rails:
- Always try to use conda for python environment management
- Always use the following python / conda environment: "document_archiver"
- Make sure you fetch the following tutorial as context information since this project will also be a locally running langchain with ollama: https://composio.dev/blog/deep-research-agent-qwen3-using-langgraph-and-ollama/
- Find additional resources on the website https://langchain-ai.github.io/langgraph/ and all sub pages (like for instances https://langchain-ai.github.io/langgraph/how-tos/many-tools/#define-the-tools)

# Document Archiver System
Create a document archiving system using LangChain with Ollama for local LLM serving and open-source OCR for document processing.

## Architecture Overview

Input Images → OCR Processing → LLM Classification → Document Grouping → File Organization

## Tech Stack
1. Core Framework:
  - Python 3.9+
  - LangChain for workflow orchestration
  - Ollama for local LLM serving

2. OCR (locally running, open-source):
  - Docling from Hugging Face for OCR processing: https://github.com/docling-project/docling

3. Additional Libraries:
  - Pillow for image processing
  - PyPDF2/pdf2image for PDF handling
  - PyExifTool for metadata extraction/writing