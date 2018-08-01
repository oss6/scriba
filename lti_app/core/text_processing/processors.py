"""Provides text processing routines."""

from collections import deque

from .document import Document
from .processing_graphs import ProcessorNode
from lti_app.core.exceptions import TextProcessingException


class TextProcessor:
    """Implements a text processor using the graph pattern.

    Args:
        processing_graph (dict):
            The processing graph to use.
        graph_root (ProcessorNode):
            The graph root on which to start processing.
    """

    def __init__(self, processing_graph, graph_root):
        self.graph = processing_graph
        self.graph_root = graph_root

    def _process(self, document, processor, **kwargs):
        out_key = processor.attrs.get('out')

        if not isinstance(processor, ProcessorNode):
            raise TextProcessingException(
                'The processor is not of the correct type.'
            )

        data = processor.process(
            document=document,
            **kwargs
        )
        document.put(out_key, data)

    def run(self, text, **kwargs):
        """Run the processor.

        Args:
            text (str): The raw text to process.

        Returns:
            Document: The processed document.
        """

        document = Document(text)
        marked = []
        queue = deque()

        # Root processing
        self._process(document, self.graph_root, **kwargs)
        queue.append(self.graph_root)
        marked.append(self.graph_root)

        # Visit all reachable processors in the graph
        while len(queue) != 0:
            processor = queue.popleft()

            for next_processor in self.graph.get(processor):
                if next_processor not in marked:
                    self._process(
                        document,
                        next_processor,
                        input_key=processor.attrs.get('out'),
                        **kwargs
                    )

                    marked.append(next_processor)
                    queue.append(next_processor)

        return document