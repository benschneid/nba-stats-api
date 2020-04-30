from sqlalchemy import MetaData, Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema='stage'))
BaseProd = declarative_base(metadata=MetaData(schema='prod'))


class StatsMixin:
    MIN = Column(Integer)
    FGM = Column(Integer)
    FGA = Column(Integer)
    FG_PCT = Column(Float)
    FG3M = Column(Integer)
    FG3A = Column(Integer)
    FG3_PCT = Column(Float)
    FTM = Column(Integer)
    FTA = Column(Integer)
    FT_PCT = Column(Float)
    OREB = Column(Integer)
    DREB = Column(Integer)
    REB = Column(Integer)
    AST = Column(Integer)
    STL = Column(Integer)
    BLK = Column(Integer)
    TOV = Column(Integer)
    PF = Column(Integer)
    PTS = Column(Integer)
    PLUS_MINUS = Column(Integer)


class OpptStatsMixin:
    OPPT_FGM = Column(Integer)
    OPPT_FGA = Column(Integer)
    OPPT_FG_PCT = Column(Float)
    OPPT_FG3M = Column(Integer)
    OPPT_FG3A = Column(Integer)
    OPPT_FG3_PCT = Column(Float)
    OPPT_FTM = Column(Integer)
    OPPT_FTA = Column(Integer)
    OPPT_FT_PCT = Column(Float)
    OPPT_OREB = Column(Integer)
    OPPT_DREB = Column(Integer)
    OPPT_REB = Column(Integer)
    OPPT_AST = Column(Integer)
    OPPT_STL = Column(Integer)
    OPPT_BLK = Column(Integer)
    OPPT_TOV = Column(Integer)
    OPPT_PF = Column(Integer)
    OPPT_PTS = Column(Integer)


class LeagueGameLog(Base):
    __tablename__ = 'league_game_log'

    SEASON_ID = Column(String)
    TEAM_ID = Column(Integer, primary_key=True)
    TEAM_ABBREVIATION = Column(String)
    TEAM_NAME = Column(String)
    GAME_ID = Column(String, primary_key=True)
    GAME_DATE = Column(String)
    MATCHUP = Column(String)
    WL = Column(String)
    MIN = Column(Integer)
    FGM = Column(Integer)
    FGA = Column(Integer)
    FG_PCT = Column(Float)
    FG3M = Column(Integer)
    FG3A = Column(Integer)
    FG3_PCT = Column(Float)
    FTM = Column(Integer)
    FTA = Column(Integer)
    FT_PCT = Column(Float)
    OREB = Column(Integer)
    DREB = Column(Integer)
    REB = Column(Integer)
    AST = Column(Integer)
    STL = Column(Integer)
    BLK = Column(Integer)
    TOV = Column(Integer)
    PF = Column(Integer)
    PTS = Column(Integer)
    PLUS_MINUS = Column(Integer)
    VIDEO_AVAILABLE = Column(Integer)
    Playoffs = Column(Boolean)


class PlayerBoxStage(StatsMixin, Base):
    __tablename__ = 'player_box'

    GAME_ID = Column(String, primary_key=True)
    TEAM_ID = Column(Integer)
    TEAM_ABBREVIATION = Column(String)
    TEAM_CITY = Column(String)
    PLAYER_ID = Column(Integer, primary_key=True)
    PLAYER_NAME = Column(String)
    START_POSITION = Column(String)
    COMMENT = Column(String)
    MIN = Column(String)
    FGM = Column(Integer)
    FGA = Column(Integer)
    FG_PCT = Column(Float)
    FG3M = Column(Integer)
    FG3A = Column(Integer)
    FG3_PCT = Column(Float)
    FTM = Column(Integer)
    FTA = Column(Integer)
    FT_PCT = Column(Float)
    OREB = Column(Integer)
    DREB = Column(Integer)
    REB = Column(Integer)
    AST = Column(Integer)
    STL = Column(Integer)
    BLK = Column(Integer)
    TOV = Column(Integer)
    PF = Column(Integer)
    PTS = Column(Integer)
    PLUS_MINUS = Column(Integer)


class Teams(BaseProd):
    __tablename__ = 'teams'

    TEAM_ID = Column(Integer, primary_key=True)
    NAME = Column(String)


class Games(BaseProd):
    __tablename__ = 'games'

    GAME_ID = Column(String, primary_key=True)
    SEASON_ID = Column(String)
    GAME_DATE = Column(DateTime)
    PLAYOFFS = Column(Boolean)


class TeamBox(StatsMixin, BaseProd):
    __tablename__ = 'team_box'

    TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID), primary_key=True)
    GAME_ID = Column(String, ForeignKey(Games.GAME_ID), primary_key=True)
    HOME = Column(Boolean)
    WIN = Column(Boolean)
    OPPONENT_TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID))


class TeamSeasonReg(StatsMixin, OpptStatsMixin, BaseProd):
    __tablename__ = 'team_season_reg'

    TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID), primary_key=True)
    SEASON_ID = Column(String, primary_key=True)
    GAMES = Column(Integer)
    WINS = Column(Integer)
    LOSSES = Column(Integer)


class TeamSeasonPost(StatsMixin, OpptStatsMixin, BaseProd):
    __tablename__ = 'team_season_post'

    TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID), primary_key=True)
    SEASON_ID = Column(String, primary_key=True)
    GAMES = Column(Integer)
    WINS = Column(Integer)
    LOSSES = Column(Integer)


class Player(BaseProd):
    __tablename__ = 'players'

    PLAYER_ID = Column(Integer, primary_key=True)
    NAME = Column(String)
    DOB = Column(DateTime)
    COUNTRY = Column(String)
    HEIGHT = Column(Integer)
    WEIGHT = Column(Integer)
    SEASON_EXP = Column(Integer)
    FROM_YEAR = Column(Integer)
    TO_YEAR = Column(Integer)
    DRAFT_YEAR = Column(Integer)
    DRAFT_RD = Column(Integer)
    DRAFT_NUMBER = Column(Integer)
    SCHOOL = Column(String)
    POSITION = Column(String)


class PlayerBoxProd(StatsMixin, BaseProd):
    __tablename__ = 'player_box'

    GAME_ID = Column(String, ForeignKey(Games.GAME_ID), primary_key=True)
    TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID))
    PLAYER_ID = Column(Integer, ForeignKey(Player.PLAYER_ID), primary_key=True)
    STARTED = Column(Boolean)


class PlayerSeasonReg(StatsMixin, BaseProd):
    __tablename__ = 'player_season_reg'

    SEASON_ID = Column(String, primary_key=True)
    TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID), primary_key=True)
    PLAYER_ID = Column(Integer, ForeignKey(Player.PLAYER_ID), primary_key=True)
    GAMES = Column(Integer)
    GAMES_STARTED = Column(Integer)


class PlayerSeasonPost(StatsMixin, BaseProd):
    __tablename__ = 'player_season_post'

    SEASON_ID = Column(String, primary_key=True)
    TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID), primary_key=True)
    PLAYER_ID = Column(Integer, ForeignKey(Player.PLAYER_ID), primary_key=True)
    GAMES = Column(Integer)
    GAMES_STARTED = Column(Integer)


class CleanPlayerBoxStage(StatsMixin, Base):
    __tablename__ = 'player_box_clean'

    GAME_ID = Column(String, ForeignKey(Games.GAME_ID), primary_key=True)
    TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID))
    PLAYER_ID = Column(Integer, ForeignKey(Player.PLAYER_ID), primary_key=True)
    STARTED = Column(Boolean)


class CleanTeamBoxStage(StatsMixin, Base):
    __tablename__ = 'team_box_clean'

    TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID), primary_key=True)
    GAME_ID = Column(String, ForeignKey(Games.GAME_ID), primary_key=True)
    HOME = Column(Boolean)
    WIN = Column(Boolean)
    OPPONENT_TEAM_ID = Column(Integer, ForeignKey(Teams.TEAM_ID))