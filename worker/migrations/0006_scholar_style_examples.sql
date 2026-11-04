-- Author-selected before/after examples, pointing to private revision history.
CREATE TABLE IF NOT EXISTS scholar_style_examples (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, document_id TEXT NOT NULL,
  work TEXT NOT NULL, kind TEXT NOT NULL, layer TEXT NOT NULL,
  before_revision INTEGER NOT NULL, after_revision INTEGER NOT NULL,
  before_sha256 TEXT NOT NULL, after_sha256 TEXT NOT NULL, created_at TEXT NOT NULL,
  UNIQUE(user_id,document_id,before_revision,after_revision)
);
CREATE INDEX IF NOT EXISTS scholar_style_examples_owner ON scholar_style_examples(user_id,created_at);
CREATE TRIGGER IF NOT EXISTS scholar_style_examples_delete AFTER DELETE ON scholar_documents
BEGIN
  DELETE FROM scholar_style_examples WHERE user_id=OLD.user_id AND document_id=OLD.id;
END;
