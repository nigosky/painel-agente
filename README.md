# painel-agente

Automação simples para gerar a visualização do ranking da ladder 2v2 de Company of Heroes 3 a partir dos resultados homologados.

## Como atualizar a ladder

1. Cadastre os times base em `data/teams.csv`.
2. Acrescente cada resultado homologado em `data/results.csv`, mantendo as colunas `date`, `challenged`, `result`, `challenger` e, opcionalmente, `map`.
3. Registre a situação operacional atual em `data/situations.csv`, com status, proteção, quem pode desafiar/ser desafiado e batalha por posição.
4. Registre as próximas batalhas marcadas em `data/challenges.csv`.
5. Rode:

```bash
python3 ladder_ranker.py
```

O comando gera:

- `build/ranking.csv`, para copiar para planilha/tela;
- `build/ranking.md`, para conferência em Markdown;
- `build/ranking_history.csv` e `build/ranking_history.md`, com a ladder refeita partida a partida desde o início;
- `build/audit.md`, com observações de revisão e possíveis inconsistências;
- `build/challenges.md`, com as próximas batalhas de posição agendadas;
- as colunas `Status`, `Proteção`, `Pode desafiar`, `Pode ser desafiado`, `Batalha por posição` e `Motivo`, explicando a situação atual de cada time.

Quando `data/situations.csv` existe, a coluna `Status` passa a ser a fonte de situação atual e não herda textos antigos de `data/teams.csv`; informações como proteção e disponibilidade ficam nas colunas próprias.

## Dashboard interativo

Também há um painel web estático em `dashboard/` para gerenciar a ladder pelo navegador. Ele permite:

- cadastrar resultados homologados e recalcular o ranking automaticamente;
- editar status, proteções, quem pode desafiar, quem pode ser desafiado e batalha por posição;
- registrar próximas batalhas/agendamentos;
- visualizar auditoria automática e histórico dia a dia;
- exportar/importar o estado em JSON e baixar o ranking em CSV.

Para abrir localmente:

```bash
python3 -m http.server 8000
```

Depois acesse `http://localhost:8000/dashboard/`. Os dados editados no painel ficam no `localStorage` do navegador até serem exportados ou restaurados.

## Regras implementadas

- Resultados homologados atualizam vitórias, derrotas, último jogo e motivo de posicionamento automaticamente.
- Quando o desafiante vence, o desafiado herda o bloco de posição anterior do desafiante, pois houve troca de ladder.
- Quando o desafiado vence, ele defende a própria posição e o desafiante não pode ultrapassá-lo apenas por estatística pós-jogo.
- Se o confronto ocorre entre times empatados no mesmo bloco, o vencedor invicto preserva sua posição inicial no bloco superior e o perdedor perde uma posição pelo ranking de competição padrão (standard competition ranking / 1224 ranking).
- Uma vitória contextual forte preserva separação de ladder quando um time invicto venceu adversário que já possui vitória homologada.
- O win rate é calculado como `vitórias / jogos disputados` dentro do mesmo contexto de ladder.
- Quando a administração aplica desempate pontual dentro de um bloco, os critérios estatísticos são: win rate, número de vitórias, número de derrotas, total de partidas feitas e confronto direto anterior entre os empatados.
- Em seguida, o total de vitórias separa times com o mesmo contexto e win rate.
- Times com empate competitivo absoluto usam a data do último jogo apenas para ordenação visual; quem jogou antes aparece acima.
- Separações geradas apenas por desempate visual/data não são definitivas: times que estavam empatados nos blocos 2 e 7 podem voltar a compartilhar a mesma posição se igualarem os critérios de desempate nas próximas rodadas.
- O isolamento atual de `General Winter / Skobadark` em 7º decorre do jogo realizado antes dos demais times do antigo bloco 7, não de uma trava permanente de posição.
- Times a estrear ficam abaixo de todos que já jogaram e acima dos inativos; a coluna `Status` exibe `a estrear` para esses times.
- A numeração usa ranking de competição padrão com empates, por exemplo: `1, 2, 2, 4, 5, 6, 7, 8, 8, 8, 8, 12, 13, 14, 15`.
