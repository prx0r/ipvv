-- A reviewer can amend a report without erasing the prior report.
CREATE TABLE IF NOT EXISTS scholar_review_report_versions (
  review_id TEXT NOT NULL, revision INTEGER NOT NULL, reviewer_id TEXT NOT NULL,
  decision TEXT NOT NULL, summary TEXT NOT NULL, rubric_json TEXT NOT NULL,
  created_at TEXT NOT NULL, PRIMARY KEY(review_id,revision),
  FOREIGN KEY(review_id) REFERENCES scholar_reviews(id)
);
-- Preserve earlier unstructured decisions as reports with no AI permission.
INSERT OR IGNORE INTO scholar_review_reports
  (review_id,reviewer_id,decision,summary,rubric_json,ai_consent,created_at,consent_updated_at)
SELECT id,reviewer_id,decision,COALESCE(reasoning,''),'{}',0,COALESCE(decided_at,created_at),COALESCE(decided_at,created_at)
FROM scholar_reviews WHERE decision IS NOT NULL;
INSERT OR IGNORE INTO scholar_review_report_versions
SELECT review_id,1,reviewer_id,decision,summary,rubric_json,created_at FROM scholar_review_reports;
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
