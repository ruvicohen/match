from operator import itemgetter

from toolz import first, curry, compose, groupby, nth, second
from toolz.curried import partial, pipe, reduce

from api.dbz_api import get_dbz
from repository.json_repository import read_json, convert_to_warrior

if __name__ == "__main__":
    url_dbz = "https://dragonball-api.com/api/characters/"
    home_team = read_json("repository/home_team.json")
    dbz_team = get_dbz(url_dbz)["items"]
    print(home_team)
    print(dbz_team)
    list1 = list(map(lambda x: convert_to_warrior(x), home_team))
    print(
        pipe(
            home_team,
            partial(map, convert_to_warrior),
            partial(map, lambda x: x.name),
            " ".join
        )
    )
    # first from home-team first from dbz-team
    # check win according to ki
    first_dbz = compose(
        first,
        partial(map, convert_to_warrior)
    )
    get_by_index = lambda i: compose(
        partial(nth, i),
        partial(map, convert_to_warrior)
    )

    win_dbz = lambda x, y: x.name if x.ki > y.ki else y.name
    print(win_dbz(first_dbz(dbz_team), first_dbz(home_team)))

    # first five against first five

    get_ki = compose(
        sum,
        partial(map, lambda x: int(x.ki.replace(".",""))),
        partial(map, convert_to_warrior)
    )

    def winners_by_five(home, dbz):
        first_five_ki_home = get_ki(home[:5])
        first_five_ki_dbz = get_ki(dbz[:5])
        if first_five_ki_home > first_five_ki_dbz:
            print("home win")
        elif first_five_ki_dbz > first_five_ki_home:
            print("dbz win")
        else:
            print("draw")

    print(winners_by_five(home_team, dbz_team))
    # first ten against first ten (only uniq by affiliation )
    get_unique_by_affiliation = compose(
        lambda x: [group[0] for group in x.values()],
        partial(groupby,lambda u: u["affiliation"])
    )

    get_unique_by_affiliation2 = compose(
        dict.values,
        dict,
        partial(map, lambda u: (u["affiliation"], u))
    )

    def winners_by_ten_and_unique(home, dbz):
        first_five_ki_home = pipe(home, get_unique_by_affiliation2, get_ki)
        first_five_ki_dbz = pipe(dbz, get_unique_by_affiliation2, get_ki)
        if first_five_ki_home > first_five_ki_dbz:
            print("home win")
        elif first_five_ki_dbz > first_five_ki_home:
            print("dbz win")
        else:
            print("draw")

    print(winners_by_ten_and_unique(home_team, dbz_team))
    # first against second only if they are not with the same affiliation

    # write the description and the name upper case of the average warrior of each teams

    upper_average_warrior = compose(
        ",".join,
        partial(map, str.upper),
        partial(map, lambda x: f'{x["name"]}: {x["description"]}'),
        lambda warriors: [warrior for idx, warrior in enumerate(warriors) if idx == len(warriors) // 2]
    )

    print(upper_average_warrior(home_team))