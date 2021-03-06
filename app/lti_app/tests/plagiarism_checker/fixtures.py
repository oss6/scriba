import pytest

from lti_app.core.plagiarism_checker import Checker as PlagiarismChecker
from lti_app.core.text_processing import processing_graphs, processors


@pytest.fixture
def make_plagiarism_checker():
    def _make_plagiarism_checker(text, excerpt):
        text_processor = processors.TextProcessor(
            processing_graphs.default_graph,
            processing_graphs.text_cleaner
        )

        text_document = text_processor.run(text)
        excerpt_document = text_processor.run(excerpt)

        return PlagiarismChecker(text_document, excerpt_document)

    return _make_plagiarism_checker
