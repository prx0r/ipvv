-- Structured private reviews and participant-only discussion.
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
