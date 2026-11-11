-- 0015: durable, idempotent gate results.
-- result_json: the graded result, so an identical retry after a lost response
--   returns the SAME receipt instead of a 409 (spec §A).
-- answers_json: canonical submitted answers, so a DIFFERENT replay is refused.
ALTER TABLE gate_sessions ADD COLUMN result_json TEXT;
ALTER TABLE gate_sessions ADD COLUMN answers_json TEXT;
