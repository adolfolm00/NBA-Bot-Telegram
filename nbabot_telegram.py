from telegram.ext import Updater, CommandHandler
import telegram
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tabulate import tabulate
import numpy as np

def help(update, context):
        comandos = "/help: lista de comandos\n/este: Ranking conferencia este\n"+\
        "/oeste: Ranking conferencia oeste\n/stats: Ranking de estadísticas"+\
        "/partidos: Ver los siguientes partidos"

        update.message.reply_text(comandos)

def get_games():
        url = 'https://www.movistarplus.es/nba/horarios'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        all_games_soup = soup.find_all('div',class_='title-team')

        all_games_list = list()

        for i in all_games_soup:
                all_games_list.append(i.text)

        
        return all_games_list

def get_games_dates():
        url = 'https://www.movistarplus.es/nba/horarios'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        all_games_dates_soup = soup.find_all('div',class_='fecha-calendar')

        all_games_dates_list = list()

        for i in all_games_dates_soup:
                all_games_dates_list.append(i.text)

        return all_games_dates_list

def games(update,context):
        games = get_games()
        date = get_games_dates()

        super_string = ""

        for i in range (len(games)):
                super_string += "⏰Horario: "+str(date[i])+"\n🏀Partido:"+str(games[i])+"\n"

        update.message.reply_text(super_string)


def get_ranking_teams():
        url = 'https://www.mundodeportivo.com/resultados/baloncesto/nba/clasificacion'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        all_teams_soup = soup.find_all('a',href='#')
        all_teams_list = list()


        #Añadir los equipos al array
        for i in all_teams_soup:
                all_teams_list.append(i.text)

      
        

        return all_teams_list

def get_ranking_stats():
        url = 'https://www.mundodeportivo.com/resultados/baloncesto/nba/clasificacion'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        

        all_stats_soup = soup.find_all('td',class_='tval text-center')
        all_stats_list = list()

        #Añadir los equipos al array
        for i in all_stats_soup:
                all_stats_list.append(i.text)

        for i in range(8):
                all_stats_list.remove("PJ")
                all_stats_list.remove("PG")
                all_stats_list.remove("PP")
                all_stats_list.remove("%PG")

       
       

        return all_stats_list


def east(update, context):
       
        # Equipos este, pasamos los 15 primeros equipos
        east_teams_list = get_ranking_teams()[:15]

        # A los 8 primeros le asignamos una medalla, que significa que avanzarán a los playoffs
                



        # Puntos este, pasamos las 60 primeras estadísticas
        east_stats_list = get_ranking_stats()[:60]
        

        #Listas estadísticas
        games_played = list()
        games_won = list()
        games_lost = list()

        

       

        #Añadimos los partidos jugados a la lista, siguen una orden de 4 en 4 cada estadística, al estar todas apelotonadas
        cont = 0
        ind = 0
        while cont < len(east_teams_list):
                games_played.append(east_stats_list[ind])
                
                ind += 4
                cont += 1
        

        #Añadimos los partidos ganados
        cont = 0
        ind = 1
        while cont < 15:
                games_won.append(east_stats_list[ind])
                ind += 4
                cont += 1 

        #Añadimos los partidos perdidos
        cont = 0
        ind = 2
        while cont < 15:
                games_lost.append(east_stats_list[ind])
                ind += 4
                cont += 1 

        result = []

        for i in range(len(east_teams_list)):
                result.append([east_teams_list[i],games_played[i],games_won[i],games_lost[i]])

        

        super_string = ""   
        super_string += "CONFERENCIA ESTE🏀 \n"
        super_string += "PJ:PARTIDOS JUGADOS\n"+"PG:PARTIDOS GANADOS\n"+"PP:PARTIDOS PERDIDOS\n"+"🏅: Clasificado a Playoffs\n"
        super_string += "------------------PJ"+"--PG"+"--PP\n"
       
        for i in range(len(east_teams_list)):
                if i <= 7:
                        if len(east_teams_list[i]) >= 17:   
                                super_string += str(i+1)+"."+str((east_teams_list[i]))+"🏅->\t\t|"+str((games_played[i]))+"\t|"+str((games_won[i]))+"|\t"+str((games_lost[i]))+"|\n"
                        
                        elif len(east_teams_list) <17: 
                                super_string += str(i+1)+"."+str((east_teams_list[i]))+"🏅->\t\t\t|"+str((games_played[i]))+"\t|"+str((games_won[i]))+"|\t"+str((games_lost[i]))+"|\n"
                else:
                         if len(east_teams_list[i]) >= 17:   
                                super_string += str(i+1)+"."+str((east_teams_list[i]))+"->\t\t|"+str((games_played[i]))+"\t|"+str((games_won[i]))+"|\t"+str((games_lost[i]))+"|\n"
                        
                         elif len(east_teams_list) <17: 
                                super_string += str(i+1)+"."+str((east_teams_list[i]))+"->\t\t\t|"+str((games_played[i]))+"\t|"+str((games_won[i]))+"|\t"+str((games_lost[i]))+"|\n"


        
         # df = pd.DataFrame({'EQUIPO':east_teams_list,' PARTIDOS JUGADOS':games_played, ' PARTIDOS GANADOS':games_won, ' PARTIDOS PERDIDOS':games_lost}, index=list(range(1,16)))
        # table = tabulate(result, headers=["EQUIPO", "PARTIDOS JUGADOS", "PARTIDOS GANADOS", "PARTIDOS PERDIDOS"],tablefmt = "github")
        #update.message.reply_text(f'<pre>{table}</pre>', parse_mode=telegram.ParseMode.HTML)
        update.message.reply_text(super_string)
        

def west(update, context):
       
        
        # Equipos este, pasamos los 15 primeros equipos
        west_teams_list = get_ranking_teams()[15:30]



        # Puntos este, pasamos las 60 primeras estadísticas
        west_stats_list = get_ranking_stats()[60:120]
        

        #Listas estadísticas
        games_played = list()
        games_won = list()
        games_lost = list()

        

       

        #Añadimos los partidos jugados a la lista, siguen una orden de 4 en 4 cada estadística, al estar todas apelotonadas
        cont = 0
        ind = 0
        while cont < len(west_teams_list):
                games_played.append(west_stats_list[ind])
                
                ind += 4
                cont += 1
        

        #Añadimos los partidos ganados
        cont = 0
        ind = 1
        while cont < len(west_teams_list):
                games_won.append(west_stats_list[ind])
                ind += 4
                cont += 1 

        #Añadimos los partidos perdidos
        cont = 0
        ind = 2
        while cont < len(west_teams_list):
                games_lost.append(west_stats_list[ind])
                ind += 4
                cont += 1 


        
        super_string = ""   
        super_string += "CONFERENCIA OESTE🏀 \n"
        super_string += "PJ:PARTIDOS JUGADOS\n"+"PG:PARTIDOS GANADOS\n"+"PP:PARTIDOS PERDIDOS\n"+"🏅: Clasificado a Playoffs\n"
        super_string += "------------------PJ"+"--PG"+"--PP\n"
       
        for i in range(len(west_teams_list)):
                if i <= 7:
                        if len(west_teams_list[i]) >= 17:   
                                super_string += str(i+1)+"."+str((west_teams_list[i]))+"🏅->\t\t|"+str((games_played[i]))+"\t|"+str((games_won[i]))+"|\t"+str((games_lost[i]))+"|\n"
                        
                        elif len(west_teams_list) <17: 
                                super_string += str(i+1)+"."+str((west_teams_list[i]))+"🏅->\t\t\t|"+str((games_played[i]))+"\t|"+str((games_won[i]))+"|\t"+str((games_lost[i]))+"|\n"
                else:
                         if len(west_teams_list[i]) >= 17:   
                                super_string += str(i+1)+"."+str((west_teams_list[i]))+"->\t\t|"+str((games_played[i]))+"\t|"+str((games_won[i]))+"|\t"+str((games_lost[i]))+"|\n"
                        
                         elif len(west_teams_list) <17: 
                                super_string += str(i+1)+"."+str((west_teams_list[i]))+"->\t\t\t|"+str((games_played[i]))+"\t|"+str((games_won[i]))+"|\t"+str((games_lost[i]))+"|\n"
       
        
        df = pd.DataFrame({'EQUIPO':west_teams_list, ' PARTIDOS JUGADOS':games_played, ' PARTIDOS GANADOS':games_won, ' PARTIDOS PERDIDOS':games_lost}, index=list(range(1,16)))
        update.message.reply_text(super_string)

def get_players_list():
        #Función que devolverá una lista con todos los jugadores
        url = 'https://www.mundodeportivo.com/resultados/baloncesto/nba/estadisticas'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        all_players_soup = soup.find_all('td',class_='tname')
        all_players = list()

         #Guardar los nombres en la lista de todos los jugadores
        cont = 0
        for i in all_players_soup:
                if cont < len(all_players_soup):
                        all_players.append(i.text)
                else:
                        break
                cont +=1

        return all_players

def get_players_stats():
        #Función que devolverá una lista con las asistencias de los jugadores
        url = 'https://www.mundodeportivo.com/resultados/baloncesto/nba/estadisticas'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        all_stats_soup = soup.find_all('td',class_='tval text-center')
        all_stats = list()

         #Guardar los nombres en la lista de todos los jugadores
        cont = 0
        for i in all_stats_soup:
                if cont < len(all_stats_soup):
                        all_stats.append(i.text)
                else:
                        break
                cont +=1


        for i in all_stats:
                if i == "TOTAL":
                        all_stats.remove(i)

        return all_stats


def assists():
        
        #Solo guardaremos los 10 primeros, ya que son los pertenecientes a asistencias
        players_list = get_players_list()[:10]
       

        #Guardamos las 10 primeras asistencias
        assists_list = get_players_stats()[:10]
        
        super_string = "RANKING ASISTENCIAS 👋🏀\n"
        medal = ""
        
        for i in range(len(assists_list)):
                if i == 0:
                        medal = "🥇"
                elif i == 1:
                        medal = "🥈"
                elif i == 2:
                         medal = "🥉"
                else: 
                        medal = ""
                         

                super_string += str(i+1)+"."+players_list[i]+medal+"->"+assists_list[i]+"\n"
        
        return super_string

        



def blocks():
        
        #Solo guardaremos del 10 al 20 ya que son los pertenecientes a tapones
        players_list = get_players_list()[10:20]
       

        #Guardamos los 10  tapones
        blocks_list = get_players_stats()[10:20]
        

        super_string = "RANKING TAPONES ✋⛔\n"
        
        for i in range(len(blocks_list)):
                if i == 0:
                        medal = "🥇"
                elif i == 1:
                        medal = "🥈"
                elif i == 2:
                         medal = "🥉"
                else: 
                        medal = ""
                         

                super_string += str(i+1)+"."+players_list[i]+medal+"->"+blocks_list[i]+"\n"
        
        return super_string



def points():
        
        #Solo guardaremos del 20 al 30 ya que son los pertenecientes a puntos
        players_list = get_players_list()[20:30]
       

        #Guardamos los 10  puntos
        points_list = get_players_stats()[20:30]
        

        super_string = "RANKING PUNTOS 🏀🔥\n"
        
        for i in range(len(points_list)):
                if i == 0:
                        medal = "🥇"
                elif i == 1:
                        medal = "🥈"
                elif i == 2:
                         medal = "🥉"
                else: 
                        medal = ""
                         

                super_string += str(i+1)+"."+players_list[i]+medal+"->"+points_list[i]+"\n"
        
        return super_string

def triples():
        
        #Solo guardaremos del 30 al 40 ya que son los pertenecientes a triples
        players_list = get_players_list()[30:40]
       

        #Guardamos los 10  Triples
        triples_list = get_players_stats()[30:40]
        
      
        super_string = "RANKING TRIPLES ➕3️⃣\n"
        
        for i in range(len(triples_list)):
                if i == 0:
                        medal = "🥇"
                elif i == 1:
                        medal = "🥈"
                elif i == 2:
                         medal = "🥉"
                else: 
                        medal = ""
                         

                super_string += str(i+1)+"."+players_list[i]+medal+"->"+triples_list[i]+"\n"
        
        return super_string

def rebounds():
        
        #Solo guardaremos del 40 al 50 ya que son los pertenecientes a rebotes
        players_list = get_players_list()[40:50]
       

        #Guardamos los 10  rebotes
        rebounds_list = get_players_stats()[40:50]
        
      
        super_string = "RANKING REBOTES 〰️🏀\n"
        
        for i in range(len(rebounds_list)):
                if i == 0:
                        medal = "🥇"
                elif i == 1:
                        medal = "🥈"
                elif i == 2:
                         medal = "🥉"
                else: 
                        medal = ""
                         

                super_string += str(i+1)+"."+players_list[i]+medal+"->"+rebounds_list[i]+"\n"
        
        return super_string


def steals():
        
        #Solo guardaremos del 40 al 50 ya que son los pertenecientes a robos
        players_list = get_players_list()[50:60]
       

        #Guardamos los 10  rebotes
        steals_list = get_players_stats()[50:60]
        
      
        super_string = "RANKING ROBOS 🥷📛\n"
        
        for i in range(len(steals_list)):
                if i == 0:
                        medal = "🥇"
                elif i == 1:
                        medal = "🥈"
                elif i == 2:
                         medal = "🥉"
                else: 
                        medal = ""
                         

                super_string += str(i+1)+"."+players_list[i]+medal+"->"+steals_list[i]+"\n"
        
        return super_string


def stats(update,context):
        super_string = ""
        super_string += assists() + "\n"
        super_string += blocks() + "\n"
        super_string += points() + "\n"
        super_string += triples() + "\n"
        super_string += rebounds() + "\n"
        super_string += steals()

        update.message.reply_text(super_string)


if __name__ == '__main__':
   
   updater = Updater(token='TOKEN', use_context=True)

   dp = updater.dispatcher

   dp.add_handler(CommandHandler('help',help))
   dp.add_handler(CommandHandler('este',east))
   dp.add_handler(CommandHandler('oeste',west))
   dp.add_handler(CommandHandler('stats',stats))
   dp.add_handler(CommandHandler('partidos',games))
   

   #add handler

   updater.start_polling()
   updater.idle()
