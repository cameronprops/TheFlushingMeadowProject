-- Future timelines are alternative artworks, not verified historical epochs.
-- The five factual eras remain in eras and all historical evidence retains that FK.
CREATE TABLE IF NOT EXISTS future_scenarios (
  scenario_id TEXT PRIMARY KEY,
  branch_id TEXT NOT NULL,
  year INTEGER NOT NULL CHECK (year IN (2039,2064)),
  title TEXT NOT NULL,
  scenario_class TEXT NOT NULL CHECK (scenario_class IN ('UTOPIAN','DYSTOPIAN')),
  status TEXT NOT NULL CHECK (status IN ('CONCEPT','BLOCKOUT','PROTOTYPE','PRODUCTION','RELEASED')),
  canonical INTEGER NOT NULL DEFAULT 0 CHECK (canonical IN (0,1)),
  site_coordinate_policy TEXT NOT NULL,
  notes TEXT,
  UNIQUE(branch_id,year)
);
CREATE INDEX IF NOT EXISTS ix_future_scenarios_year ON future_scenarios(year);
