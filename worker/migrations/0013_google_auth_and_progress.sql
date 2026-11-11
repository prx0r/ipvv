-- Google sign-in (via the shared satsang-auth service) + learner progress.
-- auth_uid is the shared service's uid (opaque, 'u_...'), never an email.
ALTER TABLE profiles ADD COLUMN auth_uid TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS idx_profiles_auth_uid
  ON profiles(auth_uid) WHERE auth_uid IS NOT NULL;

-- Server-scored gate progress. Stage is written only by the server.
CREATE TABLE IF NOT EXISTS learner_progress (
  user_id     TEXT NOT NULL,
  curriculum  TEXT NOT NULL,
  stage       INTEGER NOT NULL DEFAULT 1,
  passed_json TEXT NOT NULL DEFAULT '[]',
  items_json  TEXT NOT NULL DEFAULT '{}',
  updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (user_id, curriculum)
);

-- Every gate attempt is a receipt: what was served, what was answered.
CREATE TABLE IF NOT EXISTS learner_attempts (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL,
  curriculum   TEXT NOT NULL,
  stage        INTEGER NOT NULL,
  items_json   TEXT NOT NULL,
  answers_json TEXT NOT NULL,
  score        INTEGER NOT NULL,
  passed       INTEGER NOT NULL,
  created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_attempts_user ON learner_attempts(user_id, curriculum);
