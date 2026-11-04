-- Private selected-text comments on the immutable review snapshot.
CREATE TABLE IF NOT EXISTS scholar_review_annotations (
  id TEXT PRIMARY KEY, review_id TEXT NOT NULL, author_id TEXT NOT NULL,
  snapshot_sha256 TEXT NOT NULL, start_offset INTEGER NOT NULL, end_offset INTEGER NOT NULL,
  quote TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL,
  FOREIGN KEY(review_id) REFERENCES scholar_reviews(id)
);
CREATE INDEX IF NOT EXISTS scholar_review_annotations_thread ON scholar_review_annotations(review_id,created_at,id);
