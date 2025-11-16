# Enterprise Agent: Blog Writer Agent

An AI-driven multi-agent platform for automating document interpretation, insight extraction, summarization, and blog writing from enterprise documents.

## Features

- **Multi-Agent Architecture**: Ingestion, Extraction, Summarization, Analysis, Compliance, and Coordinator agents.
- **Document Processing**: Supports PDF and text files.
- **AI-Powered Insights**: Uses OpenAI GPT for summarization, analysis, and blog generation.
- **Security**: JWT-based authentication and RBAC.
- **Compliance Checks**: Built-in governance and risk assessment.
- **API-Driven**: RESTful API for integration with enterprise systems.

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables: Create a `.env` file with `OPENAI_API_KEY=your_key_here`
4. Run the app: `python main.py`

## Usage

- **Authentication**: POST to `/token` with username/password (default: admin/admin).
- **Process Document**: POST to `/process-document` with a file upload (PDF or text).
- **List Documents**: GET to `/documents`.

## API Endpoints

- `POST /token`: Login for access token.
- `POST /process-document`: Upload and process a document.
- `GET /documents`: List processed documents.

## Project Structure

- `agents/`: Agent implementations.
- `models/`: Pydantic data models.
- `utils/`: Logging and security utilities.
- `tests/`: Unit tests.

## Requirements

See `requirements.txt` for dependencies.

## License

MIT License.
