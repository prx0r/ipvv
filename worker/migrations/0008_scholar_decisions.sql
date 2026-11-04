-- Private, author-selected editorial decisions anchored to a saved revision.
CREATE TABLE IF NOT EXISTS scholar_decisions (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, document_id TEXT NOT NULL,
  revision INTEGER NOT NULL, snapshot_sha256 TEXT NOT NULL,
  work TEXT NOT NULL, target TEXT NOT NULL, layer TEXT NOT NULL,
  subject TEXT NOT NULL, before_text TEXT NOT NULL, after_text TEXT NOT NULL,
  reason TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS scholar_decisions_owner ON scholar_decisions(user_id,created_at,id);
CREATE TRIGGER IF NOT EXISTS scholar_decisions_delete AFTER DELETE ON scholar_documents
BEGIN
  DELETE FROM scholar_decisions WHERE user_id=OLD.user_id AND document_id=OLD.id;
END;
