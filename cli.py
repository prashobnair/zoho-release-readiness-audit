import argparse
import json
from pathlib import Path
from audit import compare

def main():
    parser = argparse.ArgumentParser(description='Audit fictional CRM config changes offline')
    parser.add_argument('fixture')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.fixture).read_text(encoding='utf-8'))
        report = compare(data['before'], data['after'])
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Input error: {exc}\n')
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.strict and not report['ready_for_release']:
        parser.exit(2)

if __name__ == '__main__':
    main()
