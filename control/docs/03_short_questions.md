# Short questions → actions

After the agent has loaded the knowledge system, users may speak briefly.

| User says (examples) | Agent does |
|----------------------|------------|
| S1 채워 줘 / run S1 / demo table | `run_demo_s1.py` or write same structure via API |
| 비워 줘 / clear board | `clear_board.py` |
| 연결 확인해 줘 | `smoke_test.py` |
| 필수 합 얼마야 | read D summary / SUMIF must |
| 안전 교육 행을 확인 필요로 | find safety row, set status, write back |
| 참고랑 필수 합치지 마 | explain C vs D; fix formulas if wrong |
| 표 헤더만 만들어 | write A1 notice + header row only |

## Template for new short questions

Add a row here when you teach a new habit:

```text
| <phrase> | <docs section or script or API range> |
```

That is how the kit **evolves**: knowledge grows, questions get shorter.
