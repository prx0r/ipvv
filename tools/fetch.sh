#!/usr/bin/env bash
# fetch.sh — pull any bulk byte from R2 without committing it.
# Usage: bash tools/fetch.sh <r2-key> <out>
# Needs /root/.r2-env (R2_ENDPOINT/R2_ACCESS_KEY/R2_SECRET_KEY).
set -u
KEY="${1:?usage: bash tools/fetch.sh <r2-key> <out>}"
OUT="${2:?usage: bash tools/fetch.sh <r2-key> <out>}"
python3 - "$KEY" "$OUT" <<'PY'
import boto3,sys
key, out = sys.argv[1], sys.argv[2]
env={}
with open('/root/.r2-env') as f:
  for l in f:
    l=l.strip()
    if l and '=' in l and not l.startswith('#'):
      k,v=l.split('=',1); env[k]=v
s3=boto3.client('s3', endpoint_url=env['R2_ENDPOINT'], aws_access_key_id=env['R2_ACCESS_KEY'], aws_secret_access_key=env['R2_SECRET_KEY'], region_name='auto')
bucket='sanskritree' if key.startswith('ipvv-translations/') else 'patala'
s3.download_file(bucket, key, out)
print(f'fetched s3://{bucket}/{key} -> {out}')
PY
