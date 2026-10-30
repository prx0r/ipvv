# works/_TEMPLATE — copy this to start a new translation

```bash
cp -r works/_TEMPLATE works/<newwork>
# then fill in order: work.json -> passages.jsonl -> t1/ -> l0/ -> argmaps/ -> l2/ -> l200/ -> c1/ -> themes.json -> pushing.jsonl
python3 tools/import_work.py --work <newwork>
python3 site/build.py <newwork>   # once import is OK
```

Every file here is the rigid shape from `specs/schema/`. Delete the examples, keep the keys.
Run `import_work.py` after each layer — it blocks on missing provenance, never on style.
