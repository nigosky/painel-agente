# Revisão e possíveis inconsistências

## Conclusão

- Ranking reprocessado desde a primeira partida com sequência final: `1, 2, 2, 4, 5, 6, 7, 8, 8, 8, 8, 12, 13, 14, 15`.
- Não foi encontrada diferença de colocação em relação ao último ranking apresentado antes da inclusão das novas colunas.

## Validações automáticas

- Nenhum problema estrutural encontrado em times, situações ou desafios agendados.

## Observações

- A planilha de situação usa marcadores de último jogo visuais que podem divergir dos marcadores globais gerados pelo script; o script mantém `V#`/`D#` pela ordem cronológica dos resultados homologados.
- A coluna `Status` agora usa `data/situations.csv` como fonte de verdade e não reaproveita status antigos de `data/teams.csv` quando a situação atual está em `Proteção`, `Pode desafiar` ou `Pode ser desafiado`.
- A planilha de situação cita `Infiel / KSxWOS / TJ`, enquanto a base de resultados usa `Infiel / KSxWOS`; o nome da base de resultados foi mantido até confirmação administrativa.
- Confrontos marcados no bloco #8 e #13 estão registrados como batalhas de posição; quando ocorrerem, o perdedor pode cair uma posição se o bloco seguir empatado pelos critérios aplicáveis.
