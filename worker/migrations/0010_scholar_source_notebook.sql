-- Private passage references selected by a scholar for essay drafting.
CREATE TABLE IF NOT EXISTS scholar_source_notebook (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, work TEXT NOT NULL, target TEXT NOT NULL,
  projection_sha256 TEXT NOT NULL, note TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS scholar_source_notebook_owner ON scholar_source_notebook(user_id,created_at,id);
