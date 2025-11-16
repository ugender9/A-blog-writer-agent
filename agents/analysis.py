from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from models import Insight, ExtractedData
from config import settings
from utils.logging import get_logger

logger = get_logger(__name__)

class AnalysisAgent:
    def __init__(self):
        self.llm = OpenAI(api_key=settings.openai_api_key, model="gpt-3.5-turbo-instruct")

    def analyze(self, extracted_data: ExtractedData, document_content: str, document_id: str) -> Insight:
        prompt_template = PromptTemplate(
            input_variables=["content", "dates", "metrics", "obligations", "entities"],
            template="""
            Based on the following document content and extracted data, provide business insights and recommendations.

            Document Content: {content}

            Extracted Dates: {dates}
            Extracted Metrics: {metrics}
            Extracted Obligations: {obligations}
            Extracted Entities: {entities}

            Insights and Recommendations:
            """
        )
        prompt = prompt_template.format(
            content=document_content[:2000],  # Limit size
            dates=", ".join(extracted_data.dates),
            metrics=str(extracted_data.metrics),
            obligations=", ".join(extracted_data.obligations),
            entities=", ".join(extracted_data.entities)
        )
        response = self.llm(prompt).strip()

        # Split into insights and recommendations (simple heuristic)
        parts = response.split("Recommendations:")
        insights = parts[0].strip().split('\n') if len(parts) > 1 else [response]
        recommendations = parts[1].strip().split('\n') if len(parts) > 1 else []

        insight = Insight(
            document_id=document_id,
            insights=[i.strip() for i in insights if i.strip()],
            recommendations=[r.strip() for r in recommendations if r.strip()]
        )
        logger.info(f"Insights generated for document: {document_id}")
        return insight
