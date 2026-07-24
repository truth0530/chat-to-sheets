# Domain rules — sheet structure

## Columns

| Col | Meaning | Summed? |
|-----|---------|---------|
| A | group: `must` / `optional` / `note` | key |
| B | item label | — |
| C | reference / benchmark | **no** |
| D | residual count / amount | **yes** |
| E | role (title only, no personal names) | — |
| F | status | — |
| G | human check question | — |

## Groups

| Value | In SUMIF on D? |
|-------|----------------|
| must | yes |
| optional | separate sum ok |
| note | **never** via D; put numbers in C |

## Forbidden

- Real personal identifiers  
- Mixing reference totals into residual sums  
- Presenting draft as final official output  

## Quality checklist

- [ ] Header row  
- [ ] Every data row has a group  
- [ ] note rows do not inflate must total  
- [ ] Uncertain cells say `needs review` / `확인 필요`  
