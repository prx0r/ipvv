-- 0014: gate sessions. Receipts for server-scored wheels.
-- A session's key never leaves the server; unlock happens only here.
CREATE TABLE IF NOT EXISTS gate_sessions (
  id          TEXT PRIMARY KEY,      -- svrand token
  user_id     TEXT NOT NULL,
  curriculum  TEXT NOT NULL,         -- 'word' | 'sentence'
  stage       INTEGER NOT NULL,
  items_json  TEXT NOT NULL,         -- the 20 served items, options shuffled, no answers
  key_json    TEXT NOT NULL,         -- {item_id: correct_index|correct_value}
  expires_at  INTEGER NOT NULL,      -- ms epoch
  used        INTEGER NOT NULL DEFAULT 0,
  created_at  INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_gate_sessions_user
  ON gate_sessions(user_id, curriculum);
