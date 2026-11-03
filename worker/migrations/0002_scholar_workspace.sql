-- Account-private Scholar documents, revision-bound reviews and sign-offs.
CREATE TABLE IF NOT EXISTS scholar_documents (
  user_id TEXT NOT NULL, id TEXT NOT NULL, kind TEXT NOT NULL, work TEXT NOT NULL,
  target TEXT NOT NULL DEFAULT '', layer TEXT NOT NULL DEFAULT '', title TEXT NOT NULL DEFAULT '',
  content_json TEXT NOT NULL, revision INTEGER NOT NULL, updated_at TEXT NOT NULL,
  PRIMARY KEY(user_id,id), FOREIGN KEY(user_id) REFERENCES profiles(id)
);
CREATE INDEX IF NOT EXISTS scholar_documents_owner_work ON scholar_documents(user_id,work,updated_at);
CREATE TABLE IF NOT EXISTS scholar_reviews (
  id TEXT PRIMARY KEY, owner_id TEXT NOT NULL, reviewer_id TEXT NOT NULL, work TEXT NOT NULL,
  document_id TEXT NOT NULL, revision INTEGER NOT NULL, snapshot_json TEXT NOT NULL,
  snapshot_sha256 TEXT NOT NULL, decision TEXT, reasoning TEXT, created_at TEXT NOT NULL, decided_at TEXT,
  FOREIGN KEY(owner_id) REFERENCES profiles(id), FOREIGN KEY(reviewer_id) REFERENCES profiles(id)
);
CREATE INDEX IF NOT EXISTS scholar_reviews_participants ON scholar_reviews(owner_id,reviewer_id);
CREATE TABLE IF NOT EXISTS scholar_signoffs (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, document_id TEXT NOT NULL, revision INTEGER NOT NULL,
  snapshot_sha256 TEXT NOT NULL, rights TEXT NOT NULL, created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES profiles(id)
);
