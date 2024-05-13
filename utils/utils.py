from datetime import UTC, datetime
import os
from re import sub
from dotenv import load_dotenv
import psycopg2

import discord
from unidecode import unidecode

load_dotenv()

DB_URL = os.getenv("NEON_URL")

POINT_GAIN = 1

CHANNEL_ID = 955169257711370280
QUESTION_HEX = 0x1860CC
CORRECT_HEX = 0x3CB556
WRONG_HEX = 0xFA8E23

COUNTRY = 1
TERRITORY = 2
CAPITALS = 11
FLAGS = 12


shortdict = {
    # countries
    "unitedstates": "usa",
    "unitedkingdom": "uk",
    "unitedarabemirates": "uae",
    "northkorea": "nk",
    "southkorea": "sk",
    "newzealand": "nz",
    "republicofthecongo": "roc",
    "drcongo": "drc",
    "dominicanrepublic": "dr",
    "saintvincentandthegrenadines": "svg",
    "papuanewguinea": "png",
    "antiguaandbarbuda": "ab",
    # "saudiarabia": "sa",
    "trinidadandtobago": "tt",
    "bosniaandherzegovina": "bh",
    "saotomeandprincipe": "stp",
    "saintkittsandnevis": "skn",
    "centralafricanrepublic": "car",
    # "guineabissau": "gb",
    # "timorleste": "tl",
    # "northmacedonia": "nm",
    "france": "bad",
    # territories
    "newcaledonia": "nc",
    "sainthelena": "sh",
    "saintpierreandmiquelon": "spm",
    "britishindianoceanterritory": "biot",
    "cocoskeelingislands": "cki",
    "northernmarianaislands": "nmi",
    "turksandcaicosislands": "tci",
    "britishvirginislands": "bvi",
    "usvirginislands": "uvi",
    "frenchpolynesia": "fp",
    "saintbarthelemy": "sb",
    "americansamoa": "as",
    # capitals
    "washingtondc": "dc",
    # secondary spellings
    "ulaanbaatar": "ulanbator",
    "macao": "macau",
    "kyiv": "kiev",
}


def parse(content: str) -> str:
    return sub("[^a-zA-Z]", "", unidecode(content)).lower().strip()


def starting_embed(answer, question_type, state_type):
    if question_type == FLAGS:
        embed = discord.Embed(
            title=f'Which {"country" if state_type==COUNTRY else "territory"} does this flag belong to?',
            color=QUESTION_HEX,
            timestamp=datetime.now(UTC),
        ).set_image(url=answer["flags"])
    else:
        embed = discord.Embed(
            title=f'What is the capital of `{answer["name"]}`?',
            color=QUESTION_HEX,
            timestamp=datetime.now(UTC),
        ).set_thumbnail(url=answer["flags"])

    return embed


def no_answer_embed(answer, question_type, state_type):
    if question_type == FLAGS:
        embed = discord.Embed(
            title="No one answered correctly!",
            description=f'Which {"country" if state_type==COUNTRY else "territory"} does this flag belong to? \nAnswer: `{answer["name"]}`',
            color=0xFA8E23,
            timestamp=datetime.now(UTC),
        ).set_thumbnail(url=answer["flags"])

    else:
        capital = (
            answer["capital"]
            if isinstance(answer["capital"], str)
            else " | ".join(answer["capital"])
        )

        embed = discord.Embed(
            title="No one answered correctly!",
            description=f'What is the capital of `{answer["name"]}`? \nAnswer: `{capital}`',
            color=WRONG_HEX,
            timestamp=datetime.now(UTC),
        )
    return embed


def update_score(id):
    conn = psycopg2.connect(DB_URL)

    cur = conn.cursor()
    cur.execute(f"SELECT id FROM parrot WHERE id = {id}")
    if cur.fetchall():
        cur.execute(f"UPDATE parrot SET score=score+{POINT_GAIN} WHERE id={id}")
        cur.execute(f"SELECT score FROM parrot WHERE id={id}")
        totals = cur.fetchall()[0][0]

    else:
        cur.execute(f"INSERT INTO parrot (id, score) VALUES ({id}, {POINT_GAIN})")
        totals = {POINT_GAIN}

    cur.close()
    conn.commit()
    conn.close()

    return totals


def win_embed(
    answer, question_type, state_type, player: discord.Member, score, start_time
):
    seconds_taken = datetime.fromtimestamp(
        datetime.now(UTC).timestamp() - start_time
    ).second
    time_elapsed = f"{seconds_taken} second{'s' if seconds_taken else ''}"
    if question_type == FLAGS:
        embed = (
            discord.Embed(
                title=f"{player} answered correctly in {time_elapsed}!",
                description=f'Which {"country" if state_type == COUNTRY else "territory"} does this flag belong to? \nAnswer: `{answer["name"]}`',
                color=0x3CB556,
                timestamp=datetime.now(UTC),
            )
            .set_thumbnail(url=answer["flags"])
            .set_author(name=player, icon_url=player.display_avatar)
            .set_footer(text=f"They have a total of {score} point(s)!")
        )
    else:
        capital = (
            answer["capital"]
            if isinstance(answer["capital"], str)
            else " | ".join(answer["capital"])
        )

        embed = (
            discord.Embed(
                title=f"{player} answered correctly in {time_elapsed}!",
                description=f'What is the capital of `{answer["name"]}`? \nAnswer: `{capital}`',
                color=0x3CB556,
                timestamp=datetime.now(UTC),
            )
            .set_author(name=player, icon_url=player.display_avatar)
            .set_footer(text=f"They have a total of {score} point(s)!")
        )

    return embed
