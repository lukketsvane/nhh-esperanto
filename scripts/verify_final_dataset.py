#!/usr/bin/env python3
"""Verify final dataset statistics."""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data' / 'processed'
df = pd.read_csv(DATA_DIR / 'nhh_esperanto_complete_unified.csv')

print('='*80)
print('FINAL DATASET STATISTICS')
print('='*80)
print(f'Total participants: {len(df)}')
print(f'With conversation data: {df["conversation_id"].notna().sum()}')
print(f'Without conversation data: {df["conversation_id"].isna().sum()}')
print(f'Overall match rate: {df["conversation_id"].notna().sum() / len(df) * 100:.1f}%')

if 'data_status' in df.columns:
    print('\nData sources:')
    for status, count in df['data_status'].value_counts().items():
        print(f'  {status}: {count}')

if 'MatchMethod' in df.columns:
    print('\nMatch methods:')
    for method, count in df['MatchMethod'].value_counts().items():
        print(f'  {method}: {count}')

print('='*80)
