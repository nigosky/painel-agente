const STORAGE_KEY = "coh3-ladder-dashboard-v1";
const RANKING_HEADERS = [
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
];

const DEFAULT_STATE = {
  teams: [
    { team: "Chacineiro / Alface / Vikitor", status: "partida marcada aguardando agendamento" },
    { team: "Lion Heart / SaNgar", status: "partida sexta às 21 horas" },
    { team: "Hjax / viperking", status: "partida domingo às 19:30" },
    { team: "Showtaro / Vitor", status: "partida marcada aguardando agendamento" },
    { team: "Lem / vonMises / Cunha", status: "partida domingo às 19:30" },
    { team: "arc / Gabe", status: "partida sábado às 20 horas" },
    { team: "Maití / meuqsaco", status: "partida marcada aguardando agendamento" },
    { team: "gaules / gbytes", status: "partida sábado às 20 horas" },
    { team: "Bineto / nigo", status: "partida sexta às 21 horas" },
    { team: "Infiel / KSxWOS", status: "partida marcada aguardando agendamento" },
    { team: "General Winter / Skobadark", status: "pode desafiar acima ou igual" },
    { team: "Major Bruno / Razi", status: "" },
    { team: "Sauronzinho/ Dragoness", status: "" },
    { team: "Alekel / Phobbos", status: "" },
    { team: "Violante / Phayol", status: "inativo" },
  ],
  results: [
    { date: "2026-05-27", challenged: "Maití / meuqsaco", result: "0-1", challenger: "arc / Gabe", map: "Campbell's Convoy" },
    { date: "2026-05-28", challenged: "gaules / gbytes", result: "0-1", challenger: "Lion Heart / SaNgar", map: "Djebel Pass" },
    { date: "2026-05-30", challenged: "Bineto / nigo", result: "0-1", challenger: "Hjax / viperking", map: "Operation Eindhoven" },
    { date: "2026-05-31", challenged: "Infiel / KSxWOS", result: "0-1", challenger: "Showtaro / Vitor", map: "Pachino Farmlands" },
    { date: "2026-06-01", challenged: "arc / Gabe", result: "0-1", challenger: "Chacineiro / Alface / Vikitor", map: "Pachino Farmlands" },
    { date: "2026-06-01", challenged: "General Winter / Skobadark", result: "0-1", challenger: "Lem / vonMises / Cunha", map: "Campbell's Convoy" },
    { date: "2026-06-05", challenged: "Lion Heart / SaNgar", result: "1-0", challenger: "Bineto / nigo", map: "El Alamein" },
    { date: "2026-06-06", challenged: "Chacineiro / Alface / Vikitor", result: "0-1", challenger: "Showtaro / Vitor", map: "El Alamein" },
    { date: "2026-06-06", challenged: "arc / Gabe", result: "1-0", challenger: "gaules / gbytes", map: "Operation Eindhoven" },
    { date: "2026-06-07", challenged: "Lem / vonMises / Cunha", result: "0-1", challenger: "Hjax / viperking", map: "Campbell's Convoy" },
    { date: "2026-06-08", challenged: "Major Bruno / Razi", result: "0-1", challenger: "Sauronzinho/ Dragoness", map: "Campbell's Convoy" },
    { date: "2026-06-10", challenged: "General Winter / Skobadark", result: "1-0", challenger: "Sauronzinho/ Dragoness", map: "El Alamein" },
    { date: "2026-06-11", challenged: "Lem / vonMises / Cunha", result: "1-0", challenger: "arc / Gabe", map: "Elst Outskirts" },
  ],
  situations: [
    { team: "Showtaro / Vitor", status: "partida marcada - domingo às 19:30", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #1 posição" },
    { team: "Lion Heart / SaNgar", status: "partida marcada - segunda-feira às 21 horas", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #2 posição" },
    { team: "Hjax / viperking", status: "partida marcada - domingo às 19:30", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #1 posição" },
    { team: "Chacineiro / Alface / Vikitor", status: "partida marcada - segunda-feira às 21 horas", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #2 posição" },
    { team: "Lem / vonMises / Cunha", status: "", protection: "proteção 48 horas sem ser desafiado até sábado", canChallenge: "pode desafiar 3 posições acima", canBeChallenged: "", battleFor: "*" },
    { team: "arc / Gabe", status: "", protection: "", canChallenge: "pode desafiar 3 posições acima", canBeChallenged: "pode ser desafiado 3 abaixo", battleFor: "*" },
    { team: "General Winter / Skobadark", status: "", protection: "proteção 48 horas sem ser desafiado até sexta-feira", canChallenge: "pode desafiar 3 posições acima", canBeChallenged: "", battleFor: "*" },
    { team: "Maití / meuqsaco", status: "partida marcada - segunda-feira às 21 horas", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #8 posição; perdedor cai uma posição" },
    { team: "Infiel / KSxWOS", status: "partida marcada - segunda-feira às 21 horas", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #8 posição; perdedor cai uma posição" },
    { team: "Bineto / nigo", status: "partida marcada - sexta-feira às 21 horas", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #8 posição; perdedor cai uma posição" },
    { team: "gaules / gbytes", status: "partida marcada - sexta-feira às 21 horas", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #8 posição; perdedor cai uma posição" },
    { team: "Sauronzinho/ Dragoness", status: "", protection: "", canChallenge: "pode desafiar 3 posições acima", canBeChallenged: "pode ser desafiado 3 abaixo", battleFor: "*" },
    { team: "Major Bruno / Razi", status: "partida marcada aguardando agendamento", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #13 posição" },
    { team: "Alekel / Phobbos", status: "partida marcada aguardando agendamento", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "batalha pela #13 posição" },
    { team: "Violante / Phayol", status: "inativo", protection: "", canChallenge: "", canBeChallenged: "", battleFor: "inativo" },
  ],
  challenges: [
    { challenged: "gaules / gbytes", challenger: "Bineto / nigo", schedule: "sexta-feira às 21 horas", battleFor: "batalha pela #8 posição; perdedor cai uma posição devido a estarem em empate" },
    { challenged: "Showtaro / Vitor", challenger: "Hjax / viperking", schedule: "domingo às 19:50 horas", battleFor: "batalha pela #1 posição" },
    { challenged: "Maití / meuqsaco", challenger: "Infiel / KSxWOS", schedule: "segunda-feira às 20 horas", battleFor: "batalha pela #8 posição; perdedor cai uma posição devido a estarem em empate" },
    { challenged: "Lion Heart / SaNgar", challenger: "Chacineiro / Alface / Vikitor", schedule: "segunda-feira às 21 horas", battleFor: "batalha pela #2 posição" },
    { challenged: "Major Bruno / Razi", challenger: "Alekel / Phobbos", schedule: "a confirmar dia e hora", battleFor: "batalha pela #13 posição" },
  ],
};

let state = loadState();
let latestComputed = null;

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function loadState() {
  const saved = localStorage.getItem(STORAGE_KEY);
  return saved ? JSON.parse(saved) : clone(DEFAULT_STATE);
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function teamNames() {
  return state.teams.map((team) => team.team);
}

function parseResult(result) {
  const parts = result.replace(/[–—]/g, "-").split("-").map((part) => Number(part.trim()));
  if (parts.length !== 2 || parts.some((part) => Number.isNaN(part))) {
    throw new Error(`Resultado inválido: ${result}`);
  }
  return parts;
}

function makeStats(team, index) {
  return {
    name: team.team,
    status: team.status || "",
    seedOrder: index,
    wins: 0,
    losses: 0,
    firstPlayed: null,
    lastPlayed: null,
    lastMarker: "Sem jogos",
    inheritedCompetitiveKey: null,
    inheritedReason: "",
    demotedFromKey: null,
    beatenOpponents: new Set(),
    contextualOpponents: new Set(),
  };
}

function games(team) {
  return team.wins + team.losses;
}

function winRate(team) {
  return games(team) ? team.wins / games(team) : 0;
}

function isInactive(team) {
  return (team.status || "").trim().toLowerCase() === "inativo";
}

function dateValue(date) {
  return date ? new Date(`${date}T00:00:00`).getTime() : Number.MAX_SAFE_INTEGER;
}

function contextualStrength(team, teams) {
  if (team.losses) return 0;
  return [...team.contextualOpponents].filter((opponent) => teams.get(opponent)?.wins > 0).length;
}

function competitiveKey(team, teams) {
  if (isInactive(team)) return ["inactive"];
  if (games(team) === 0) return ["to_debut"];
  if (team.inheritedCompetitiveKey) return team.inheritedCompetitiveKey;
  return [contextualStrength(team, teams), Number(winRate(team).toFixed(12)), team.wins, -team.losses];
}

function compareValues(a, b) {
  if (typeof a === "number" && typeof b === "number") return a - b;
  return String(a).localeCompare(String(b), "pt-BR", { sensitivity: "base" });
}

function compareKeys(left, right) {
  const length = Math.max(left.length, right.length);
  for (let index = 0; index < length; index += 1) {
    const comparison = compareValues(left[index] ?? "", right[index] ?? "");
    if (comparison !== 0) return comparison;
  }
  return 0;
}

function sameKey(left, right) {
  return compareKeys(left, right) === 0;
}

function rankKeyAtLeast(left, right) {
  return left.length === 4 && right.length === 4 && compareKeys(left, right) >= 0;
}

function sortKey(team, teams) {
  if (isInactive(team)) return [3, 0, 0, 0, 0, Number.MAX_SAFE_INTEGER, team.seedOrder, team.name.toLowerCase()];
  if (games(team) === 0) return [2, 0, 0, 0, 0, Number.MAX_SAFE_INTEGER, team.seedOrder, team.name.toLowerCase()];
  if (team.inheritedCompetitiveKey) {
    if (sameKey(team.inheritedCompetitiveKey, ["new_entry_played"])) {
      return [1, team.demotedFromKey ? 1 : 0, 0, 0, 0, dateValue(team.lastPlayed), team.seedOrder, team.name.toLowerCase()];
    }
    if (team.inheritedCompetitiveKey.length === 4) {
      const [context, rate, wins, negativeLosses] = team.inheritedCompetitiveKey;
      return [0, -context, -rate, -wins, -negativeLosses, dateValue(team.lastPlayed), team.seedOrder, team.name.toLowerCase()];
    }
    return [2, 0, 0, 0, 0, dateValue(team.lastPlayed), team.seedOrder, team.name.toLowerCase()];
  }
  return [
    0,
    -contextualStrength(team, teams),
    -winRate(team),
    -team.wins,
    team.losses,
    dateValue(team.lastPlayed),
    team.seedOrder,
    team.name.toLowerCase(),
  ];
}

function ensureTeam(teams, name) {
  if (!teams.has(name)) teams.set(name, makeStats({ team: name, status: "" }, teams.size));
  return teams.get(name);
}

function orderedTeams(teams) {
  return [...teams.values()].sort((left, right) => compareKeys(sortKey(left, teams), sortKey(right, teams)));
}

function rankTeams(teams) {
  const ordered = orderedTeams(teams);
  const keyRanks = new Map();
  const keyCounts = new Map();
  ordered.forEach((team, index) => {
    const key = JSON.stringify(competitiveKey(team, teams));
    if (!keyRanks.has(key)) keyRanks.set(key, index + 1);
    if (!team.demotedFromKey) keyCounts.set(key, (keyCounts.get(key) || 0) + 1);
  });

  const ranked = [];
  let previousKey = null;
  let previousRank = 0;
  ordered.forEach((team) => {
    const keyArray = competitiveKey(team, teams);
    const key = JSON.stringify(keyArray);
    if (team.demotedFromKey) {
      const demotedKey = JSON.stringify(team.demotedFromKey);
      if (keyRanks.has(demotedKey)) {
        ranked.push({ rank: keyRanks.get(demotedKey) + (keyCounts.get(demotedKey) || 1), team });
        return;
      }
    }
    const rank = key === previousKey ? previousRank : keyRanks.get(key);
    ranked.push({ rank, team });
    previousKey = key;
    previousRank = rank;
  });
  return ranked;
}

function applyMatch(teams, match, matchNumber) {
  const previousRanks = new Map(rankTeams(teams).map(({ rank, team }) => [team.name, rank]));
  const [left, right] = parseResult(match.result);
  if (left === right) throw new Error(`Empate não suportado na partida ${matchNumber}`);
  const winnerName = left > right ? match.challenged : match.challenger;
  const loserName = left > right ? match.challenger : match.challenged;
  const winner = ensureTeam(teams, winnerName);
  const loser = ensureTeam(teams, loserName);
  const winnerPreviousRank = previousRanks.get(winner.name) || previousRanks.size + 1;
  const loserPreviousRank = previousRanks.get(loser.name) || previousRanks.size + 1;
  const winnerPreviousKey = competitiveKey(winner, teams);
  const loserPreviousKey = competitiveKey(loser, teams);
  const sameLadderBlock = sameKey(winnerPreviousKey, loserPreviousKey);
  const newTeamBlockMatch = sameLadderBlock && sameKey(winnerPreviousKey, ["to_debut"]) && !winner.status.trim() && !loser.status.trim();
  const tiedLadderBlock = winnerName === match.challenger && sameLadderBlock && (!sameKey(winnerPreviousKey, ["to_debut"]) || newTeamBlockMatch);

  winner.wins += 1;
  winner.inheritedCompetitiveKey = newTeamBlockMatch ? ["new_entry_played"] : null;
  if (tiedLadderBlock && sameKey(winnerPreviousKey, ["to_debut"])) winner.inheritedReason = "Venceu estreia; segue no bloco dos novos.";
  else if (tiedLadderBlock) winner.inheritedReason = "Defendeu posição inicial; segue invicto.";
  else if (winnerName === match.challenged && winnerPreviousKey) winner.inheritedReason = `Defendeu posição contra ${loser.name}.`;
  else winner.inheritedReason = "";
  winner.demotedFromKey = null;
  winner.beatenOpponents.add(loser.name);
  if (!tiedLadderBlock) winner.contextualOpponents.add(loser.name);

  loser.losses += 1;
  loser.demotedFromKey = null;
  if (winnerName === match.challenger && (!sameKey(winnerPreviousKey, ["to_debut"]) || newTeamBlockMatch)) {
    loser.inheritedCompetitiveKey = newTeamBlockMatch ? ["new_entry_played"] : winnerPreviousKey;
    if (tiedLadderBlock) {
      loser.demotedFromKey = newTeamBlockMatch ? ["new_entry_played"] : winnerPreviousKey;
      loser.inheritedReason = `Perdeu empate para ${winner.name}; caiu pelo 1224.`;
    } else {
      loser.inheritedReason = `Perdeu posição para ${winner.name}; herdou bloco anterior.`;
    }
  } else if (winnerName === match.challenged && loserPreviousKey) {
    loser.inheritedCompetitiveKey = loserPreviousRank === winnerPreviousRank + 1 && rankKeyAtLeast(loserPreviousKey, competitiveKey(winner, teams)) ? null : loserPreviousKey;
    loser.inheritedReason = `Perdeu desafio para ${winner.name}; posição preservada.`;
  }

  for (const [team, prefix] of [[winner, "V"], [loser, "D"]]) {
    if (!team.firstPlayed || match.date < team.firstPlayed) team.firstPlayed = match.date;
    if (!team.lastPlayed || match.date >= team.lastPlayed) {
      team.lastPlayed = match.date;
      team.lastMarker = `${prefix}#${matchNumber}`;
    }
  }
}

function buildTeams() {
  const teams = new Map(state.teams.map((team, index) => [team.team, makeStats(team, index)]));
  for (const situation of state.situations) {
    if (situation.status?.toLowerCase() === "inativo" && teams.has(situation.team)) teams.get(situation.team).status = "inativo";
  }
  return teams;
}

function compute() {
  const teams = buildTeams();
  const matches = [...state.results].sort((left, right) => `${left.date}`.localeCompare(`${right.date}`));
  matches.forEach((match, index) => applyMatch(teams, match, index + 1));
  const ranked = rankTeams(teams);
  const situations = new Map(state.situations.map((situation) => [situation.team, situation]));
  const rows = ranked.map(({ rank, team }) => {
    const situation = situations.get(team.name) || { battleFor: "*" };
    return {
      rank,
      team: team.name,
      wins: team.wins,
      losses: team.losses,
      winRate: games(team) ? `${Math.round(winRate(team) * 100)}%` : "—",
      last: team.lastMarker,
      status: situation.status || (games(team) === 0 && !isInactive(team) ? "a estrear" : ""),
      protection: situation.protection || "",
      canChallenge: situation.canChallenge || "",
      canBeChallenged: situation.canBeChallenged || "",
      battleFor: situation.battleFor || "*",
      reason: rankReason(team, teams),
    };
  });
  return { rows, audit: audit(rows), history: historySnapshots() };
}

function rankReason(team, teams) {
  const context = contextualStrength(team, teams);
  const beatWinningOpponent = [...team.beatenOpponents].some((opponent) => teams.get(opponent)?.wins > 0);
  if (isInactive(team)) return "Inativo; fica no final.";
  if (games(team) === 0) return "A estrear; acima dos inativos.";
  if (team.inheritedReason) return team.inheritedReason;
  if (context) return "Tomou posição e segue invicto.";
  if (team.losses && beatWinningOpponent) return "Mantém bloco de ladder após troca anterior.";
  if (team.losses === 0 && team.wins > 1) return "Invicto; posição preservada.";
  if (team.losses === 0) return "Invicto 1-0 no bloco.";
  if (team.wins > 0) return "Mantém posição no contexto atual.";
  if (team.losses === 1) return "Sem vitória; ordem visual por data.";
  return "Sem vitória; abaixo por derrotas.";
}

function audit(rows) {
  const rankByTeam = new Map(rows.map((row) => [row.team, row.rank]));
  const knownTeams = new Set(rows.map((row) => row.team));
  const notes = [];
  const counts = new Map();

  for (const situation of state.situations) {
    if (!knownTeams.has(situation.team)) notes.push(`Situação cadastrada para time fora do ranking: ${situation.team}`);
  }
  for (const challenge of state.challenges) {
    counts.set(challenge.challenged, (counts.get(challenge.challenged) || 0) + 1);
    counts.set(challenge.challenger, (counts.get(challenge.challenger) || 0) + 1);
    const missing = [challenge.challenged, challenge.challenger].filter((team) => !knownTeams.has(team));
    if (missing.length) {
      notes.push(`Desafio ${challenge.challenged} x ${challenge.challenger} cita time fora do ranking: ${missing.join(", ")}`);
      continue;
    }
    const challengedRank = rankByTeam.get(challenge.challenged);
    const challengerRank = rankByTeam.get(challenge.challenger);
    if (challengedRank > challengerRank) notes.push(`Desafio ${challenge.challenged} x ${challenge.challenger} aponta desafiado abaixo do desafiante.`);
    else if (challengerRank - challengedRank > 3) notes.push(`Desafio ${challenge.challenged} x ${challenge.challenger} excede o limite de 3 posições acima.`);
  }
  for (const [team, count] of counts) {
    if (count > 1) notes.push(`${team} aparece em ${count} desafios ativos; a regra permite apenas 1.`);
  }
  if (!notes.length) notes.push("Nenhum problema estrutural encontrado em times, situações ou desafios agendados.");
  return notes;
}

function historySnapshots() {
  const teams = buildTeams();
  return [...state.results]
    .sort((left, right) => `${left.date}`.localeCompare(`${right.date}`))
    .map((match, index) => {
      applyMatch(teams, match, index + 1);
      return {
        title: `#${index + 1} — ${match.date} — ${match.challenged} ${match.result} ${match.challenger}`,
        rows: rankTeams(teams).map(({ rank, team }) => ({ rank, team: team.name, wins: team.wins, losses: team.losses, rate: games(team) ? `${Math.round(winRate(team) * 100)}%` : "—" })),
      };
    });
}

function render() {
  try {
    latestComputed = compute();
  } catch (error) {
    document.querySelector("#auditList").innerHTML = `<li class="issue">${error.message}</li>`;
    return;
  }
  renderOptions();
  renderCards();
  renderRanking();
  renderResults();
  renderSituations();
  renderChallenges();
  renderAudit();
  saveState();
}

function renderOptions() {
  const options = teamNames().map((team) => `<option value="${escapeHtml(team)}">${escapeHtml(team)}</option>`).join("");
  document.querySelectorAll("select[name='challenged'], select[name='challenger'], select[name='team']").forEach((select) => {
    const current = select.value;
    select.innerHTML = options;
    if (current) select.value = current;
  });
}

function renderCards() {
  document.querySelector("#teamCount").textContent = state.teams.length;
  document.querySelector("#matchCount").textContent = state.results.length;
  document.querySelector("#battleCount").textContent = state.challenges.length;
  document.querySelector("#auditCount").textContent = latestComputed.audit[0].startsWith("Nenhum") ? "0" : latestComputed.audit.length;
}

function renderTable(elementId, headers, rows) {
  const table = document.querySelector(elementId);
  table.innerHTML = `
    <thead><tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr></thead>
    <tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody>`;
}

function renderRanking() {
  renderTable("#rankingTable", RANKING_HEADERS, latestComputed.rows.map((row) => [
    `<strong>#${row.rank}</strong>`,
    escapeHtml(row.team),
    numeric(row.wins),
    numeric(row.losses),
    `<span class="badge ${row.winRate === "100%" ? "good" : row.winRate === "0%" ? "danger" : "warn"}">${row.winRate}</span>`,
    escapeHtml(row.last),
    escapeHtml(row.status),
    escapeHtml(row.protection),
    escapeHtml(row.canChallenge),
    escapeHtml(row.canBeChallenged),
    escapeHtml(row.battleFor),
    escapeHtml(row.reason),
  ]));
}

function renderResults() {
  renderTable("#resultsTable", ["Data", "Desafiado", "Resultado", "Desafiante", "Mapa", ""], state.results.map((row, index) => [
    escapeHtml(row.date), escapeHtml(row.challenged), escapeHtml(row.result), escapeHtml(row.challenger), escapeHtml(row.map || ""), deleteButton("result", index),
  ]));
}

function renderSituations() {
  renderTable("#situationsTable", ["Time", "Status", "Proteção", "Pode desafiar", "Pode ser desafiado", "Batalha", ""], state.situations.map((row, index) => [
    escapeHtml(row.team), escapeHtml(row.status), escapeHtml(row.protection), escapeHtml(row.canChallenge), escapeHtml(row.canBeChallenged), escapeHtml(row.battleFor), deleteButton("situation", index),
  ]));
}

function renderChallenges() {
  renderTable("#challengesTable", ["Desafiado", "Desafiante", "Agendamento", "Batalha", ""], state.challenges.map((row, index) => [
    escapeHtml(row.challenged), escapeHtml(row.challenger), escapeHtml(row.schedule), escapeHtml(row.battleFor), deleteButton("challenge", index),
  ]));
}

function renderAudit() {
  document.querySelector("#auditList").innerHTML = latestComputed.audit
    .map((note) => `<li class="${note.startsWith("Nenhum") ? "ok" : "issue"}">${escapeHtml(note)}</li>`)
    .join("");
  document.querySelector("#historyList").innerHTML = latestComputed.history.map((snapshot) => `
    <details>
      <summary>${escapeHtml(snapshot.title)}</summary>
      <div class="table-wrap compact">
        <table><thead><tr><th>Posição</th><th>Time</th><th>V</th><th>D</th><th>WR</th></tr></thead>
        <tbody>${snapshot.rows.map((row) => `<tr><td>#${row.rank}</td><td>${escapeHtml(row.team)}</td><td>${row.wins}</td><td>${row.losses}</td><td>${row.rate}</td></tr>`).join("")}</tbody></table>
      </div>
    </details>`).join("");
}

function numeric(value) {
  return `<span class="numeric">${value}</span>`;
}

function deleteButton(kind, index) {
  return `<button class="danger small" data-delete-kind="${kind}" data-delete-index="${index}" type="button">Remover</button>`;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function formValues(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function download(filename, content, type = "text/plain") {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function rankingCsv() {
  const rows = [RANKING_HEADERS, ...latestComputed.rows.map((row) => [
    row.rank, row.team, row.wins, row.losses, row.winRate, row.last, row.status, row.protection, row.canChallenge, row.canBeChallenged, row.battleFor, row.reason,
  ])];
  return rows.map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(",")).join("\n");
}

function setupEvents() {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab, .panel").forEach((element) => element.classList.remove("active"));
      tab.classList.add("active");
      document.querySelector(`#${tab.dataset.tab}`).classList.add("active");
    });
  });

  document.querySelector("#resultForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const values = formValues(event.currentTarget);
    state.results.push(values);
    event.currentTarget.reset();
    render();
  });

  document.querySelector("#situationForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const values = formValues(event.currentTarget);
    const situation = {
      team: values.team,
      status: values.status || "",
      protection: values.protection || "",
      canChallenge: values.canChallenge || "",
      canBeChallenged: values.canBeChallenged || "",
      battleFor: values.battleFor || "*",
    };
    const index = state.situations.findIndex((item) => item.team === situation.team);
    if (index >= 0) state.situations[index] = situation;
    else state.situations.push(situation);
    render();
  });

  document.querySelector("#challengeForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const values = formValues(event.currentTarget);
    state.challenges.push({ challenged: values.challenged, challenger: values.challenger, schedule: values.schedule || "", battleFor: values.battleFor || "" });
    event.currentTarget.reset();
    render();
  });

  document.body.addEventListener("click", (event) => {
    const button = event.target.closest("[data-delete-kind]");
    if (!button) return;
    const collection = { result: "results", situation: "situations", challenge: "challenges" }[button.dataset.deleteKind];
    state[collection].splice(Number(button.dataset.deleteIndex), 1);
    render();
  });

  document.querySelector("#exportState").addEventListener("click", () => download("ladder-dashboard.json", JSON.stringify(state, null, 2), "application/json"));
  document.querySelector("#exportRankingCsv").addEventListener("click", () => download("ranking.csv", rankingCsv(), "text/csv"));
  document.querySelector("#resetState").addEventListener("click", () => {
    state = clone(DEFAULT_STATE);
    render();
  });
  document.querySelector("#importState").addEventListener("change", async (event) => {
    const [file] = event.target.files;
    if (!file) return;
    state = JSON.parse(await file.text());
    render();
  });
}

setupEvents();
render();
