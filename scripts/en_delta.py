# -*- coding: utf-8 -*-
"""增補翻譯包（D01…）：用法同 en_units.py：check D01|all / fixheb D01 / show D01。輸出寫 en/out/Dxx.txt"""
import json,sys
sys.path.insert(0,'scripts')
import en_units as U
_L=U.L
def L(p):
    if p=='en/units.json': return {str(i):s for i,s in enumerate(_L('en/delta_units.json'))}
    if p=='en/packs.json': return _L('en/delta_packs.json')
    return _L(p)
U.L=L
if __name__=='__main__':
    c=sys.argv[1]
    if c=='show': print(open(f'en/delta_in/{sys.argv[2]}.txt',encoding='utf-8').read())
    elif c=='fixheb': U.fixheb(sys.argv[2])
    elif c=='check':
        pks=list(L('en/packs.json')) if sys.argv[2]=='all' else sys.argv[2:]
        for pk in pks:
            e=U.check_pack(pk); print(pk,'✓ 通過' if not e else '✗'); [print('  ',x) for x in e]
