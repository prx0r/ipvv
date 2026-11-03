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
