#!/usr/bin/env python3
"""
spec_parser.py — Extracts structured elements from product specs for audit processing.

Supports: Markdown (.md), plain text (.txt), and basic HTML (.html)
For .docx files: converts to text first using python-docx if available, falls back to raw text.

Usage:
    python spec_parser.py <path_to_spec_file>
    python spec_parser.py <path_to_spec_file> --format json
    python spec_parser.py <path_to_spec_file> --format summary

Output formats:
    text (default) — Human-readable structured extraction
    json           — Machine-readable for further processing
    summary        — One-line-per-field for quick audit prep
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def extract_text(filepath: str) -> str:
    """Extract raw text from the file, handling common formats."""
    path = Path(filepath)
    ext = path.suffix.lower()

    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if ext in ('.md', '.txt', '.text'):
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()

    if ext == '.html':
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        # Strip HTML tags
        content = re.sub(r'<[^>]+>', ' ', content)
        content = re.sub(r'&nbsp;', ' ', content)
        content = re.sub(r'&amp;', '&', content)
        content = re.sub(r'&lt;', '<', content)
        content = re.sub(r'&gt;', '>', content)
        return content

    if ext == '.docx':
        try:
            import docx
            doc = docx.Document(filepath)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return '\n'.join(paragraphs)
        except ImportError:
            print("Note: python-docx not installed. Reading as raw bytes (quality may vary).", file=sys.stderr)
            with open(filepath, 'rb') as f:
                raw = f.read()
            # Extract readable text from docx XML (rough fallback)
            text = raw.decode('utf-8', errors='replace')
            text = re.sub(r'<[^>]+>', ' ', text)
            return text

    # Fallback: try to read as text
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Field extractors
# ---------------------------------------------------------------------------

# Section header patterns — covers common PRD and spec heading styles
SECTION_PATTERNS = {
    'problem_statement': [
        r'(?i)#+\s*(problem\s+statement|problem|background|context|overview|the\s+problem)',
        r'(?i)^\s*(problem\s+statement|problem|background|context)[\s:]+',
    ],
    'success_metrics': [
        r'(?i)#+\s*(success\s+metrics?|metrics?|kpis?|goals?|objectives?|measures?\s+of\s+success)',
        r'(?i)^\s*(success\s+metrics?|metrics?|kpis?|goals?)[\s:]+',
    ],
    'out_of_scope': [
        r'(?i)#+\s*(out\s+of\s+scope|not\s+in\s+scope|exclusions?|non[-\s]goals?)',
        r'(?i)^\s*(out\s+of\s+scope|not\s+in\s+scope|non[-\s]goals?)[\s:]+',
    ],
    'acceptance_criteria': [
        r'(?i)#+\s*(acceptance\s+criteria|requirements?|functional\s+requirements?|user\s+stories?|acs?)',
        r'(?i)^\s*(acceptance\s+criteria|requirements?)[\s:]+',
    ],
    'error_states': [
        r'(?i)#+\s*(error\s+states?|error\s+handling|errors?|failure\s+states?|edge\s+cases?)',
        r'(?i)^\s*(error\s+states?|error\s+handling)[\s:]+',
    ],
    'dependencies': [
        r'(?i)#+\s*(dependencies|technical\s+dependencies?|integrations?|external\s+dependencies?)',
        r'(?i)^\s*(dependencies|integrations?)[\s:]+',
    ],
    'user_actors': [
        r'(?i)#+\s*(users?|user\s+types?|actors?|personas?|roles?|stakeholders?)',
        r'(?i)^\s*(users?|user\s+types?|actors?)[\s:]+',
    ],
    'rollback': [
        r'(?i)#+\s*(rollback|kill\s+switch|feature\s+flags?|rollout|deployment)',
        r'(?i)^\s*(rollback|kill\s+switch)[\s:]+',
    ],
}

# Vague/untestable language patterns
VAGUE_PATTERNS = [
    # Performance
    (r'\b(fast|quickly|quick|snappy|smooth|responsive|instantaneous|real[\s-]time|near[\s-]real[\s-]time|minimal\s+latency)\b',
     'performance descriptor without threshold'),
    # Usability
    (r'\b(intuitive|easy\s+to\s+use|simple|clear|obvious|user[\s-]friendly|discoverable|seamless)\b',
     'usability descriptor (behavior, not feeling)'),
    # Quality
    (r'\b(good|appropriate|proper|correct|accurate|complete|comprehensive|robust|reliable|high[\s-]quality)\b',
     'quality descriptor without measurable standard'),
    # Scope
    (r'\b(all\s+edge\s+cases|all\s+platforms|all\s+user\s+types|all\s+scenarios|handle\s+everything)\b',
     'unbounded scope phrase'),
    # Vague quantity
    (r'\b(several|many|few|some|various|numerous|adequate|sufficient|reasonable)\b',
     'vague quantity without threshold'),
]

# Scope creep risk phrases
SCOPE_RISK_PATTERNS = [
    r'\b(handle\s+all\s+edge\s+cases)\b',
    r'\b(support\s+future\s+extensibility|future[\s-]proof)\b',
    r'\b(integrate\s+with\s+(the\s+)?existing\s+system)\b',
    r'\b(work\s+across\s+all\s+platforms?)\b',
    r'\b(follow\s+best\s+practices?)\b',
    r'\b(be\s+consistent\s+with\s+the\s+rest\s+of\s+(the\s+)?product)\b',
    r'\b(include\s+appropriate\s+error\s+handling)\b',
    r'\b(support\s+all\s+user\s+types?)\b',
    r'\b(make\s+it\s+easy\s+to\s+add)\b',
    r'\b(handle\s+large\s+amounts?\s+of\s+data)\b',
    r'\b(etc\.?|and\s+so\s+on|and\s+more)\b',
]

# Assumption indicator phrases
ASSUMPTION_PATTERNS = [
    (r'\b(pull\s+from|fetch\s+from|use\s+the\s+existing|from\s+the\s+(current|existing))\b', 'system behavior assumption'),
    (r"\b(user'?s?\s+(purchase|order|billing|payment|profile|account|history|data))\b", 'data availability assumption'),
    (r'\b(if\s+(the\s+)?user\s+has\s+permission|users?\s+with\s+access|authorized\s+users?)\b', 'permission assumption'),
    (r'\b(on\s+(mobile|desktop|all\s+devices|all\s+browsers?))\b', 'platform assumption'),
    (r'\b(after\s+onboarding|after\s+setup|once\s+configured|when\s+enabled)\b', 'sequence/state assumption'),
    (r'\b(the\s+(existing|current)\s+(api|service|system|database|endpoint))\b', 'integration assumption'),
]

# Legal/compliance risk phrases — triggers a Legal/Compliance priority flag
LEGAL_RISK_PATTERNS = [
    (r'\b(voice\s+clon(e|ing)|biometric|deepfake)\b', 'biometric/voice cloning — check right of publicity and biometric data law'),
    (r'\b(gdpr|ccpa|hipaa|coppa|bipa|pii|personal\s+data)\b', 'data privacy regulation'),
    (r'\b(right\s+of\s+publicity|likeness|impersonat(e|ion))\b', 'right of publicity'),
    (r'\b(payment|billing|pci|stripe|financial\s+data)\b', 'payment/financial data handling'),
    (r'\b(minor|child|under\s+13|under\s+18|parental\s+consent)\b', 'child safety regulation (COPPA/KOSA)'),
    (r'\b(user\s+generated\s+content|ugc|copyright|dmca|takedown)\b', 'copyright/DMCA exposure'),
]


def extract_sections(text: str) -> dict:
    """Split text into labeled sections based on heading patterns."""
    lines = text.split('\n')
    sections = {}
    current_section = 'preamble'
    current_lines = []

    for line in lines:
        matched_section = None
        for section_name, patterns in SECTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, line):
                    matched_section = section_name
                    break
            if matched_section:
                break

        if matched_section:
            if current_lines:
                sections[current_section] = '\n'.join(current_lines).strip()
            current_section = matched_section
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_section] = '\n'.join(current_lines).strip()

    return sections


def find_acceptance_criteria(text: str) -> list:
    """Extract individual acceptance criteria items."""
    criteria = []

    # Look for numbered or bulleted lists in AC sections
    sections = extract_sections(text)
    ac_section = sections.get('acceptance_criteria', '')

    # Also check for "Given/When/Then" format
    given_when_then = re.findall(
        r'(?i)(given\s+.+?\n(?:when\s+.+?\n)?then\s+.+?)(?=\n(?:given|when|scenario|\d+\.|\-|\*)|\Z)',
        text,
        re.DOTALL
    )

    # Numbered items
    numbered = re.findall(r'^\s*\d+[\.\)]\s+(.+?)$', ac_section, re.MULTILINE)

    # Bulleted items
    bulleted = re.findall(r'^\s*[-*•]\s+(.+?)$', ac_section, re.MULTILINE)

    criteria.extend(given_when_then)
    criteria.extend(numbered)
    criteria.extend(bulleted)

    return [c.strip() for c in criteria if len(c.strip()) > 10]


def find_vague_language(text: str) -> list:
    """Find instances of vague or untestable language."""
    findings = []
    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        for pattern, issue_type in VAGUE_PATTERNS:
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                for match in matches:
                    findings.append({
                        'line': i,
                        'text': line.strip(),
                        'match': match if isinstance(match, str) else match[0],
                        'issue_type': issue_type,
                    })

    return findings


def find_scope_risks(text: str) -> list:
    """Find scope creep risk phrases."""
    findings = []
    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        for pattern in SCOPE_RISK_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                match = re.search(pattern, line, re.IGNORECASE)
                findings.append({
                    'line': i,
                    'text': line.strip(),
                    'phrase': match.group(0) if match else '',
                })

    return findings


def find_assumptions(text: str) -> list:
    """Find implicit assumption indicators."""
    findings = []
    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        for pattern, assumption_type in ASSUMPTION_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                match = re.search(pattern, line, re.IGNORECASE)
                findings.append({
                    'line': i,
                    'text': line.strip(),
                    'phrase': match.group(0) if match else '',
                    'assumption_type': assumption_type,
                })

    return findings


def find_legal_risks(text: str) -> list:
    """Find legal and compliance risk indicators."""
    findings = []
    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        for pattern, risk_type in LEGAL_RISK_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                match = re.search(pattern, line, re.IGNORECASE)
                findings.append({
                    'line': i,
                    'text': line.strip(),
                    'phrase': match.group(0) if match else '',
                    'risk_type': risk_type,
                })

    return findings


def find_pronouns_without_referent(text: str) -> list:
    """Find high-risk pronoun usage that may be ambiguous."""
    findings = []
    lines = text.split('\n')

    # Look for "it should", "it will", "it must" where "it" is ambiguous
    pronoun_patterns = [
        r'\bit\s+(should|will|must|can|may|is)\b',
        r'\bthey\s+(should|will|must|can|may|are)\b',
        r'\bthis\s+(should|will|must|can|may|is)\b',
    ]

    for i, line in enumerate(lines, 1):
        for pattern in pronoun_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    'line': i,
                    'text': line.strip(),
                })

    return findings


def check_completeness(sections: dict, acs: list) -> dict:
    """Assess which required fields are present vs. missing."""
    required_fields = {
        'problem_statement': 'Problem statement',
        'success_metrics': 'Success metrics',
        'out_of_scope': 'Out-of-scope definition',
        'acceptance_criteria': 'Acceptance criteria',
        'error_states': 'Error states',
        'dependencies': 'Dependencies',
        'user_actors': 'User/actor definition',
        'rollback': 'Rollback/kill switch',
    }

    results = {}
    for field_key, field_name in required_fields.items():
        content = sections.get(field_key, '').strip()
        if not content or len(content) < 20:
            results[field_key] = {
                'name': field_name,
                'status': 'MISSING',
                'content_length': len(content),
            }
        else:
            results[field_key] = {
                'name': field_name,
                'status': 'PRESENT',
                'content_length': len(content),
                'preview': content[:200] + ('...' if len(content) > 200 else ''),
            }

    results['ac_count'] = len(acs)
    return results


def derive_priority_actions(completeness: dict, vague: list, scope_risks: list,
                             assumptions: list, legal_risks: list) -> list:
    """
    Derive up to 3 labeled priority actions ranked by severity.
    Returns a list of (category_label, description) tuples.
    """
    priorities = []

    # Legal/Compliance — highest severity, always surfaces first if present
    if legal_risks:
        unique_risk_types = list(dict.fromkeys(r['risk_type'] for r in legal_risks))
        priorities.append((
            'Legal / Compliance',
            f"{len(legal_risks)} legal/compliance risk indicator(s) detected "
            f"({'; '.join(unique_risk_types[:2])}). Resolve with legal counsel before "
            f"any related sprint begins."
        ))

    # Structural — zero ACs or multiple critical missing fields
    missing_fields = [v['name'] for k, v in completeness.items()
                      if isinstance(v, dict) and v.get('status') == 'MISSING']
    ac_count = completeness.get('ac_count', 0)

    if ac_count == 0 and missing_fields:
        priorities.append((
            'Structural',
            f"Zero acceptance criteria detected and {len(missing_fields)} required "
            f"field(s) missing ({', '.join(missing_fields[:3])}{'...' if len(missing_fields) > 3 else ''}). "
            f"The spec is not buildable as written — add ACs before sprint planning."
        ))
    elif ac_count == 0:
        priorities.append((
            'Structural',
            "Zero acceptance criteria detected. QA cannot write a single test and "
            "engineering cannot know when any feature is done."
        ))
    elif missing_fields:
        critical = [f for f in missing_fields if f in
                    ('Problem statement', 'Acceptance criteria', 'Success metrics')]
        if critical:
            priorities.append((
                'Structural',
                f"Critical field(s) missing: {', '.join(critical)}. "
                f"Engineering will make unbounded assumptions without these."
            ))

    # Sprint Risk — scope risks or high assumption count
    if scope_risks and len(priorities) < 3:
        priorities.append((
            'Sprint Risk',
            f"{len(scope_risks)} scope creep risk phrase(s) and "
            f"{len(assumptions)} implicit assumption indicator(s) detected. "
            f"These will cause mid-sprint scope debates without bounded rewrites."
        ))
    elif vague and len(priorities) < 3:
        priorities.append((
            'Sprint Risk',
            f"{len(vague)} vague/untestable language instance(s) detected. "
            f"QA will be unable to verify these requirements without measurable rewrites."
        ))

    return priorities[:3]


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text_output(filepath: str, sections: dict, acs: list,
                       completeness: dict, vague: list, scope_risks: list,
                       assumptions: list, legal_risks: list) -> str:
    """Format a human-readable audit prep report."""
    lines = []
    lines.append(f"SPEC PARSER OUTPUT")
    lines.append(f"File: {filepath}")
    lines.append(f"{'=' * 60}")

    # Completeness
    lines.append("\n## SECTION DETECTION")
    present = [v['name'] for k, v in completeness.items()
               if isinstance(v, dict) and v.get('status') == 'PRESENT']
    missing = [v['name'] for k, v in completeness.items()
               if isinstance(v, dict) and v.get('status') == 'MISSING']

    lines.append(f"  Sections found ({len(present)}): {', '.join(present) if present else 'none'}")
    lines.append(f"  Sections missing ({len(missing)}): {', '.join(missing) if missing else 'none'}")
    lines.append(f"  Acceptance criteria items detected: {completeness.get('ac_count', 0)}")

    # Legal risks
    lines.append(f"\n## LEGAL / COMPLIANCE RISK INDICATORS ({len(legal_risks)} found)")
    if legal_risks:
        for item in legal_risks[:10]:
            lines.append(f"  Line {item['line']}: [{item['risk_type']}]")
            lines.append(f"    \"{item['text'][:100]}\"")
    else:
        lines.append("  None detected.")

    # Vague language
    lines.append(f"\n## VAGUE LANGUAGE INSTANCES ({len(vague)} found)")
    if vague:
        for item in vague[:20]:  # Cap at 20 to avoid noise
            lines.append(f"  Line {item['line']}: [{item['issue_type']}]")
            lines.append(f"    \"{item['text'][:100]}\"")
    else:
        lines.append("  None detected.")

    # Scope risks
    lines.append(f"\n## SCOPE CREEP RISK PHRASES ({len(scope_risks)} found)")
    if scope_risks:
        for item in scope_risks[:15]:
            lines.append(f"  Line {item['line']}: \"{item['phrase']}\"")
            lines.append(f"    Context: \"{item['text'][:100]}\"")
    else:
        lines.append("  None detected.")

    # Assumptions
    lines.append(f"\n## IMPLICIT ASSUMPTIONS ({len(assumptions)} found)")
    if assumptions:
        for item in assumptions[:15]:
            lines.append(f"  Line {item['line']}: [{item['assumption_type']}]")
            lines.append(f"    \"{item['text'][:100]}\"")
    else:
        lines.append("  None detected.")

    # Acceptance criteria
    lines.append(f"\n## EXTRACTED ACCEPTANCE CRITERIA ({len(acs)} items)")
    if acs:
        for i, ac in enumerate(acs[:30], 1):
            lines.append(f"  {i}. {ac[:200]}")
    else:
        lines.append("  No structured ACs detected. May need manual extraction.")

    # Priority actions
    priorities = derive_priority_actions(completeness, vague, scope_risks, assumptions, legal_risks)
    lines.append(f"\n## RECOMMENDED NEXT ACTIONS (ranked by severity)")
    if priorities:
        for i, (label, desc) in enumerate(priorities, 1):
            lines.append(f"  {i}. [{label}]: {desc}")
    else:
        lines.append("  No critical actions identified. Proceed to full audit.")

    lines.append(f"\n{'=' * 60}")
    lines.append("Parsing complete. Pass this output to the spec auditor for full analysis.")

    return '\n'.join(lines)


def format_json_output(filepath: str, sections: dict, acs: list,
                       completeness: dict, vague: list, scope_risks: list,
                       assumptions: list, legal_risks: list) -> str:
    """Format as JSON for machine processing."""
    priorities = derive_priority_actions(completeness, vague, scope_risks, assumptions, legal_risks)
    output = {
        'file': filepath,
        'sections_detected': {k: v for k, v in sections.items() if k != 'preamble'},
        'completeness': completeness,
        'acceptance_criteria': acs,
        'vague_language_instances': vague,
        'scope_creep_risks': scope_risks,
        'assumption_indicators': assumptions,
        'legal_risk_indicators': legal_risks,
        'recommended_next_actions': [
            {'rank': i + 1, 'category': label, 'description': desc}
            for i, (label, desc) in enumerate(priorities)
        ],
        'summary': {
            'sections_present': len([v for k, v in completeness.items()
                                     if isinstance(v, dict) and v.get('status') == 'PRESENT']),
            'sections_missing': len([v for k, v in completeness.items()
                                     if isinstance(v, dict) and v.get('status') == 'MISSING']),
            'ac_count': len(acs),
            'vague_instances': len(vague),
            'scope_risk_instances': len(scope_risks),
            'assumption_instances': len(assumptions),
            'legal_risk_instances': len(legal_risks),
        }
    }
    return json.dumps(output, indent=2)


def format_summary_output(completeness: dict, vague: list, scope_risks: list,
                           assumptions: list, legal_risks: list) -> str:
    """Labeled, severity-ranked priority actions followed by field status."""
    lines = []

    # Priority actions — ranked, labeled, most severe first
    priorities = derive_priority_actions(completeness, vague, scope_risks, assumptions, legal_risks)
    if priorities:
        lines.append("RECOMMENDED NEXT ACTIONS (highest severity first):")
        for i, (label, desc) in enumerate(priorities, 1):
            lines.append(f"  {i}. [{label}]: {desc}")
        lines.append("")

    # Field presence
    lines.append("FIELD STATUS:")
    for k, v in completeness.items():
        if isinstance(v, dict):
            status_icon = "✅" if v.get('status') == 'PRESENT' else "❌"
            lines.append(f"  {status_icon} {v['name']}: {v.get('status', 'UNKNOWN')}")

    lines.append("")
    lines.append("SIGNAL COUNTS:")
    lines.append(f"  ⚖️  Legal/compliance risk indicators: {len(legal_risks)}")
    lines.append(f"  ⚠️  Vague language instances: {len(vague)}")
    lines.append(f"  ⚠️  Scope creep risk phrases: {len(scope_risks)}")
    lines.append(f"  ⚠️  Assumption indicators: {len(assumptions)}")

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Extract structured elements from a product spec for audit processing.'
    )
    parser.add_argument('filepath', help='Path to the spec file')
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'summary'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    # Extract and parse
    text = extract_text(args.filepath)
    sections = extract_sections(text)
    acs = find_acceptance_criteria(text)
    vague = find_vague_language(text)
    scope_risks = find_scope_risks(text)
    assumptions = find_assumptions(text)
    legal_risks = find_legal_risks(text)
    completeness = check_completeness(sections, acs)

    # Output
    if args.format == 'json':
        print(format_json_output(args.filepath, sections, acs, completeness,
                                 vague, scope_risks, assumptions, legal_risks))
    elif args.format == 'summary':
        print(format_summary_output(completeness, vague, scope_risks,
                                    assumptions, legal_risks))
    else:
        print(format_text_output(args.filepath, sections, acs, completeness,
                                 vague, scope_risks, assumptions, legal_risks))


if __name__ == '__main__':
    main()