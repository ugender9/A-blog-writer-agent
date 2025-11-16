from agents.ingestion import IngestionAgent
from agents.extraction import ExtractionAgent
from agents.summarization import SummarizationAgent
from agents.analysis import AnalysisAgent
from agents.compliance import ComplianceAgent
from models import Document, ExtractedData, Summary, Insight, ComplianceCheck, BlogPost
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from config import settings
from utils.logging import get_logger

logger = get_logger(__name__)

class CoordinatorAgent:
    def __init__(self):
        self.ingestion = IngestionAgent()
        self.extraction = ExtractionAgent()
        self.summarization = SummarizationAgent()
        self.analysis = AnalysisAgent()
        self.compliance = ComplianceAgent()
        self.llm = OpenAI(api_key=settings.openai_api_key, model="gpt-3.5-turbo-instruct")

    def process_document(self, content: str, filename: str) -> dict:
        # Step 1: Ingest
        doc = self.ingestion.ingest_document(content, filename)

        # Step 2: Extract
        extracted = self.extraction.extract_data(doc.content, doc.id)

        # Step 3: Summarize
        summary = self.summarization.summarize(doc.content, doc.id)

        # Step 4: Analyze
        insight = self.analysis.analyze(extracted, doc.content, doc.id)

        # Step 5: Compliance Check
        compliance = self.compliance.check_compliance(doc.content, doc.id)

        # Step 6: Generate Blog Post
        blog_post = self._generate_blog_post(doc, summary, insight)

        result = {
            "document": doc,
            "extracted_data": extracted,
            "summary": summary,
            "insights": insight,
            "compliance": compliance,
            "blog_post": blog_post
        }
        logger.info(f"Document processing completed for: {doc.id}")
        return result

    def _generate_blog_post(self, doc: Document, summary: Summary, insight: Insight) -> BlogPost:
        prompt_template = PromptTemplate(
            input_variables=["summary", "insights"],
            template="""
            Based on the summary and insights, write a blog post about the document.

            Summary: {summary}
            Insights: {insights}

            Blog Post Title and Content:
            """
        )
        prompt = prompt_template.format(
            summary=summary.summary_text,
            insights="; ".join(insight.insights + insight.recommendations)
        )
        response = self.llm(prompt).strip()

        # Parse title and content (assume first line is title)
        lines = response.split('\n', 1)
        title = lines[0].strip() if lines else "Generated Blog Post"
        content = lines[1].strip() if len(lines) > 1 else response

        blog_post = BlogPost(
            title=title,
            content=content,
            tags=["enterprise", "document", "insights"],
            based_on_document_ids=[doc.id]
        )
        return blog_post
