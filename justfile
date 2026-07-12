default:
  @just --list

audit:
  python3 scripts/audit.py --self-test .

benchmark-validate:
  python3 benchmark/validate.py

benchmark-run run_id model workers="4":
  python3 benchmark/run.py --run-id {{run_id}} --model {{model}} --workers {{workers}}

benchmark-score run_id:
  python3 benchmark/score.py --run-id {{run_id}}
