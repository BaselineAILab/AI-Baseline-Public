"""Offline compaction checks; never execute notebook cells or contact model/API services."""
import ast
import __future__
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def helpers():
    notebook = json.loads((ROOT / 'Notebooks/financial_research_pipeline.ipynb').read_text())
    wanted = {'compact_ai_baseline_context', 'compact_ai_baseline_section',
              'compact_evidence_entries', 'extract_agent_context', 'call_ai_baseline',
              'ai_baseline_context_sections'}
    functions = [node for cell in notebook['cells'] if cell['cell_type'] == 'code'
                 for node in ast.parse(''.join(cell['source'])).body
                 if isinstance(node, ast.FunctionDef) and node.name in wanted]
    namespace = {'re': re, 'json': json, 'ANSWER_CONTEXT_MAX_CHARS': 6000,
                 'ANSWER_CONTEXT_PER_SEARCH_MAX_CHARS': 3000,
                 'ANSWER_CONTEXT_MAX_EVIDENCE_ENTRIES_PER_SEARCH': 3,
                 'ANSWER_CONTEXT_SOURCE_REGISTRY_MAX_CHARS': 1000}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(ROOT), 'exec', flags=__future__.annotations.compiler_flag), namespace)
    return namespace


def entry(source='A', content='Supported claim.', identifier='one', refs=None):
    refs = identifier if refs is None else refs
    return (f'<entry sources="{source}"><citations><citation id="{identifier}" source="{source}" '
            f'url="https://basl.ink/a7Km2Qx" /></citations><consensus citations="{refs}">{content}'
            '</consensus></entry>')


def context(entries, sources='<source id="A" title="Complete &amp; original metadata" />', index=1):
    return (f'# AI Baseline search context {index}\nQuery: question\n\n'
            '## Evidence Instructions\nResolve <source_registry> and copy supplied URLs verbatim.\n\n'
            '## Notices\nOne other source link is unavailable.\n\n## Coverage\nPartial evidence.\n\n'
            '## Evidence\n<source_registry>' + sources + '</source_registry>\n' + '\n'.join(entries))


def evidence(value):
    return [ET.fromstring(row) for row in re.findall(r'<entry\b.*?</entry>', value, re.S)]


class NotebookCitationTests(unittest.TestCase):
    def setUp(self):
        self.functions = helpers()

    def compact(self, text, budget=3000):
        return self.functions['compact_ai_baseline_section'](text, budget)

    def test_preserves_provider_instructions_notices_metadata_and_verbatim_links(self):
        original = entry(content='Supported &amp; qualified claim.')
        result = self.compact(context([original]))
        self.assertIn(original, result)
        self.assertIn('Resolve <source_registry> and copy supplied URLs verbatim.', result)
        self.assertIn('One other source link is unavailable.', result)
        self.assertIn('Partial evidence.', result)
        registry = ET.fromstring(re.search(r'^<source_registry>.*?</source_registry>', result, re.S | re.M)[0])
        self.assertEqual(registry[0].attrib['title'], 'Complete & original metadata')
        self.assertEqual(evidence(result)[0].find('citations/citation').attrib['url'], 'https://basl.ink/a7Km2Qx')

    def test_keeps_multiple_passages_and_claim_specific_references_together(self):
        original = ('<entry sources="A B"><citations>'
                    '<citation id="a1" source="A" url="https://basl.ink/a7Km2Qx" />'
                    '<citation id="a2" source="A" url="https://basl.ink/b8Ln3Ry" />'
                    '<citation id="b1" source="B" url="https://basl.ink/c9Mo4Sz" />'
                    '</citations><consensus citations="a1 a2 b1">Combined claim</consensus>'
                    '<additional_context><item citations="a2" sources="A">Narrow context</item>'
                    '</additional_context></entry>')
        result = self.compact(context([original], '<source id="A" /><source id="B" /><source id="Unused" />'))
        self.assertIn(original, result)
        self.assertNotIn('id="Unused"', result)
        self.assertEqual(evidence(result)[0].find('additional_context/item').attrib['citations'], 'a2')

    def test_oversized_first_entry_is_omitted_whole_and_smaller_entry_survives(self):
        result = self.compact(context([entry(content='large' * 1000), entry(identifier='two')]), 900)
        self.assertLessEqual(len(result), 900)
        self.assertEqual(len(evidence(result)), 1)
        self.assertEqual(evidence(result)[0].find('citations/citation').attrib['id'], 'two')
        self.assertIn('Some evidence was omitted', result)
        self.assertNotIn('large', result)

    def test_registry_budget_never_removes_metadata_from_retained_evidence(self):
        self.functions['ANSWER_CONTEXT_SOURCE_REGISTRY_MAX_CHARS'] = 30
        result = self.compact(context([entry()]))
        self.assertEqual(evidence(result), [])
        self.assertIn('Some evidence was omitted', result)

    def test_dangling_references_missing_sources_and_ambiguous_registry_fail_closed(self):
        for original in (entry(refs='missing'), entry(source='Absent')):
            self.assertEqual(evidence(self.compact(context([original]))), [])
        ambiguous = context([entry()], '<source id="A" /><source id="A" />')
        self.assertEqual(evidence(self.compact(ambiguous)), [])

    def test_missing_links_leave_complete_valid_evidence_usable(self):
        original = '<entry sources="A"><citations></citations><consensus citations="">Evidence without a link</consensus></entry>'
        self.assertIn(original, self.compact(context([original])))

    def test_headings_inside_evidence_never_split_context_or_attribution(self):
        for heading in ('## Embedded source heading', '# AI Baseline search context 999: source text',
                        '# Follow-up AI Baseline search context 999'):
            original = entry(content='Supported text.\n' + heading + '\nMore supported text.')
            sections = self.functions['ai_baseline_context_sections'](
                [{'topic': 'Topic', 'query': 'Question', 'agent_context': context([original])}], [])
            result = self.functions['compact_ai_baseline_context'](sections)
            self.assertEqual(len(sections), 1)
            self.assertIn(original, result)
            self.assertEqual(len(evidence(result)), 1)

    def test_real_response_notices_survive_extraction_and_compaction(self):
        response = {'agent_context': {'text': '## Evidence Instructions\nCopy links.\n\n'
                    '## Evidence\n<source_registry><source id="A" /></source_registry>\n' + entry()},
                    'notices': [{'code': 'SOURCE_LINKS_UNAVAILABLE', 'message': 'Some links unavailable.'}]}
        extracted = self.functions['extract_agent_context'](response)
        result = self.compact(extracted)
        self.assertIn('SOURCE_LINKS_UNAVAILABLE', result)
        self.assertIn('Some links unavailable.', result)
        self.assertIn(entry(), result)
        response['notices'] = [None, {'message': 'malformed'}]
        self.assertEqual(self.functions['extract_agent_context'](response), response['agent_context']['text'])

    def test_request_uses_current_include_contract(self):
        self.functions.update(prepare_ai_baseline_query=lambda value: value,
            AI_BASELINE_API_BASE_URL='https://example.invalid/v2', AI_BASELINE_DOMAIN='sandp_500',
            AI_BASELINE_MODE='research', AI_BASELINE_EFFORT='medium',
            AI_BASELINE_TIMEOUT_SECONDS=30, ai_baseline_headers=lambda: {},
            post_json=lambda url, headers, payload, timeout: payload)
        payload = self.functions['call_ai_baseline']('Question')
        self.assertEqual(payload['include'], {'evidence': True, 'evidence_instructions': True,
                                             'agent_context': True, 'summary': True})

    def test_global_budget_never_slices_a_citation_or_instruction_section(self):
        combined = [context([entry()], index=index) for index in range(20)]
        result = self.functions['compact_ai_baseline_context'](combined)
        self.assertLessEqual(len(result), self.functions['ANSWER_CONTEXT_MAX_CHARS'])
        self.assertEqual(result.count('<entry '), result.count('</entry>'))
        self.functions['ANSWER_CONTEXT_MAX_CHARS'] = 5
        self.assertLessEqual(len(self.functions['compact_ai_baseline_context'](combined)), 5)


if __name__ == '__main__':
    unittest.main()
