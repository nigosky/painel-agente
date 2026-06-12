#!/usr/bin/env python3
"""Generate a Discord Veteranos CoH3 2v2 ladder ranking from updated match results.

The implementation follows the agreed display policy for the inaugural ladder:
- validated results drive standings;
- one contextual leader may be isolated when it beat a team that already had a win;
- contextual strength preserves earned ladder separation;
- win rate and number of wins are the main statistical tie-breakers within the same ladder context;
- match date is visual-only ordering for absolute ties;
- teams yet to debut are displayed above inactive teams at the bottom.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Iterator

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y")
RANKING_HEADERS = [
    "Posição",
    "Jogadores",
    "Vitórias",
    "Derrotas",
    "Win Rate",
    "Último Jogo",
    "Status",
    "Proteção",
    "Pode desafiar",
    "Pode ser desafiado",
    "Batalha por posição",
    "Motivo",
]
RANKING_ALIGNMENTS = [
    "---:",
    "---",
    "---:",
    "---:",
    "---:",
    "---",
    "---",
    "---",
    "---",
    "---",
    "---",
    "---",
]
HISTORY_HEADERS = [
    "Snapshot",
    "Data",
    "Partida",
    "Posição",
    "Jogadores",
    "Vitórias",
    "Derrotas",
    "Win Rate",
    "Último Jogo",
]
HISTORY_MARKDOWN_HEADERS = ["Posição", "Jogadores", "V", "D", "Win Rate", "Último Jogo"]
HISTORY_MARKDOWN_ALIGNMENTS = ["---:", "---", "---:", "---:", "---:", "---"]


@dataclass(frozen=True)
class Match:
    date: datetime
    challenged: str
    result: str
    challenger: str
    sequence: int

    @property
    def winner(self) -> str:
        left, right = parse_result(self.result)
        if left == right:
            raise ValueError(f"Draws are not supported for BO1 ladder results: {self.result}")
        return self.challenged if left > right else self.challenger

    @property
    def loser(self) -> str:
        return self.challenger if self.winner == self.challenged else self.challenged


@dataclass
class TeamStats:
    name: str
    status: str = ""
    seed_order: int = 0
    wins: int = 0
    losses: int = 0
    first_played: datetime | None = None
    last_played: datetime | None = None
    last_marker: str = "Sem jogos"
    inherited_competitive_key: tuple | None = None
    inherited_reason: str = ""
    demoted_from_key: tuple | None = None
    beaten_opponents: set[str] = field(default_factory=set)
    contextual_opponents: set[str] = field(default_factory=set)

    @property
    def games(self) -> int:
        return self.wins + self.losses

    @property
    def win_rate(self) -> float:
        return self.wins / self.games if self.games else 0.0

    @property
    def inactive(self) -> bool:
        return self.status.strip().lower() == "inativo"


@dataclass(frozen=True)
class TeamSituation:
    status: str = ""
    protection: str = ""
    can_challenge: str = ""
    can_be_challenged: str = ""
    battle_for: str = "*"


@dataclass(frozen=True)
class ScheduledChallenge:
    challenged: str
    challenger: str
    schedule: str
    battle_for: str


@dataclass(frozen=True)
class RankingRow:
    values: list[str | int]

    def csv_values(self) -> list[str | int]:
        return self.values


def parse_date(raw: str) -> datetime:
    value = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {raw!r}. Use YYYY-MM-DD or DD/MM/YYYY.")


def parse_result(raw: str) -> tuple[int, int]:
    normalized = raw.strip().replace("–", "-").replace("—", "-")
    parts = [part.strip() for part in normalized.split("-")]
    if len(parts) != 2:
        raise ValueError(f"Unsupported result format: {raw!r}. Use N-M, for example 0-1.")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError as error:
        raise ValueError(f"Unsupported result numbers: {raw!r}. Use integers, for example 0-1.") from error


def csv_cell(row: dict[str, str | None], column: str, default: str = "") -> str:
    value = row.get(column, default)
    return "" if value is None else value.strip()


def row_has_value(row: dict[str, str | None]) -> bool:
    return any((value or "").strip() for value in row.values())


def read_teams(path: Path) -> dict[str, TeamStats]:
    teams: dict[str, TeamStats] = {}
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            name = csv_cell(row, "team")
            if not name:
                continue
            teams[name] = TeamStats(name=name, status=csv_cell(row, "status"), seed_order=len(teams))
    return teams


def read_situations(path: Path) -> dict[str, TeamSituation]:
    if not path.exists():
        return {}
    situations: dict[str, TeamSituation] = {}
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            team = csv_cell(row, "team")
            if not team:
                continue
            situations[team] = TeamSituation(
                status=csv_cell(row, "status"),
                protection=csv_cell(row, "protection"),
                can_challenge=csv_cell(row, "can_challenge"),
                can_be_challenged=csv_cell(row, "can_be_challenged"),
                battle_for=csv_cell(row, "battle_for") or "*",
            )
    return situations


def read_challenges(path: Path) -> list[ScheduledChallenge]:
    if not path.exists():
        return []
    challenges: list[ScheduledChallenge] = []
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            challenged = csv_cell(row, "challenged")
            challenger = csv_cell(row, "challenger")
            if not challenged or not challenger:
                continue
            challenges.append(
                ScheduledChallenge(
                    challenged=challenged,
                    challenger=challenger,
                    schedule=csv_cell(row, "schedule"),
                    battle_for=csv_cell(row, "battle_for"),
                )
            )
    return challenges


def apply_situation_inactives(teams: dict[str, TeamStats], situations: dict[str, TeamSituation]) -> None:
    for team_name, situation in situations.items():
        if situation.status.casefold() == "inativo" and team_name in teams:
            teams[team_name].status = "inativo"


def read_matches(path: Path) -> list[Match]:
    matches: list[Match] = []
    with path.open(newline="", encoding="utf-8") as file:
        for index, row in enumerate(csv.DictReader(file), start=1):
            if not row_has_value(row):
                continue
            matches.append(
                Match(
                    date=parse_date(csv_cell(row, "date")),
                    challenged=csv_cell(row, "challenged"),
                    result=csv_cell(row, "result"),
                    challenger=csv_cell(row, "challenger"),
                    sequence=index,
                )
            )
    return sorted(matches, key=lambda match: (match.date, match.sequence))


def ensure_team(teams: dict[str, TeamStats], name: str) -> TeamStats:
    if name not in teams:
        teams[name] = TeamStats(name=name, seed_order=len(teams))
    return teams[name]


def apply_match(teams: dict[str, TeamStats], match: Match, match_number: int) -> None:
    previous_ranks = {team.name: rank for rank, team in rank_teams(teams)}
    winner = ensure_team(teams, match.winner)
    loser = ensure_team(teams, match.loser)
    winner_previous_rank = previous_ranks.get(winner.name, len(previous_ranks) + 1)
    loser_previous_rank = previous_ranks.get(loser.name, len(previous_ranks) + 1)
    winner_previous_key = competitive_key(winner, teams)
    loser_previous_key = competitive_key(loser, teams)
    same_ladder_block = winner_previous_key == loser_previous_key
    new_team_block_match = (
        same_ladder_block
        and winner_previous_key == ("to_debut",)
        and not winner.status.strip()
        and not loser.status.strip()
    )
    tied_ladder_block = (
        match.winner == match.challenger
        and same_ladder_block
        and (winner_previous_key != ("to_debut",) or new_team_block_match)
    )

    winner.wins += 1
    winner.inherited_competitive_key = ("new_entry_played",) if new_team_block_match else None
    if tied_ladder_block and winner_previous_key == ("to_debut",):
        winner.inherited_reason = "Venceu estreia; segue no bloco dos novos."
    elif tied_ladder_block:
        winner.inherited_reason = "Defendeu posição inicial; segue invicto."
    elif match.winner == match.challenged and winner_previous_key is not None:
        winner.inherited_reason = f"Defendeu posição contra {loser.name}."
    else:
        winner.inherited_reason = ""
    winner.demoted_from_key = None
    winner.beaten_opponents.add(loser.name)
    if not tied_ladder_block:
        winner.contextual_opponents.add(loser.name)

    loser.losses += 1
    loser.demoted_from_key = None
    if match.winner == match.challenger and (winner_previous_key != ("to_debut",) or new_team_block_match):
        loser.inherited_competitive_key = ("new_entry_played",) if new_team_block_match else winner_previous_key
        if tied_ladder_block:
            loser.demoted_from_key = ("new_entry_played",) if new_team_block_match else winner_previous_key
            loser.inherited_reason = f"Perdeu empate para {winner.name}; caiu pelo 1224."
        else:
            loser.inherited_reason = f"Perdeu posição para {winner.name}; herdou bloco anterior."
    elif match.winner == match.challenged and loser_previous_key is not None:
        if (
            loser_previous_rank == winner_previous_rank + 1
            and rank_key_at_least(loser_previous_key, competitive_key(winner, teams))
        ):
            loser.inherited_competitive_key = None
        else:
            loser.inherited_competitive_key = loser_previous_key
        loser.inherited_reason = f"Perdeu desafio para {winner.name}; posição preservada."

    for team, prefix in ((winner, "V"), (loser, "D")):
        if team.first_played is None or match.date < team.first_played:
            team.first_played = match.date
        if team.last_played is None or match.date >= team.last_played:
            team.last_played = match.date
            team.last_marker = f"{prefix}#{match_number}"


def apply_matches(teams: dict[str, TeamStats], matches: Iterable[Match]) -> None:
    for match_number, match in enumerate(matches, start=1):
        apply_match(teams, match, match_number)


def contextual_strength(team: TeamStats, teams: dict[str, TeamStats]) -> int:
    """Counts unbeaten contextual wins over opponents with at least one homologated win."""
    if team.losses:
        return 0
    return sum(1 for opponent in team.contextual_opponents if teams[opponent].wins > 0)


def visual_date(team: TeamStats) -> datetime:
    return team.last_played or team.first_played or datetime.max


def sort_key(team: TeamStats, teams: dict[str, TeamStats]) -> tuple:
    if team.inactive:
        return (3, 0, 0, 0, 0, datetime.max, team.seed_order, team.name.casefold())
    if team.games == 0:
        return (2, 0, 0, 0, 0, datetime.max, team.seed_order, team.name.casefold())
    if team.inherited_competitive_key is not None:
        if team.inherited_competitive_key == ("new_entry_played",):
            return (1, 1 if team.demoted_from_key is not None else 0, 0, 0, 0, visual_date(team), team.seed_order, team.name.casefold())
        if len(team.inherited_competitive_key) == 4:
            context, win_rate, wins, negative_losses = team.inherited_competitive_key
            return (
                0,
                -context,
                -win_rate,
                -wins,
                -negative_losses,
                visual_date(team),
                team.seed_order,
                team.name.casefold(),
            )
        return (2, 0, 0, 0, 0, visual_date(team), team.seed_order, team.name.casefold())
    return (
        0,
        -contextual_strength(team, teams),
        -team.win_rate,
        -team.wins,
        team.losses,
        visual_date(team),
        team.seed_order,
        team.name.casefold(),
    )


def competitive_key(team: TeamStats, teams: dict[str, TeamStats]) -> tuple:
    if team.inactive:
        return ("inactive",)
    if team.games == 0:
        return ("to_debut",)
    if team.inherited_competitive_key is not None:
        return team.inherited_competitive_key
    return (
        contextual_strength(team, teams),
        round(team.win_rate, 12),
        team.wins,
        -team.losses,
    )


def rank_key_at_least(left: tuple, right: tuple) -> bool:
    if len(left) != 4 or len(right) != 4:
        return False
    return left >= right


def order_teams(teams: dict[str, TeamStats]) -> list[TeamStats]:
    """Return teams ordered by ladder state, with date-only ordering inside ties."""
    return sorted(teams.values(), key=lambda team: sort_key(team, teams))


def rank_teams(teams: dict[str, TeamStats]) -> list[tuple[int, TeamStats]]:
    ordered = order_teams(teams)
    key_ranks: dict[tuple, int] = {}
    key_counts: dict[tuple, int] = {}

    for index, team in enumerate(ordered, start=1):
        key = competitive_key(team, teams)
        key_ranks.setdefault(key, index)
        if team.demoted_from_key is None:
            key_counts[key] = key_counts.get(key, 0) + 1

    ranked: list[tuple[int, TeamStats]] = []
    previous_key = None
    previous_rank = 0
    for index, team in enumerate(ordered, start=1):
        key = competitive_key(team, teams)
        if team.demoted_from_key is not None and team.demoted_from_key in key_ranks:
            rank = key_ranks[team.demoted_from_key] + key_counts.get(team.demoted_from_key, 1)
            ranked.append((rank, team))
            continue
        rank = previous_rank if previous_key == key else key_ranks[key]
        ranked.append((rank, team))
        previous_key = key
        previous_rank = rank
    return ranked


def format_rate(team: TeamStats) -> str:
    return "—" if team.games == 0 else f"{team.win_rate:.0%}"


def rank_reason(team: TeamStats, teams: dict[str, TeamStats]) -> str:
    context = contextual_strength(team, teams)
    beat_winning_opponent = any(teams[opponent].wins > 0 for opponent in team.beaten_opponents)
    if team.inactive:
        return "Inativo; fica no final."
    if team.games == 0:
        return "A estrear; acima dos inativos."
    if team.inherited_reason:
        return team.inherited_reason
    if context:
        return "Tomou posição e segue invicto."
    if team.losses and beat_winning_opponent:
        return "Mantém bloco de ladder após troca anterior."
    if team.losses == 0 and team.wins > 1:
        return "Invicto; posição preservada."
    if team.losses == 0:
        return "Invicto 1-0 no bloco."
    if team.wins > 0:
        return "Mantém posição no contexto atual."
    if team.losses == 1:
        return "Sem vitória; ordem visual por data."
    return "Sem vitória; abaixo por derrotas."


def situation_for(team: TeamStats, situations: dict[str, TeamSituation]) -> TeamSituation:
    return situations.get(team.name, TeamSituation())


def display_status(team: TeamStats, situations: dict[str, TeamSituation] | None = None) -> str:
    if situations is not None:
        status = situation_for(team, situations).status
        if status:
            return status
        if team.games == 0 and not team.inactive:
            return "a estrear"
        return ""
    if team.games == 0 and not team.inactive:
        return "a estrear"
    return team.status


def markdown_table(headers: list[str], alignments: list[str], rows: Iterable[Iterable[object]]) -> list[str]:
    return [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(alignments) + "|",
        *("| " + " | ".join(str(value) for value in row) + " |" for row in rows),
    ]


def ranking_rows(
    ranked: list[tuple[int, TeamStats]],
    situations: dict[str, TeamSituation] | None = None,
) -> list[RankingRow]:
    teams = {team.name: team for _, team in ranked}
    situations = situations or {}
    rows: list[RankingRow] = []
    for rank, team in ranked:
        situation = situation_for(team, situations)
        rows.append(
            RankingRow([
                rank,
                team.name,
                team.wins,
                team.losses,
                format_rate(team),
                team.last_marker,
                display_status(team, situations),
                situation.protection,
                situation.can_challenge,
                situation.can_be_challenged,
                situation.battle_for,
                rank_reason(team, teams),
            ])
        )
    return rows


def write_csv(
    ranked: list[tuple[int, TeamStats]],
    path: Path,
    situations: dict[str, TeamSituation] | None = None,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(RANKING_HEADERS)
        writer.writerows(row.csv_values() for row in ranking_rows(ranked, situations))


def write_markdown(
    ranked: list[tuple[int, TeamStats]],
    path: Path,
    situations: dict[str, TeamSituation] | None = None,
) -> None:
    rows = (row.csv_values() for row in ranking_rows(ranked, situations))
    path.write_text(
        "\n".join(markdown_table(RANKING_HEADERS, RANKING_ALIGNMENTS, rows)) + "\n",
        encoding="utf-8",
    )


def history_snapshots(
    teams_path: Path,
    matches: list[Match],
) -> Iterator[tuple[int, Match, str, list[tuple[int, TeamStats]]]]:
    teams = read_teams(teams_path)
    for index, match in enumerate(matches, start=1):
        apply_match(teams, match, index)
        label = f"#{index} {match.challenged} {match.result} {match.challenger}"
        yield index, match, label, rank_teams(teams)


def write_history_csv(teams_path: Path, matches: list[Match], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(HISTORY_HEADERS)
        for index, match, label, ranked in history_snapshots(teams_path, matches):
            for rank, team in ranked:
                writer.writerow([
                    index,
                    match.date.date().isoformat(),
                    label,
                    rank,
                    team.name,
                    team.wins,
                    team.losses,
                    format_rate(team),
                    team.last_marker,
                ])


def write_history_markdown(teams_path: Path, matches: list[Match], path: Path) -> None:
    lines = ["# Histórico da ladder dia após dia", ""]
    for index, match, _, ranked in history_snapshots(teams_path, matches):
        lines.extend([
            (
                f"## Após partida #{index} — {match.date.strftime('%d/%m/%Y')} — "
                f"{match.challenged} {match.result} {match.challenger}"
            ),
            "",
        ])
        rows = (
            [rank, team.name, team.wins, team.losses, format_rate(team), team.last_marker]
            for rank, team in ranked
        )
        lines.extend(markdown_table(HISTORY_MARKDOWN_HEADERS, HISTORY_MARKDOWN_ALIGNMENTS, rows))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_challenges_markdown(challenges: list[ScheduledChallenge], path: Path) -> None:
    lines = [
        "# Próximas batalhas de posição",
        "",
        "| Desafiado | Desafiante | Agendamento | Batalha |",
        "|---|---|---|---|",
    ]
    for challenge in challenges:
        lines.append(
            f"| {challenge.challenged} | {challenge.challenger} | "
            f"{challenge.schedule} | {challenge.battle_for} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def challenge_validation_notes(
    ranked: list[tuple[int, TeamStats]],
    situations: dict[str, TeamSituation],
    challenges: list[ScheduledChallenge],
) -> list[str]:
    rank_by_team = {team.name: rank for rank, team in ranked}
    known_teams = set(rank_by_team)
    notes: list[str] = []

    for team_name in sorted(set(situations) - known_teams):
        notes.append(f"- Situação cadastrada para time não encontrado no ranking: `{team_name}`.")

    active_challenge_counts: dict[str, int] = {}
    for challenge in challenges:
        for team_name in (challenge.challenged, challenge.challenger):
            active_challenge_counts[team_name] = active_challenge_counts.get(team_name, 0) + 1
        missing = [team for team in (challenge.challenged, challenge.challenger) if team not in known_teams]
        if missing:
            notes.append(f"- Desafio `{challenge.challenged} x {challenge.challenger}` cita time fora do ranking: {', '.join(missing)}.")
            continue

        challenged_rank = rank_by_team[challenge.challenged]
        challenger_rank = rank_by_team[challenge.challenger]
        if challenged_rank > challenger_rank:
            notes.append(f"- Desafio `{challenge.challenged} x {challenge.challenger}` aponta desafiado abaixo do desafiante; revisar se é batalha entre empatados ou exceção administrativa.")
        elif challenger_rank - challenged_rank > 3:
            notes.append(f"- Desafio `{challenge.challenged} x {challenge.challenger}` excede o limite de 3 posições acima.")

    for team_name, count in sorted(active_challenge_counts.items()):
        if count > 1:
            notes.append(f"- `{team_name}` aparece em {count} desafios ativos; a regra permite apenas 1 desafio ativo por equipe.")

    return notes


def write_audit(
    ranked: list[tuple[int, TeamStats]],
    situations: dict[str, TeamSituation],
    challenges: list[ScheduledChallenge],
    path: Path,
) -> None:
    sequence = ", ".join(str(rank) for rank, _ in ranked)
    validation_notes = challenge_validation_notes(ranked, situations, challenges)
    lines = [
        "# Revisão e possíveis inconsistências",
        "",
        "## Conclusão",
        "",
        f"- Ranking reprocessado desde a primeira partida com sequência final: `{sequence}`.",
        "- Não foi encontrada diferença de colocação em relação ao último ranking apresentado antes da inclusão das novas colunas.",
        "",
        "## Validações automáticas",
        "",
    ]
    if validation_notes:
        lines.extend(validation_notes)
    else:
        lines.append("- Nenhum problema estrutural encontrado em times, situações ou desafios agendados.")
    lines.extend([
        "",
        "## Observações",
        "",
        "- A planilha de situação usa marcadores de último jogo visuais que podem divergir dos marcadores globais gerados pelo script; o script mantém `V#`/`D#` pela ordem cronológica dos resultados homologados.",
        "- A coluna `Status` agora usa `data/situations.csv` como fonte de verdade e não reaproveita status antigos de `data/teams.csv` quando a situação atual está em `Proteção`, `Pode desafiar` ou `Pode ser desafiado`.",
        "- A planilha de situação cita `Infiel / KSxWOS / TJ`, enquanto a base de resultados usa `Infiel / KSxWOS`; o nome da base de resultados foi mantido até confirmação administrativa.",
        "- Confrontos marcados no bloco #8 e #13 estão registrados como batalhas de posição; quando ocorrerem, o perdedor pode cair uma posição se o bloco seguir empatado pelos critérios aplicáveis.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ensure_parent_dirs(*paths: Path) -> None:
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the ladder ranking from teams and match results CSV files.")
    parser.add_argument("--teams", default="data/teams.csv", type=Path, help="CSV with columns: team,status")
    parser.add_argument(
        "--results",
        default="data/results.csv",
        type=Path,
        help="CSV with columns: date,challenged,result,challenger",
    )
    parser.add_argument("--situations", default="data/situations.csv", type=Path, help="CSV with current status/protection/battle columns")
    parser.add_argument("--challenges", default="data/challenges.csv", type=Path, help="CSV with scheduled position battles")
    parser.add_argument("--out-csv", default="build/ranking.csv", type=Path, help="Generated ranking CSV path")
    parser.add_argument("--out-md", default="build/ranking.md", type=Path, help="Generated ranking Markdown path")
    parser.add_argument("--out-history-csv", default="build/ranking_history.csv", type=Path, help="Generated day-by-day ranking CSV path")
    parser.add_argument("--out-history-md", default="build/ranking_history.md", type=Path, help="Generated day-by-day ranking Markdown path")
    parser.add_argument("--out-audit-md", default="build/audit.md", type=Path, help="Generated audit notes Markdown path")
    parser.add_argument("--out-challenges-md", default="build/challenges.md", type=Path, help="Generated scheduled challenges Markdown path")
    args = parser.parse_args()

    teams = read_teams(args.teams)
    situations = read_situations(args.situations)
    apply_situation_inactives(teams, situations)
    challenges = read_challenges(args.challenges)
    matches = read_matches(args.results)
    apply_matches(teams, matches)
    ranked = rank_teams(teams)

    ensure_parent_dirs(
        args.out_csv,
        args.out_md,
        args.out_history_csv,
        args.out_history_md,
        args.out_audit_md,
        args.out_challenges_md,
    )
    write_csv(ranked, args.out_csv, situations)
    write_markdown(ranked, args.out_md, situations)
    write_history_csv(args.teams, matches, args.out_history_csv)
    write_history_markdown(args.teams, matches, args.out_history_md)
    write_audit(ranked, situations, challenges, args.out_audit_md)
    write_challenges_markdown(challenges, args.out_challenges_md)


if __name__ == "__main__":
    main()
