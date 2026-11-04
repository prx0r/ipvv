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
