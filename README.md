# ⚡️ RAGnarok
A **Retrieval-Augmented Generation (RAG)** application built with **FastAPI**, **LangChain**, **Chroma**, **OpenAI**, and **Streamlit**. Users can upload PDF documents, index them into a vector database, and ask natural language questions grounded on the uploaded documents.


## Screenshot
<figure>
  <img src="./images/ragnarok_home_page.png" alt="RAGnarok Home Page">
  <center><figcaption>RAGnarok Home Page</figcaption></center>
</figure>

<figure>
  <img src="./images/ragnarok_upload_page.png" alt="RAGnarok Upload Page">
  <center><figcaption>RAGnarok Upload Page</figcaption></center>
</figure>

<figure>
  <img src="./images/ragnarok_chat_page.png" alt="RAGnarok Chat Page">
  <center><figcaption>RAGnarok Chat Page</figcaption></center>
</figure>

<figure>
  <img src="./images/ragnarok_document_page.png" alt="RAGnarok Document Page">
  <center><figcaption>RAGnarok Document Page</figcaption></center>
</figure>

## Features
- PDF document ingestion
- Automatic text extraction
- Configurable text chunking
- OpenAI embeddings
- Persistent Chroma vector database
- Semantic retrieval
- GPT-powered question answering
- Document management
- Streamlit frontend
- REST API
- Unit and API tests
- GitHub Actions CI

## Architecture
```mermaid
flowchart LR

UI[Streamlit Frontend]

API[FastAPI Backend]

Services[Service Layer]

Repository[Repository Layer]

Chroma[(Chroma)]

OpenAI[OpenAI]

UI --> API

API --> Services

Services --> Repository

Repository --> Chroma

Services --> OpenAI
```

## RAG Flow
```mermaid
flowchart TD

Upload --> PDFParsing --> Chunking --> Embedding --> VectorStore

Question --> SimilaritySearch --> PromptConstruction --> GPT --> Answer
```

## Backend Design

```mermaid
flowchart TD

UploadAPI

ChatAPI

DocumentsAPI

UploadAPI --> IngestionService

ChatAPI --> ChatService

DocumentsAPI --> DocumentService

IngestionService --> PDFService

IngestionService --> ChunkService

IngestionService --> EmbeddingService

EmbeddingService --> ChromaRepository

ChatService --> RetrievalService

ChatService --> PromptService

ChatService --> LLMService

RetrievalService --> ChromaRepository
```

## Frontend Design

```mermaid
flowchart LR

Pages --> FrontendServices --> HTTPClient --> FastAPI

```
