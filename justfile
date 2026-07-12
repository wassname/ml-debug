default:
  @just --list

audit:
  python3 scripts/audit.py --self-test .
