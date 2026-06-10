"""Pydantic v2 input/output models for westlaw_mcp tools."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

# ── Shared ────────────────────────────────────────────────────────────────


class ResponseFormat(str, Enum):
    """Output format for tool responses."""

    MARKDOWN = "markdown"
    JSON = "json"


class PaginationMixin(BaseModel):
    """Shared pagination fields."""

    model_config = ConfigDict(str_strip_whitespace=True)

    limit: int = Field(default=20, ge=1, le=100, description="Max results to return")
    offset: int = Field(default=0, ge=0, description="Results to skip for pagination")
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'",
    )


# ── WestLaw Classic (Playwright) ───────────────────────────────────────


class WestlawClassicSearchInput(PaginationMixin):
    """Input for WestLaw Classic full-database search."""

    query: str = Field(
        ...,
        min_length=2,
        max_length=500,
        description="Search query (supports Westlaw search syntax)",
    )
    content_type: str | None = Field(
        default=None,
        description="Filter by content type: 'cases', 'statutes', 'regulations', 'secondary', or None for all",
    )
    jurisdiction: str | None = Field(
        default=None,
        description="Jurisdiction filter (e.g., 'US-FED', 'US-CA', 'EU', 'UK')",
    )


class WestlawClassicDocInput(BaseModel):
    """Input for retrieving a WestLaw Classic document."""

    model_config = ConfigDict(str_strip_whitespace=True)

    doc_url: str = Field(..., min_length=10, description="Full Westlaw document URL")
    include_full_text: bool = Field(default=True, description="Include full document text")


# ── CourtListener ─────────────────────────────────────────────────────


class CaseSearchInput(PaginationMixin):
    """Input for US case law search via CourtListener."""

    query: str = Field(..., min_length=2, max_length=300, description="Search query for case law")
    court: str | None = Field(default=None, description="Court filter (e.g., 'scotus', 'ca9')")
    date_after: str | None = Field(default=None, description="Filter cases after date (YYYY-MM-DD)")
    date_before: str | None = Field(
        default=None, description="Filter cases before date (YYYY-MM-DD)"
    )


class CaseGetInput(BaseModel):
    """Input for getting a specific case — Westlaw Classic with CourtListener fallback."""

    model_config = ConfigDict(str_strip_whitespace=True)

    cluster_id: str | None = Field(
        default=None, description="CourtListener opinion cluster ID (backward compatible)"
    )
    case_name: str | None = Field(default=None, description="Case name (e.g. 'Roe v. Wade')")
    citation: str | None = Field(default=None, description="Case citation (e.g. '410 U.S. 113')")
    doc_url: str | None = Field(default=None, description="Direct Westlaw or CourtListener URL")

    @model_validator(mode="after")
    def at_least_one(self) -> "CaseGetInput":
        if not any([self.cluster_id, self.case_name, self.citation, self.doc_url]):
            raise ValueError("Provide at least one of: cluster_id, case_name, citation, doc_url")
        return self


# ── Congress.gov ──────────────────────────────────────────────────────


class LegislationSearchInput(PaginationMixin):
    """Input for searching US legislation via Congress.gov."""

    query: str = Field(
        ..., min_length=2, max_length=300, description="Search query for bills/resolutions"
    )
    congress: int | None = Field(
        default=None, ge=1, le=200, description="Congress number (e.g., 118)"
    )
    bill_type: str | None = Field(
        default=None, description="Bill type: 'hr', 's', 'hjres', 'sjres', 'hconres', 'sconres'"
    )


# ── Federal Register ──────────────────────────────────────────────────


class RegulationSearchInput(PaginationMixin):
    """Input for searching Federal Register documents."""

    query: str = Field(..., min_length=2, max_length=300, description="Search query")
    doc_type: str | None = Field(
        default=None,
        description="Document type: 'RULE', 'PRORULE', 'NOTICE', 'PRESDOCU' (executive orders)",
    )
    agency: str | None = Field(
        default=None, description="Agency slug (e.g., 'environmental-protection-agency')"
    )


# ── eCFR ──────────────────────────────────────────────────────────────


class CFRSectionInput(BaseModel):
    """Input for getting a specific CFR section."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: int = Field(..., ge=1, le=50, description="CFR title number (1-50)")
    part: str | None = Field(default=None, description="Part number (e.g., '164' for HIPAA)")
    section: str | None = Field(default=None, description="Section number (e.g., '164.502')")
    query: str | None = Field(default=None, description="Text search within CFR")


# ── EUR-Lex ───────────────────────────────────────────────────────────


class EULawSearchInput(PaginationMixin):
    """Input for searching EU regulations via EUR-Lex."""

    query: str = Field(..., min_length=2, max_length=300, description="Search query for EU law")
    doc_type: str | None = Field(
        default=None,
        description="Document type: 'regulation', 'directive', 'decision'",
    )
    year: int | None = Field(default=None, ge=1950, le=2030, description="Publication year filter")


# ── Unified Search ────────────────────────────────────────────────────


class UnifiedSearchInput(PaginationMixin):
    """Input for cross-source unified search."""

    query: str = Field(
        ..., min_length=2, max_length=500, description="Search query across all sources"
    )
    sources: str | None = Field(
        default=None,
        description="Comma-separated sources to search: 'westlaw,cases,legislation,regulations,cfr,eu'. Default: all",
    )


# ── Taiwan Judicial ───────────────────────────────────────────────────


class TaiwanJudgmentSearchInput(PaginationMixin):
    """Input for searching Taiwan court judgments."""

    query: str = Field(
        ..., min_length=1, max_length=300, description="Search keywords (Chinese or English)"
    )
    court: str | None = Field(
        default=None,
        description="Court filter: 'TPS' (Supreme), 'TPH' (High), 'TPD' (District), 'TPA' (Admin)",
    )
    date_range: str | None = Field(
        default=None, description="Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end)"
    )


class TaiwanStatuteInput(BaseModel):
    """Input for Taiwan statute lookup."""

    model_config = ConfigDict(str_strip_whitespace=True)

    law_name: str = Field(
        ..., min_length=1, max_length=200, description="Name of the law (e.g., '民法', '刑法')"
    )
    article: str | None = Field(
        default=None, description="Specific article number (e.g., '184', '339')"
    )


class TaiwanInterpretationSearchInput(PaginationMixin):
    """Input for searching Taiwan constitutional interpretations."""

    topic: str = Field(
        ..., min_length=1, max_length=300, description="Search topic or keywords"
    )


# ── EU Compliance ─────────────────────────────────────────────────────


class EUComplianceSearchInput(PaginationMixin):
    """Input for searching EU regulations with compliance focus."""

    topic: str = Field(
        ..., min_length=2, max_length=300,
        description="Search topic (e.g., 'data protection', 'artificial intelligence')",
    )
    regulation_type: str | None = Field(
        default=None,
        description="Filter: 'regulation', 'directive', 'decision', 'delegated', 'implementing'",
    )


class EUComplianceArticleInput(BaseModel):
    """Input for getting a specific EU regulation article."""

    model_config = ConfigDict(str_strip_whitespace=True)

    regulation_id: str = Field(
        ..., min_length=2, max_length=100,
        description="CELEX number or short name (e.g., '32016R0679' or 'GDPR')",
    )
    article_num: str = Field(
        ..., min_length=1, max_length=20,
        description="Article number (e.g., '6', '17', '83')",
    )


class EUComplianceCompareInput(BaseModel):
    """Input for comparing two EU regulations."""

    model_config = ConfigDict(str_strip_whitespace=True)

    reg1: str = Field(
        ..., min_length=2, max_length=100,
        description="First regulation (CELEX or short name like 'GDPR')",
    )
    reg2: str = Field(
        ..., min_length=2, max_length=100,
        description="Second regulation (CELEX or short name like 'AI_ACT')",
    )


# ── OECD Tax Treaties ─────────────────────────────────────────────────


class OECDTreatyInput(BaseModel):
    """Input for getting a bilateral tax treaty."""

    model_config = ConfigDict(str_strip_whitespace=True)

    country1: str = Field(
        ..., min_length=2, max_length=3,
        description="First country ISO code (e.g., 'US', 'TW', 'SG')",
    )
    country2: str = Field(
        ..., min_length=2, max_length=3,
        description="Second country ISO code (e.g., 'GB', 'JP', 'DE')",
    )


class OECDModelConventionInput(BaseModel):
    """Input for searching Model Tax Convention articles."""

    model_config = ConfigDict(str_strip_whitespace=True)

    article: str = Field(
        ..., min_length=1, max_length=50,
        description="Article number (e.g., '5' for PE, '7' for Business Profits) or topic",
    )


class OECDMLIStatusInput(BaseModel):
    """Input for checking MLI status."""

    model_config = ConfigDict(str_strip_whitespace=True)

    country: str = Field(
        ..., min_length=2, max_length=3,
        description="Country ISO code (e.g., 'US', 'SG', 'GB')",
    )


# ── SEC EDGAR ─────────────────────────────────────────────────────────


class SECFilingSearchInput(PaginationMixin):
    """Input for searching SEC EDGAR filings."""

    company: str | None = Field(
        default=None, description="Company name or ticker symbol (e.g., 'Apple', 'AAPL')"
    )
    filing_type: str | None = Field(
        default=None,
        description="Filing type (e.g., '10-K', '10-Q', '8-K', 'S-1', 'DEF 14A')",
    )
    date_range: str | None = Field(
        default=None, description="Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end)"
    )
    cik: str | None = Field(
        default=None, description="SEC Central Index Key (10-digit)"
    )


class SECFilingGetInput(BaseModel):
    """Input for getting a specific SEC filing."""

    model_config = ConfigDict(str_strip_whitespace=True)

    accession_number: str = Field(
        ..., min_length=10, max_length=30,
        description="SEC accession number (e.g., '0000320193-23-000106')",
    )


class SECFullTextSearchInput(PaginationMixin):
    """Input for full-text search across SEC filings."""

    query: str = Field(
        ..., min_length=2, max_length=500,
        description="Full-text search query (searches within filing content)",
    )
    filing_type: str | None = Field(
        default=None, description="Filter by filing type (e.g., '10-K', '8-K')"
    )
    date_range: str | None = Field(
        default=None, description="Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end)"
    )


# ── Singapore eLitigation ──────────────────────────────────────────────


class SingaporeCaseSearchInput(PaginationMixin):
    """Input for searching Singapore court judgments."""

    query: str = Field(
        ..., min_length=2, max_length=300, description="Search keywords for case law"
    )
    court: str | None = Field(
        default=None,
        description="Court: 'SGCA' (Appeal), 'SGHC' (High Court), 'SGDC' (District)",
    )
    date_range: str | None = Field(
        default=None, description="Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end)"
    )


class SingaporeJudgmentGetInput(BaseModel):
    """Input for getting a Singapore judgment."""

    model_config = ConfigDict(str_strip_whitespace=True)

    case_id: str = Field(
        ..., min_length=2, max_length=100,
        description="Case ID or neutral citation (e.g., '[2024] SGCA 1')",
    )
