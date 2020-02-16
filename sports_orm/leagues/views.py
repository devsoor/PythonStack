from django.shortcuts import render, redirect
from django.db.models import Q
from .models import League, Team, Player

from . import team_maker

def index(request):
	all_baseball_leagues = League.objects.filter(sport="Baseball")
	all_womens_leagues = League.objects.filter(name__icontains="women")
	hockey_sport = League.objects.filter(sport__icontains="hockey")
	other_than_football = League.objects.exclude(sport__icontains="football")
	call_conferences = League.objects.filter(name__icontains="conference")
	atlantic_region = League.objects.filter(name__icontains="atlantic")
	teams_dallas = Team.objects.filter(location="Dallas")
	teams_raptors = Team.objects.filter(team_name__icontains="raptor")
	includes_city = Team.objects.filter(location__icontains="city")
	begin_with_t = Team.objects.filter(team_name__startswith="T")
	alpha_location = Team.objects.order_by('location')
	alpha_location_reverse = Team.objects.order_by('-location')
	lastname_cooper = Player.objects.filter(last_name="Cooper")
	firstname_joshua = Player.objects.filter(first_name="Joshua")
	cooper_except_joshua = Player.objects.filter(last_name="Cooper").exclude(first_name="Joshua")
	alexander_or_wyatt = Player.objects.filter(Q(first_name="Alexander") | Q(first_name="Wyatt"))

	# PART 2
	# all teams in the Atlantic Soccer Conference
	leagueASC = League.objects.get(name="Atlantic Soccer Conference")
	teams_in_atlantic_soccer_conference = Team.objects.filter(league=leagueASC)

	# all (current) players on the Boston Penguins
	team = Team.objects.get(Q(location="Boston") & Q(team_name="Penguins"))
	# this is an array of current teams
	# to access player info. eg. current_players_boston_penguins[0].curr_team.location
	current_players_boston_penguins = Player.objects.filter(curr_team=team)

	# all (current) players in the International Collegiate Baseball Conference
	league = League.objects.get(name="International Collegiate Baseball Conference")
	teams = Team.objects.filter(league=league)
	current_players_ICBC = Player.objects.filter(curr_team__in=teams)

	# all (current) players in the American Conference of Amateur Football with last name "Lopez"
	leagueACAF = League.objects.get(name="American Conference of Amateur Football")
	teams = Team.objects.filter(league=leagueACAF)
	current_players_ACAF_lopez = Player.objects.filter(curr_team__in=teams).filter(last_name="Lopez")

	# all football players
	all_football_leagues = League.objects.filter(sport="Football")
	teams = Team.objects.filter(league__in=all_football_leagues)
	all_football_players = Player.objects.filter(all_teams__in=teams)
	# for x in all_football_players:
	# 	print(x.first_name)


	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"all_baseball_leagues": all_baseball_leagues,
		"all_womens_leagues": all_womens_leagues,
		"hockey_sport": hockey_sport,
		"other_than_football": other_than_football,
		"call_conferences": call_conferences,
		"atlantic_region": atlantic_region,
		"teams_dallas": teams_dallas,
		"teams_raptors": teams_raptors,
		"includes_city": includes_city,
		"begin_with_t": begin_with_t,
		"alpha_location": alpha_location,
		"alpha_location_reverse": alpha_location_reverse,
		"lastname_cooper": lastname_cooper,
		"firstname_joshua": firstname_joshua,
		"cooper_except_joshua": cooper_except_joshua,
		"alexander_or_wyatt": alexander_or_wyatt,
		"teams_in_atlantic_soccer_conference": teams_in_atlantic_soccer_conference,
		"current_players_boston_penguins": current_players_boston_penguins,
		"current_players_ICBC": current_players_ICBC,
		"current_players_ACAF_lopez": current_players_ACAF_lopez,
		"all_football_players": all_football_players,
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")