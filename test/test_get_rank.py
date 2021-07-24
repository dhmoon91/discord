import os
import logging
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from riot_api import get_summoner_rank
from db.db import bind_engine

log = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
LOCAL_BOT_PREFIX = os.getenv("LOCAL_BOT_PREFIX")
TEST_DB_URL = os.getenv("TEST_DB_URL")
# Connec to Test DB.
engine = create_engine(TEST_DB_URL)
bind_engine(engine)
conn = engine.connect()

# pylint: disable=E0213,R0201,C0103
class TestGetRank():
    """
    Class to test functionality from get_rank.py file
    """

    @pytest.fixture(scope='session', autouse=True)
    def setup_and_restore_db(root_path):
        """
        Setup and restore DB used for test
        """

        # Yield for test cases to run
        yield

        # After test runs, truncate summoners table
        conn.execute("TRUNCATE TABLE summoners")

    # pylint: disable=C0301
    def test_get_summoner_rank_norank_norecord_in_DB(
        root_path,
        mocker
        ):
        """
        Test Scenario:
        - Summoner does not have solo queue data
        - Summoner does not exist in the DB
        """
        mocker.patch(
            'riotwatcher._apis.league_of_legends.SummonerApiV4.by_name',
            return_value = {
                "id": "ACIuWKdxMpkvr_S5-oTzJB58y_A9hJlAknRKMdo7g_huZEo",
                "accountId": "Ue5LL1z5n63qoOntop6hDx8oD2VWSMlyyWwuqz-zN2Ji7g",
                "puuid": "eDQgZzLbwqqkAg-JkWc_nhfgcnCZwPGTik-nJpTFmaVsiYoH9pFhVfihxifjMwrV18USAPQlUSXXqg",
                "name": "EXAMPLE",
                "profileIconId": "554",
                "revisionDate": "1612617562000",
                "summonerLevel": "47",
                "tier_division": "UNRANKED"
            }
        )
        mocker.patch(
            'riotwatcher._apis.league_of_legends.LeagueApiV4.by_summoner',
            return_value = []
        )
        mocker.patch(
            'riotwatcher._apis.league_of_legends.DataDragonApi.versions_for_region',
            return_value = {
                'n': {
                    'item': '11.15.1',
                    'rune': '7.23.1',
                    'mastery': '7.23.1',
                    'summoner': '11.15.1',
                    'champion': '11.15.1',
                    'profileicon': '11.15.1',
                    'map': '11.15.1',
                    'language': '11.15.1',
                    'sticker': '11.15.1'
                },
                'v': '11.15.1',
                'l': 'en_US',
                'cdn': 'https://ddragon.leagueoflegends.com/cdn',
                'dd': '11.15.1',
                'lg': '11.15.1',
                'css': '11.15.1',
                'profileiconmax': 28,
                'store': None
            }
        )
        expected_summoner_profile = {
            "summoner_name": "EXAMPLE",
            "summoner_icon_image_url": "http://ddragon.leagueoflegends.com/cdn/11.15.1/img/profileicon/554.png",
            "summoner_level": 47,
            "tier_image_path": "/Users/SPARK/GitHub/discord/images/Emblem_Unranked.png",
            "tier_image_name": "Emblem_Unranked.png",
            "tier": "UNRANKED I",
            "puuid": "eDQgZzLbwqqkAg-JkWc_nhfgcnCZwPGTik-nJpTFmaVsiYoH9pFhVfihxifjMwrV18USAPQlUSXXqg",
            "tier_division": "UNRANKED",
            "tier_rank": "I",
            "solo_win": 0,
            "solo_loss": 0,
            "league_points": 0,
        }
        actual_summoner_profile = get_summoner_rank(expected_summoner_profile["summoner_name"])
        assert expected_summoner_profile["summoner_name"] == actual_summoner_profile["summoner_name"]
        assert expected_summoner_profile["puuid"] == actual_summoner_profile["puuid"]
        assert expected_summoner_profile["solo_win"] == actual_summoner_profile["solo_win"]
        assert expected_summoner_profile["solo_loss"] == actual_summoner_profile["solo_loss"]
        assert expected_summoner_profile["league_points"] == actual_summoner_profile["league_points"]

    # pylint: disable=C0301
    def test_get_summoner_rank_norank_yesrecord_in_DB(
        root_path,
        mocker
        ):
        """
        Test Scenario:
        - Summoner does not have solo queue data
        - Summoner does exist in the DB
        """
        # This time, mocked API call for SummonerApiV4.by_name has two different values: revisionDate, summonerLevel
        # No need to mock for other two API calls since code path of get_summoner_rank()  won't require other two
        # API calls(): LeagueApiV4.by_summoner, DataDragonApi.versions_for_region
        mocker.patch(
            'riotwatcher._apis.league_of_legends.SummonerApiV4.by_name',
            return_value = {
                "id": "ACIuWKdxMpkvr_S5-oTzJB58y_A9hJlAknRKMdo7g_huZEo",
                "accountId": "Ue5LL1z5n63qoOntop6hDx8oD2VWSMlyyWwuqz-zN2Ji7g",
                "puuid": "eDQgZzLbwqqkAg-JkWc_nhfgcnCZwPGTik-nJpTFmaVsiYoH9pFhVfihxifjMwrV18USAPQlUSXXqg",
                "name": "EXAMPLE",
                "profileIconId": "554",
                "revisionDate": "1620000000000",
                "summonerLevel": "50",
                "tier_division": "UNRANKED"
            }
        )
        expected_summoner_profile = {
            "summoner_name": "EXAMPLE",
            "summoner_icon_image_url": "http://ddragon.leagueoflegends.com/cdn/11.15.1/img/profileicon/554.png",
            "summoner_level": 47,
            "tier_image_path": "/Users/SPARK/GitHub/discord/images/Emblem_Unranked.png",
            "tier_image_name": "Emblem_Unranked.png",
            "tier": "UNRANKED I",
            "puuid": "eDQgZzLbwqqkAg-JkWc_nhfgcnCZwPGTik-nJpTFmaVsiYoH9pFhVfihxifjMwrV18USAPQlUSXXqg",
            "tier_division": "UNRANKED",
            "tier_rank": "I",
            "solo_win": 0,
            "solo_loss": 0,
            "league_points": 0,
        }
        actual_summoner_profile = get_summoner_rank(expected_summoner_profile["summoner_name"])

        assert expected_summoner_profile["summoner_name"] == actual_summoner_profile["summoner_name"]
        assert expected_summoner_profile["puuid"] == actual_summoner_profile["puuid"]
        assert expected_summoner_profile["solo_win"] == actual_summoner_profile["solo_win"]
        assert expected_summoner_profile["solo_loss"] == actual_summoner_profile["solo_loss"]
        # By checking summonerLevel==47, can verify if this is from DB
        assert actual_summoner_profile["summoner_level"] == 47
        assert expected_summoner_profile["league_points"] == actual_summoner_profile["league_points"]

    # pylint: disable=C0301
    def test_get_summoner_rank_yesrank_norecord_in_DB(
        root_path,
        mocker
        ):
        """
        Test Scenario:
        - Summoner does have solo queue data
        - Summoner does not exist in the DB
        """
        # Using different player who has rank
        mocker.patch(
            'riotwatcher._apis.league_of_legends.SummonerApiV4.by_name',
            return_value = {
                'id': 'VvruhJ0e__QyGDYQC87_N2OdwsNf_HpNB_N3g_DXp1bqrC8',
                'accountId': 'kVZi_7OchZrXSiDHneDy_JCcIr9Y7kuizHfjtmWP2nJ7HA',
                'puuid': 'Gis2tmv3tYX9XVb9tihXylX7pO-75aYIBUg96xi6ZDLI769mzPD0ERTDZcq7X00Fr5KtcIu1lvkiZQ',
                'name': 'd4022',
                'profileIconId': 4572,
                'revisionDate': 1627430846000,
                'summonerLevel': 103
            }
        )
        mocker.patch(
            'riotwatcher._apis.league_of_legends.LeagueApiV4.by_summoner',
            return_value = [
                {'leagueId': 'a2a37ac1-e00f-40d8-8008-894d5eb121a6',
                'queueType': 'RANKED_FLEX_SR',
                'tier': 'BRONZE',
                'rank': 'IV',
                'summonerId': 'VvruhJ0e__QyGDYQC87_N2OdwsNf_HpNB_N3g_DXp1bqrC8',
                'summonerName': 'd4022',
                'leaguePoints': 64, 'wins': 14,
                'losses': 19,
                'veteran': False,
                'inactive': False,
                'freshBlood': False,
                'hotStreak': False
                },
                {'leagueId': 'd6dea52e-6269-4d4e-b378-4385aa602f0f',
                'queueType': 'RANKED_SOLO_5x5',
                'tier': 'SILVER',
                'rank': 'IV',
                'summonerId': 'VvruhJ0e__QyGDYQC87_N2OdwsNf_HpNB_N3g_DXp1bqrC8',
                'summonerName': 'd4022',
                'leaguePoints': 46,
                'wins': 21,
                'losses': 24,
                'veteran': False,
                'inactive': False,
                'freshBlood': False,
                'hotStreak': False
                }
            ]
        )
        mocker.patch(
            'riotwatcher._apis.league_of_legends.DataDragonApi.versions_for_region',
            return_value = {
                'n': {
                    'item': '11.15.1',
                    'rune': '7.23.1',
                    'mastery': '7.23.1',
                    'summoner': '11.15.1',
                    'champion': '11.15.1',
                    'profileicon': '11.15.1',
                    'map': '11.15.1',
                    'language': '11.15.1',
                    'sticker': '11.15.1'
                },
                'v': '11.15.1',
                'l': 'en_US',
                'cdn': 'https://ddragon.leagueoflegends.com/cdn',
                'dd': '11.15.1',
                'lg': '11.15.1',
                'css': '11.15.1',
                'profileiconmax': 28,
                'store': None
            }
        )
        expected_summoner_profile = {
            'summoner_name': 'd4022',
            'summoner_icon_image_url': 'http://ddragon.leagueoflegends.com/cdn/11.15.1/img/profileicon/4572.png',
            'summoner_level': 103,
            'tier_image_path': '/Users/SPARK/GitHub/discord/images/Emblem_Silver.png',
            'tier_image_name': 'Emblem_Silver.png',
            'tier': 'SILVER IV',
            'puuid': 'Gis2tmv3tYX9XVb9tihXylX7pO-75aYIBUg96xi6ZDLI769mzPD0ERTDZcq7X00Fr5KtcIu1lvkiZQ',
            'tier_division': 'SILVER',
            'tier_rank': 'IV',
            'solo_win': 21,
            'solo_loss': 24,
            'league_points': 46
        }
        actual_summoner_profile = get_summoner_rank(expected_summoner_profile["summoner_name"])

        assert expected_summoner_profile["summoner_name"] == actual_summoner_profile["summoner_name"]
        assert expected_summoner_profile["summoner_icon_image_url"] == actual_summoner_profile["summoner_icon_image_url"]
        assert expected_summoner_profile["summoner_level"] == actual_summoner_profile["summoner_level"]
        assert expected_summoner_profile["tier_image_path"] == actual_summoner_profile["tier_image_path"]
        assert expected_summoner_profile["tier_image_name"] == actual_summoner_profile["tier_image_name"]
        assert expected_summoner_profile["tier"] == actual_summoner_profile["tier"]
        assert expected_summoner_profile["puuid"] == actual_summoner_profile["puuid"]
        assert expected_summoner_profile["tier_division"] == actual_summoner_profile["tier_division"]
        assert expected_summoner_profile["tier_rank"] == actual_summoner_profile["tier_rank"]
        assert expected_summoner_profile["solo_win"] == actual_summoner_profile["solo_win"]
        assert expected_summoner_profile["solo_loss"] == actual_summoner_profile["solo_loss"]
        assert expected_summoner_profile["league_points"] == actual_summoner_profile["league_points"]

    # pylint: disable=C0301
    def test_get_rank_summoner_not_found(
        root_path,
        mocker
        ):
        """
        Test Scenario: no such user exist
        Expepcted Result: exception is raised for invalid username
        """
        mocker.patch(
            'riotwatcher._apis.league_of_legends.SummonerApiV4.by_name',
            side_effect=Exception('not found'),
            status_codes=404
        )
        with pytest.raises(Exception):
            assert get_summoner_rank("wefnasdfjpqowiejfsdafnlknfqpoweijfasdfngiopqjwepoijfdslkaklnqpoijafsdafp")
            assert Exception == 404
