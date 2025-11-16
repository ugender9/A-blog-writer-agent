from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from models import Summary
from config import settings
from utils.logging import get_logger

logger = get_logger(__name__)

class SummarizationAgent:
    def __init__(self):
        self.llm = OpenAI(api_key=settings.openai_api_key, model="gpt-3.5-turbo-instruct")

    def summarize(self, document_content: str, document_id: str) -> Summary:
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template="Summarize the following document in a concise manner, highlighting key points:\n\n{text}\n\nSummary:"
        )
        prompt = prompt_template.format(text=document_content[:4000])  # Limit input size
        summary_text = self.llm(prompt).strip()

        # Extract key points (simple split by sentences)
        key_points = [point.strip() for point in summary_text.split('.') if point.strip()][:5]

        summary = Summary(
            document_id=document_id,
            summary_text=summary_text,
            key_points=key_points
        )
        logger.info(f"Summary generated for document: {document_id}")
        return summary
