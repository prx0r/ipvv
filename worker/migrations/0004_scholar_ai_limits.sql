-- Metadata only: never store prompts, audio, model responses, or provider keys.
CREATE TABLE IF NOT EXISTS scholar_ai_usage (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, day TEXT NOT NULL,
  started_at TEXT NOT NULL, expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS scholar_ai_usage_day ON scholar_ai_usage(day);
CREATE INDEX IF NOT EXISTS scholar_ai_usage_account_day ON scholar_ai_usage(user_id,day);
CREATE INDEX IF NOT EXISTS scholar_ai_usage_active ON scholar_ai_usage(expires_at);
