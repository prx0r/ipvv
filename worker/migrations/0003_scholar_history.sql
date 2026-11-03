-- Private revision history. The triggers make a snapshot in the same transaction
-- as each successful optimistic save, including writes from future clients.
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
-- Existing drafts have only their current snapshot; older edits cannot be recovered.
INSERT OR IGNORE INTO scholar_document_history
SELECT user_id,id,revision,kind,work,target,layer,title,content_json,updated_at FROM scholar_documents;
