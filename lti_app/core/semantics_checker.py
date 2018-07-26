"""Provides semantics checkers.

A semantic checker must detect the topic
as well as the semantic structure similarity.

Todo:
    - Compound word synonyms
    - Detect idioms
    - Different POS tags

"""

import itertools
import re

from gensim import corpora, models, similarities
from predpatt import PredPatt

from lti_app.core.text_helpers import are_synonyms, clean_text
from lti_app.core.tools import Tools


class Checker:
    """Implements the default semantics checker.

    Args:
        text_document (Document): The text submitted by the student.
        excerpt_document (Document): The assignment's excerpt.
        supporting_excerpts (str): Paraphrase excerpts examples.
    """

    def __init__(self, text_document, excerpt_document, supporting_excerpts):
        self.text_document = text_document
        self.excerpt_document = excerpt_document
        self.supporting_excerpts = (
            [
                line.strip()
                for line in clean_text(supporting_excerpts).splitlines()
                if line.strip() != ''
            ]
            if supporting_excerpts is not None
            else []
        )

        # Load document vectors
        documents = [self.excerpt_document.text] + self.supporting_excerpts
        self.vectors_corpus = self._docs_to_vectors(documents)

        # Load tools
        self.tools = Tools()

    def _docs_to_vectors(self, documents):
        stoplist = set('for a of the and to in'.split())
        texts = [
            [word for word in document.lower().split() if word not in stoplist]
            for document in documents
        ]

        self.dictionary = corpora.Dictionary(texts)

        return [self.dictionary.doc2bow(text) for text in texts]

    def _get_pred_patterns(self, sentences, opts):
        pred_patt = []

        for line in sentences:
            for sentence in line:
                pp = PredPatt.from_constituency(str(sentence), opts=opts)
                for predicate in pp.instances:
                    pred_patt.append({
                        'target': predicate,
                        'args': predicate.arguments
                    })

        return pred_patt

    def _is_target_negated(self, target):
        tokens = [token.text for token in target.tokens]
        return 'not' in tokens or "n't" in tokens

    def _tuple_similarity(self, t1, t2):
        similarity = 0.0
        weight_target = 1.7
        weight_arg = 1
        num_args_shared = 0

        target1 = self.tools.stemmer.stem(t1['target'].root.text)
        args1 = t1['args']

        target2 = self.tools.stemmer.stem(t2['target'].root.text)
        args2 = t2['args']

        # Reverse arguments if passive voice is used
        if len(args1) == 2 and args1[0].root.gov_rel == 'nsubjpass':
            args1.reverse()

        if len(args2) == 2 and args2[0].root.gov_rel == 'nsubjpass':
            args2.reverse()

        # Check for negation in the predicate
        t1_negated = self._is_target_negated(t1['target'])
        t2_negated = self._is_target_negated(t2['target'])
        negation_mismatch = (
            (t1_negated and not t2_negated) or
            (not t1_negated and t2_negated)
        )

        if (
            not negation_mismatch and
            (target1 == target2 or are_synonyms(target1, target2))
        ):
            similarity += weight_target

        for arg1, arg2 in list(itertools.zip_longest(args1, args2)):
            arg1_text = arg1 and self.tools.stemmer.stem(arg1.root.text)
            arg2_text = arg2 and self.tools.stemmer.stem(arg2.root.text)

            if (
                arg1 is not None
                and arg2 is not None
                and (
                    arg1_text == arg2_text
                    or are_synonyms(arg1_text, arg2_text)
                )
            ):
                similarity += weight_arg
            num_args_shared += 1

        normalization_factor = weight_target + num_args_shared

        return round(similarity / normalization_factor, 2)

    def run(self):
        # 1. Predicate patterns method
        # ----------------------------

        pairs = []
        text_pred_args = self.text_document.get('predicate_patterns')[:]
        excerpt_pred_args = self.excerpt_document.get('predicate_patterns')[:]

        while len(text_pred_args) > 0 and len(excerpt_pred_args) > 0:
            similarity_results = []

            for d_text in text_pred_args:
                for d_excerpt in excerpt_pred_args:
                    similarity = self._tuple_similarity(d_text, d_excerpt)
                    similarity_results.append((d_text, d_excerpt, similarity))

            best_pair = max(similarity_results, key=lambda item: item[2])

            pairs.append(best_pair)

            text_pred_args.remove(best_pair[0])
            excerpt_pred_args.remove(best_pair[1])

        if len(pairs) == 0:
            return 0

        pp_method_result = sum([sim for _, _, sim in pairs]) / len(pairs)

        # 2. Vector similarity method
        # ---------------------------

        tfidf = models.TfidfModel(self.vectors_corpus)
        index = similarities.SparseMatrixSimilarity(
            tfidf[self.vectors_corpus],
            num_features=len(self.dictionary)
        )
        vec = self.dictionary.doc2bow(self.text_document.text.lower().split())

        sims = index[tfidf[vec]]

        vs_method_result = sum(sims) / len(sims)

        return (pp_method_result + vs_method_result) / 2
