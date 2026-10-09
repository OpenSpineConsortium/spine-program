<!--
Full title page, source (submitted separately; NOT anonymized). build_packet_src.py renders build/full_title_page.docx.
The journal's list (RSNA_AI_REQUIREMENTS.md, "What is submitted", item 2): title; every author's first and last name,
middle initial, degrees and institution; the originating institution's name and street address; the corresponding
author's telephone, e-mail and postal address; funding; manuscript type; word count of the text; unanonymized
acknowledgments; data sharing statement. Also here: guarantor, conflicts, ethics determination, CRediT roles, ORCID,
writing tools. Word counts are computed at build time by the check_limits.py counter.
-->
# {{TITLE}}

**Manuscript type:** {{fm.article_type}}

**Author:** {{AUTHOR_LINE}}

**Affiliation:** ^1^{{fm.affiliations.0.name}}, {{fm.affiliations.0.city}}

**Originating institution and street address:** {{fm.affiliations.0.name}}, {{fm.institution_street_address}}

**Corresponding author:** {{fm.corresponding_author.name}}; {{fm.affiliations.0.name}}, {{fm.institution_street_address}}; telephone {{fm.corresponding_author.telephone}}; e-mail {{fm.corresponding_author.email}}

**ORCID:** {{fm.orcid}}

**Word count:** text (Introduction through Discussion), {{WORDS_BODY}} words; abstract, {{WORDS_ABSTRACT}} words; {{N_FIGURES}} figures; {{N_TABLES}} tables; {{N_REFS}} references.

**Funding:** {{fm.funding}}

**Conflicts of interest:** {{fm.conflicts_of_interest}} {{fm.industry_support}}

**Guarantor:** {{fm.guarantor}}

**Author contributions (CRediT):** {{CREDIT}}

**Acknowledgments:** {{fm.acknowledgments}}

**Ethics:** {{ETHICS_FULL}}

**Trial registration:** {{fm.trial_registration}}

**Data sharing statement:** {{DATA_SHARING_FULL}}

**Use of writing tools:** {{fm.writing_tools}}
