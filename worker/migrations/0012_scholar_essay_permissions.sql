-- Exact published essay versions: author-controlled AI use scopes.
CREATE TABLE IF NOT EXISTS scholar_essay_permissions (
  work TEXT NOT NULL, essay_id TEXT NOT NULL, author_id TEXT NOT NULL,
  allow_answers INTEGER NOT NULL DEFAULT 0 CHECK (allow_answers IN (0,1)),
  allow_drafts INTEGER NOT NULL DEFAULT 0 CHECK (allow_drafts IN (0,1)),
  updated_at TEXT NOT NULL, PRIMARY KEY(work,essay_id)
);
CREATE INDEX IF NOT EXISTS scholar_essay_permissions_author
  ON scholar_essay_permissions(author_id,work);
