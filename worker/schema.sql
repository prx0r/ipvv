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
