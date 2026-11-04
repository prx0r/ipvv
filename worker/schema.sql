CREATE TABLE IF NOT EXISTS profiles (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE,
  created_at TEXT DEFAULT (datetime('now')),
  password_hash TEXT,          -- PBKDF2-SHA256, 100000 iters (worker cap), b64url bits
  salt TEXT,                   -- hex16
  display_name TEXT,
  orcid TEXT,                  -- filled by the ORCID OAuth leg (AUTH-SETUP.md)
  provider TEXT DEFAULT 'local'  -- local | orcid | google
);

CREATE TABLE IF NOT EXISTS variants (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  work TEXT NOT NULL,
  chunk TEXT NOT NULL,
  style TEXT NOT NULL DEFAULT 'owner',
  text TEXT NOT NULL,
  gate_verdict TEXT,
  accepted INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (user_id) REFERENCES profiles(id)
);

CREATE TABLE IF NOT EXISTS bookmarks (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  work TEXT NOT NULL,
  chunk TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (user_id) REFERENCES profiles(id)
);

-- Keep in sync with migrations/0002_scholar_workspace.sql.
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
-- Keep in sync with migrations/0005_scholar_peer_review.sql.
CREATE TABLE IF NOT EXISTS scholar_review_reports (
  review_id TEXT PRIMARY KEY, reviewer_id TEXT NOT NULL, decision TEXT NOT NULL,
  summary TEXT NOT NULL, rubric_json TEXT NOT NULL, ai_consent INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL, consent_updated_at TEXT NOT NULL,
  FOREIGN KEY(review_id) REFERENCES scholar_reviews(id)
);
CREATE TRIGGER IF NOT EXISTS scholar_review_report_decide AFTER INSERT ON scholar_review_reports
BEGIN
  UPDATE scholar_reviews SET decision=NEW.decision,reasoning=NEW.summary,decided_at=NEW.created_at
  WHERE id=NEW.review_id AND reviewer_id=NEW.reviewer_id AND decision IS NULL;
END;
CREATE TABLE IF NOT EXISTS scholar_review_messages (
  id TEXT PRIMARY KEY, review_id TEXT NOT NULL, author_id TEXT NOT NULL,
  body TEXT NOT NULL, created_at TEXT NOT NULL,
  FOREIGN KEY(review_id) REFERENCES scholar_reviews(id)
);
CREATE INDEX IF NOT EXISTS scholar_review_messages_thread ON scholar_review_messages(review_id,created_at,id);
-- Keep in sync with migrations/0007_scholar_review_versions.sql.
CREATE TABLE IF NOT EXISTS scholar_review_report_versions (
  review_id TEXT NOT NULL, revision INTEGER NOT NULL, reviewer_id TEXT NOT NULL,
  decision TEXT NOT NULL, summary TEXT NOT NULL, rubric_json TEXT NOT NULL,
  created_at TEXT NOT NULL, PRIMARY KEY(review_id,revision),
  FOREIGN KEY(review_id) REFERENCES scholar_reviews(id)
);
CREATE TRIGGER IF NOT EXISTS scholar_report_version_insert AFTER INSERT ON scholar_review_reports
BEGIN
  INSERT OR IGNORE INTO scholar_review_report_versions
  VALUES (NEW.review_id,1,NEW.reviewer_id,NEW.decision,NEW.summary,NEW.rubric_json,NEW.created_at);
END;
CREATE TRIGGER IF NOT EXISTS scholar_report_version_update AFTER UPDATE OF decision,summary,rubric_json ON scholar_review_reports
WHEN NEW.decision<>OLD.decision OR NEW.summary<>OLD.summary OR NEW.rubric_json<>OLD.rubric_json
BEGIN
  INSERT INTO scholar_review_report_versions
  SELECT NEW.review_id,COALESCE(MAX(revision),0)+1,NEW.reviewer_id,NEW.decision,NEW.summary,NEW.rubric_json,NEW.consent_updated_at
  FROM scholar_review_report_versions WHERE review_id=NEW.review_id;
  UPDATE scholar_reviews SET decision=NEW.decision,reasoning=NEW.summary,decided_at=NEW.consent_updated_at WHERE id=NEW.review_id;
END;
CREATE TABLE IF NOT EXISTS scholar_signoffs (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, document_id TEXT NOT NULL, revision INTEGER NOT NULL,
  snapshot_sha256 TEXT NOT NULL, rights TEXT NOT NULL, created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES profiles(id)
);

-- Keep in sync with migrations/0003_scholar_history.sql.
CREATE TABLE IF NOT EXISTS scholar_document_history (
  user_id TEXT NOT NULL, document_id TEXT NOT NULL, revision INTEGER NOT NULL,
  kind TEXT NOT NULL, work TEXT NOT NULL, target TEXT NOT NULL, layer TEXT NOT NULL,
  title TEXT NOT NULL, content_json TEXT NOT NULL, updated_at TEXT NOT NULL,
  PRIMARY KEY(user_id,document_id,revision)
);
CREATE TRIGGER IF NOT EXISTS scholar_history_insert AFTER INSERT ON scholar_documents
BEGIN
  INSERT OR IGNORE INTO scholar_document_history
  VALUES (NEW.user_id,NEW.id,NEW.revision,NEW.kind,NEW.work,NEW.target,NEW.layer,NEW.title,NEW.content_json,NEW.updated_at);
END;
CREATE TRIGGER IF NOT EXISTS scholar_history_update AFTER UPDATE ON scholar_documents
BEGIN
  INSERT OR IGNORE INTO scholar_document_history
  VALUES (NEW.user_id,NEW.id,NEW.revision,NEW.kind,NEW.work,NEW.target,NEW.layer,NEW.title,NEW.content_json,NEW.updated_at);
END;
CREATE TRIGGER IF NOT EXISTS scholar_history_delete AFTER DELETE ON scholar_documents
BEGIN
  DELETE FROM scholar_document_history WHERE user_id=OLD.user_id AND document_id=OLD.id;
END;

-- Keep in sync with migrations/0004_scholar_ai_limits.sql.
CREATE TABLE IF NOT EXISTS scholar_ai_usage (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, day TEXT NOT NULL,
  started_at TEXT NOT NULL, expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS scholar_ai_usage_day ON scholar_ai_usage(day);
CREATE INDEX IF NOT EXISTS scholar_ai_usage_account_day ON scholar_ai_usage(user_id,day);
CREATE INDEX IF NOT EXISTS scholar_ai_usage_active ON scholar_ai_usage(expires_at);

-- Keep in sync with migrations/0006_scholar_style_examples.sql.
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

-- Keep in sync with migrations/0008_scholar_decisions.sql.
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

-- Keep in sync with migrations/0009_scholar_review_annotations.sql.
-- Private selected-text comments on the immutable review snapshot.
CREATE TABLE IF NOT EXISTS scholar_review_annotations (
  id TEXT PRIMARY KEY, review_id TEXT NOT NULL, author_id TEXT NOT NULL,
  snapshot_sha256 TEXT NOT NULL, start_offset INTEGER NOT NULL, end_offset INTEGER NOT NULL,
  quote TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL,
  FOREIGN KEY(review_id) REFERENCES scholar_reviews(id)
);
CREATE INDEX IF NOT EXISTS scholar_review_annotations_thread ON scholar_review_annotations(review_id,created_at,id);

-- Keep in sync with migrations/0010_scholar_source_notebook.sql.
-- Private passage references selected by a scholar for essay drafting.
CREATE TABLE IF NOT EXISTS scholar_source_notebook (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, work TEXT NOT NULL, target TEXT NOT NULL,
  projection_sha256 TEXT NOT NULL, note TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS scholar_source_notebook_owner ON scholar_source_notebook(user_id,created_at,id);

-- Keep in sync with migrations/0011_scholar_source_links.sql.
-- Account-private, typed links between saved source references.
CREATE TABLE IF NOT EXISTS scholar_source_links (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, from_source_id TEXT NOT NULL,
  to_source_id TEXT NOT NULL, relation TEXT NOT NULL, note TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS scholar_source_links_owner ON scholar_source_links(user_id,created_at,id);
CREATE TRIGGER IF NOT EXISTS scholar_source_links_delete AFTER DELETE ON scholar_source_notebook
BEGIN
  DELETE FROM scholar_source_links WHERE user_id=OLD.user_id AND (from_source_id=OLD.id OR to_source_id=OLD.id);
END;

-- Keep in sync with migrations/0012_scholar_essay_permissions.sql.
-- Explicit author grants for an exact published essay, separated by AI use.
CREATE TABLE IF NOT EXISTS scholar_essay_permissions (
  work TEXT NOT NULL, essay_id TEXT NOT NULL, author_id TEXT NOT NULL,
  allow_answers INTEGER NOT NULL DEFAULT 0 CHECK (allow_answers IN (0,1)),
  allow_drafts INTEGER NOT NULL DEFAULT 0 CHECK (allow_drafts IN (0,1)),
  updated_at TEXT NOT NULL, PRIMARY KEY(work,essay_id)
);
CREATE INDEX IF NOT EXISTS scholar_essay_permissions_author
  ON scholar_essay_permissions(author_id,work);

CREATE TABLE IF NOT EXISTS chat_sessions (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  work TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chat_messages (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (session_id) REFERENCES chat_sessions(id)
);
