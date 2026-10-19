-- Interviews must not be treated as original construction drawings.
CREATE TABLE IF NOT EXISTS historical_interviews (
 interview_id TEXT PRIMARY KEY, interviewee_or_group TEXT NOT NULL, interviewer_or_host TEXT,
 interview_date TEXT, publication_date TEXT, recalled_fair_years TEXT NOT NULL, fair_role TEXT,
 building_or_subject TEXT, research_value TEXT, record_type TEXT NOT NULL, repository TEXT,
 catalog_url TEXT NOT NULL, transcript_access TEXT, audio_access TEXT, source_review TEXT NOT NULL,
 rights_status TEXT NOT NULL, archive_copy_status TEXT NOT NULL, priority TEXT, next_action TEXT
);
CREATE TABLE IF NOT EXISTS oral_history_collections (
 collection_id TEXT PRIMARY KEY, title TEXT NOT NULL, repository TEXT, date TEXT, era_covered TEXT,
 catalog_url TEXT NOT NULL, status TEXT NOT NULL, description TEXT, next_action TEXT
);
CREATE TABLE IF NOT EXISTS interview_claims (
 claim_id TEXT PRIMARY KEY, interview_id TEXT NOT NULL REFERENCES historical_interviews(interview_id),
 linked_asset TEXT, summary TEXT NOT NULL, claim_class TEXT NOT NULL,
 timecode_or_section TEXT, recalled_era TEXT, verification_next TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_interview_claims_source ON interview_claims(interview_id);
