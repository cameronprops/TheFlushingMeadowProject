-- v1.1.1: narrative evidence and source index (fiction is not historical proof).
CREATE TABLE IF NOT EXISTS narrative_literature (
  literature_id TEXT PRIMARY KEY, title TEXT NOT NULL,
  literature_type TEXT NOT NULL, repository_or_author TEXT,
  years TEXT, source_url TEXT, access_status TEXT NOT NULL,
  rights_status TEXT NOT NULL, research_subjects TEXT,
  local_archive_uri TEXT, sha256 TEXT
);
CREATE TABLE IF NOT EXISTS narrative_threads (
  thread_id TEXT PRIMARY KEY, subject TEXT NOT NULL, year_scope TEXT,
  category TEXT, place_id TEXT, literature_id TEXT NOT NULL
    REFERENCES narrative_literature(literature_id),
  source_grounded_summary TEXT NOT NULL, evidence_status TEXT NOT NULL,
  next_action TEXT, event_or_era_date TEXT, fact_or_fiction TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_narrative_source ON narrative_threads(literature_id);
CREATE INDEX IF NOT EXISTS ix_narrative_era ON narrative_threads(year_scope);
