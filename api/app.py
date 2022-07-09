import json
import logging

from enum import Enum
from random import shuffle
from dataclasses import dataclass, field

from pandas import DataFrame, Series
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.applications import Starlette

logger = logging.getLogger("uvicorn")

TEAM = None 
DF = None 

class Restaurant(Enum):
    CH = 'Panda Express'
    IT = 'Olive Garden'
    JP = 'Tabata Ramen & Sushi'
    MX = 'Chipotle Mexican Grill'
    TH = 'Zoob Zib Noodle'
    US = 'Five Guys'

@dataclass
class Worker:
    name: str
    RL: list = field(default_factory=list)
    L: list = field(default_factory=list)
    DL: list = field(default_factory=list)

    def add_pref(self, o, c):
        self.__dict__[o].append(c)

    def __str__(self):
        return self.name 

def choose(options):
    ''' Choose preferences from the optiosn '''
    pref = ['RL', 'L', 'DL']
    shuffle(options)
    while options:
        shuffle(pref) 
        c = options.pop() 
        yield pref[0], c

def init_team():
    members = 'Adolfo—Eric—Evan—Jean-Marc—Jef—Ricardo—Simoni'.split('—')
    
    team = []
    for member in members:
        w = Worker(name=member)
        for (o, c) in choose([*Restaurant]):
            w.add_pref(o, c)
        team.append(w)
    
    global TEAM
    TEAM = team

    preferences = {'RL':[], 'L':[], 'DL':[]}
    for w in TEAM:
        for p in preferences.keys():
            preferences[p].extend([(w.name, r.name) for r in getattr(w, p)])

    df = (
        DataFrame({
            k: Series(data=True, index=preferences[k])
            for k in preferences
        }).fillna(False).sort_index()
    ).pipe(lambda df: df @ Series({'RL': 1, 'L': 0, 'DL': -1}))

    global DF 
    DF = df


def restaurants(request):
    ''' return Restaurants '''

    restaurants = [r.value for r in Restaurant]
    return JSONResponse(
        {
            'restaurants': restaurants
        },
        headers = {"Access-Control-Allow-Origin": '*'}
    )

def team(request):
    ''' return team members and their preferences '''

    restaurants = [r.value for r in Restaurant]
    return JSONResponse(
        {
            'team': [ 
                {
                    'name': w.name, 
                    'RL': [rl.value for rl in w.RL],
                    'L': [l.value for l in w.L],
                    'DL': [dl.value for dl in w.DL],
                }
                for w in TEAM 
            ],
            'winner': DF.groupby(level=1).sum().sort_values().idxmax()
        },
        headers = {"Access-Control-Allow-Origin": '*'}
    )

def winner(request):
    ''' return where we should eat '''
    
    logger.info(f'\nScores:\n{DF.groupby(level=1).sum().sort_values()}')
    return JSONResponse(
        {
            'winner': Restaurant[DF.groupby(level=1).sum().sort_values().idxmax()].value
        },
        headers = {"Access-Control-Allow-Origin": '*'}
    )

def ping(request):
    ''' pong '''
    
    return JSONResponse(
        {'ping': 'pong'}, 
        headers = {"Access-Control-Allow-Origin": 'http://127.0.0.1:8080'}
    )

routes = [
    Route("/", endpoint=ping, methods=["GET"]),
    Route("/v1/team", endpoint=team, methods=["GET"]),
    Route("/v1/winner", endpoint=winner, methods=["GET"]),
    Route("/v1/restaurants", endpoint=restaurants, methods=["GET"]),
]

app = Starlette(on_startup=[init_team], routes=routes,)
