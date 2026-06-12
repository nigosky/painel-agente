import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class LadderRankerIntegrationTest(unittest.TestCase):
    def test_generates_expected_current_ranking(self):
        subprocess.run([sys.executable, "ladder_ranker.py"], check=True)
        with Path("build/ranking.csv").open(encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(rows[0]["Jogadores"], "Showtaro / Vitor")
        self.assertEqual(rows[0]["Posição"], "1")
        self.assertEqual(rows[0]["Vitórias"], "2")
        self.assertEqual(rows[0]["Win Rate"], "100%")
        self.assertEqual(rows[0]["Batalha por posição"], "batalha pela #1 posição")
        self.assertIn("Proteção", rows[0])
        self.assertIn("Pode desafiar", rows[0])
        self.assertIn("Pode ser desafiado", rows[0])
        self.assertEqual(rows[1]["Jogadores"], "Lion Heart / SaNgar")
        self.assertEqual(rows[1]["Posição"], "2")
        self.assertEqual(rows[1]["Vitórias"], "2")
        self.assertIn("Motivo", rows[0])
        self.assertEqual(
            [row["Posição"] for row in rows],
            ["1", "2", "2", "4", "5", "6", "7", "8", "8", "8", "8", "12", "13", "14", "15"],
        )
        self.assertEqual(rows[2]["Jogadores"], "Hjax / viperking")
        self.assertEqual(rows[2]["Posição"], "2")
        self.assertEqual(rows[2]["Vitórias"], "2")
        self.assertEqual(rows[3]["Jogadores"], "Chacineiro / Alface / Vikitor")
        self.assertEqual(rows[3]["Posição"], "4")
        self.assertEqual(rows[3]["Derrotas"], "1")
        self.assertEqual(rows[4]["Jogadores"], "Lem / vonMises / Cunha")
        self.assertEqual(rows[4]["Posição"], "5")
        self.assertEqual(rows[4]["Vitórias"], "2")
        self.assertEqual(rows[4]["Derrotas"], "1")
        self.assertEqual(rows[4]["Win Rate"], "67%")
        self.assertEqual(rows[5]["Jogadores"], "arc / Gabe")
        self.assertEqual(rows[5]["Posição"], "6")
        self.assertEqual(rows[5]["Vitórias"], "2")
        self.assertEqual(rows[5]["Derrotas"], "2")
        self.assertEqual(rows[5]["Win Rate"], "50%")
        self.assertEqual(rows[5]["Status"], "")
        self.assertEqual(rows[5]["Pode desafiar"], "pode desafiar 3 posições acima")
        self.assertEqual(rows[6]["Jogadores"], "General Winter / Skobadark")
        self.assertEqual(rows[6]["Posição"], "7")
        self.assertEqual(rows[6]["Vitórias"], "1")
        self.assertEqual(rows[6]["Derrotas"], "1")
        self.assertEqual(rows[6]["Status"], "")
        self.assertEqual(rows[6]["Proteção"], "proteção 48 horas sem ser desafiado até sexta-feira")
        self.assertEqual(rows[7]["Posição"], "8")
        self.assertEqual(rows[8]["Posição"], "8")
        self.assertEqual(rows[9]["Jogadores"], "Bineto / nigo")
        self.assertEqual(rows[9]["Posição"], "8")
        self.assertEqual(rows[9]["Derrotas"], "2")
        self.assertEqual(rows[10]["Jogadores"], "gaules / gbytes")
        self.assertEqual(rows[10]["Posição"], "8")
        self.assertEqual(rows[10]["Derrotas"], "2")
        self.assertEqual(rows[11]["Jogadores"], "Sauronzinho/ Dragoness")
        self.assertEqual(rows[11]["Posição"], "12")
        self.assertEqual(rows[11]["Vitórias"], "1")
        self.assertEqual(rows[11]["Derrotas"], "1")
        self.assertEqual(rows[12]["Jogadores"], "Major Bruno / Razi")
        self.assertEqual(rows[12]["Posição"], "13")
        self.assertEqual(rows[12]["Derrotas"], "1")
        self.assertEqual(rows[13]["Jogadores"], "Alekel / Phobbos")
        self.assertEqual(rows[13]["Posição"], "14")
        self.assertEqual(rows[13]["Status"], "partida marcada aguardando agendamento")
        self.assertEqual(rows[13]["Batalha por posição"], "batalha pela #13 posição")
        self.assertEqual(rows[-1]["Jogadores"], "Violante / Phayol")
        self.assertEqual(rows[-1]["Posição"], "15")
        self.assertEqual(rows[-1]["Status"], "inativo")
        self.assertTrue(Path("build/ranking_history.md").exists())
        self.assertTrue(Path("build/ranking_history.csv").exists())
        self.assertTrue(Path("build/audit.md").exists())
        self.assertTrue(Path("build/challenges.md").exists())
        self.assertIn("Nenhum problema estrutural", Path("build/audit.md").read_text(encoding="utf-8"))

    def test_tolerates_short_optional_csv_rows(self):
        from ladder_ranker import read_situations, read_challenges

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            situations_path = root / "situations.csv"
            situations_path.write_text(
                "team,status,protection,can_challenge,can_be_challenged,battle_for\n"
                "Time Sem Campos,,,,\n",
                encoding="utf-8",
            )
            challenges_path = root / "challenges.csv"
            challenges_path.write_text(
                "challenged,challenger,schedule,battle_for\n"
                "Time A,Time B,sexta\n",
                encoding="utf-8",
            )

            situations = read_situations(situations_path)
            challenges = read_challenges(challenges_path)

        self.assertEqual(situations["Time Sem Campos"].battle_for, "*")
        self.assertEqual(challenges[0].battle_for, "")


if __name__ == "__main__":
    unittest.main()
