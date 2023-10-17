import fitz
import io
import requests
from schema import Schema, Literal

from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from llama_index import GPTVectorStoreIndex, Document


def _get_pages_from_pdf(
    url="https://media.wizards.com/2023/downloads/dnd/SRD_CC_v5.1.pdf",
):
    request = requests.get(url)
    filestream = io.BytesIO(request.content)
    pdf = fitz.open(stream=filestream, filetype="pdf")
    page_texts = [
        page.get_text()
        .replace("\xa0", " ")
        .replace("\t", "")
        .replace("\r", "")
        .replace("\n", "")
        for page in pdf
    ]
    return page_texts


INDEX = GPTVectorStoreIndex.from_documents(
    [Document(text=t) for t in _get_pages_from_pdf()]
)


class SRDVectors(BaseTool):
    def __init__(**kwargs):
        super().__init__(**kwargs)
        self.query_engine = INDEX.as_query_engine()

    @activity(
        config={
            "description": "Use this whenever you need information about D&D 5e.",
            "schema": Schema(
                {
                    Literal(
                        "query",
                        description="""A question about D&D 5e.""",
                    ): str,
                }
            ),
        }
    )
    def query_srd_vectors(self, params: dict) -> str:
        query_str = params["values"]["query"]
        return self.query_engine.query(query_str).response
