# Python 3.6
import hlt  
from hlt import entity
from hlt import constants  
from hlt.positionals import Direction, Position, go_nine_d, get_direction

import logging 
import math
import random
import time


'''
    score = (haliteMined - haliteBurned) / (turnsToMoveToTile + turnsToMoveHome + turnsStayedOnTile).
'''


game = hlt.Game()  
game.ready("Williambot")
ship_states = {}
me = game.me
game_map = game.game_map 
deposit_locations = [me.shipyard.position]
dibs_pos = []
picked_location = {}
req_dis = int(game_map.height/4)
counter = 0
wait = False
grand_total_start = [[c.halite_amount for c in row] for row in game.game_map._cells]
n = [sum(i) for i in zip(*grand_total_start)]
grand_total_start = sum(n)
drop_ships = []
enemy_dropoffs = []
no_more = []
dont_go_below = []
X_vals = list(x for x in range(0,45))
depletion_per_round = []
drop_ship_id = []

def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) 

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    return(round(b,2))


def penis():
    t1 = time.time()
    des = []
    for positions in deposit_locations:
        distance = game_map.calculate_distance(ship.position, positions)
        des.append(distance)
    get_i = min(des)
    index = des.index(get_i)
    
    location = deposit_locations[index]

    h_am = {}
    for position, value in halite_amount.items():
        if position == ship.position:
            if game_map.calculate_distance(ship.position, me.shipyard.position) <=4:
                value = value*4
            else:
                value = value*9

        turns_to_tile = game_map.calculate_distance(ship.position, position)
        turns_to_move_home = game_map.calculate_distance(position,location)
        
        halite_gained_by_moves = (turns_to_move_home+turns_to_tile)*(game_map[ship.position].halite_amount*0.20)
        
        score = (value+halite_gained_by_moves) / (turns_to_tile+turns_to_move_home+1)
        h_am[position] = score
        
    t2 = time.time()
    logging.info(f"time to run fuction penis: {round(t2-t1,5)}")
    return h_am


def to_move_or_not_to_move(ship, move):
    if game_map.calculate_distance(ship.position, me.shipyard.position) >=3:
        if game_map[ship.position].halite_amount != 0:
            if game_map[ship.position+Position(*move)].halite_amount != 0:
                move_cost = (game_map[ship.position].halite_amount/constants.MOVE_COST_RATIO)
                collect = (game_map[ship.position+Position(*move)].halite_amount)*0.25
                if not game_map[ship.position+Position(*move)].has_structure:
                    if move_cost >= collect:
                        future_pos[ship] = ship.position


def suicide_cals(ship,location):
    not_zone = False

    if ship.position == location:
        ship_states[ship.id] = "stay" 
        return

    for direction in dir_list:
        if ship.position ==location+Position(*direction):
            not_zone = True
    
    if not not_zone:
        future_pos[ship] = ship.position+Position(*game_map.get_direction(ship,location))
    else:
        suicide_pos[ship] = ship.position+Position(*game_map.get_direction(ship,location))


def map_s(size):
    surroundings = []
    for x in range(-1*size,size+1):
        for y in range(-1*size,size+1): 
                surroundings.append([x,y])   

    halite_amount = {}
    for row,column in surroundings:
        halite_amount[Position(row,column)] = game_map[Position(row,column)].halite_amount      
        if len(me.get_ships()) >= 16:
            if game_map[Position(row,column)].insper_cell:
                halite_amount[Position(row,column)] = 1.69*(game_map[Position(row,column)].halite_amount)
        
    return halite_amount


def nav_dropoff(ship, location):
    if ship.position != location:
        move = game_map.get_direction(ship, location)
        move = ship.position+Position(*move)
        future_pos[ship] = move  
        if game_map[move].enemy_ship:
            move = game_map.get_direction(ship, location)
            move = ship.position+Position(*go_nine_d(move))
            future_pos[ship] = move
    

    if ship.position == location:
        ship.take_first
        clear()
          

def dropoff_req():
    global wait, counter
    
    if not len(no_more) >=1:
        if (grand_total_current/grand_total_start)*100 >= 52:
            make_better_drop()
            if len(drop_ships) >= 1:
                    wait = True
                    if me.halite_amount >= 5000:
                        wait = False
                        drop_ships.clear()
                        counter = 0


def evasive_maneuvers():
    h_am = penis()
    direct = max(h_am, key= h_am.get)
    if direct != ship.position:
        move = game_map.get_direction(ship, (direct)) 
    else:
        h_am.pop(direct)
        direct = max(h_am, key= h_am.get)
        move = game_map.get_direction(ship,(direct)) 

    future_pos[ship] = ship.position+Position(*move)

    if game_map[ship.position].enemy_ship:
        for direction in [Direction.North,Direction.South,Direction.West,Direction.East]:
            if not game_map[ship.position+Position(*direction)].enemy_ship:
                future_pos[ship] = ship.position+Position(*direction)
                return
    
    if game_map[ship.position+Position(*move)].enemy_ship:
        if not game_map[ship.position+Position(*go_nine_d(move))].enemy_ship:
            future_pos[ship] = ship.position+Position(*go_nine_d(move))
            return
        
        future_pos[ship] = ship.position+Position(*Direction.invert(move))
        return


def regular():
    
    moves = {}
    for direction in dir_list:
        moves[(direction)] = game_map[ship.position+Position(*direction)].halite_amount
        if direction == Direction.Still:
        
            moves[(direction)] = 2.5*game_map[ship.position+Position(*direction)].halite_amount
        
        if game_map[ship.position+Position(*direction)].insper_cell:
            moves[(direction)] = 1.6*game_map[ship.position+Position(*direction)].halite_amount

    directional_choice = max(moves, key=moves.get)
    return directional_choice
    

def basic_nav():
    if ship not in picked_location:
        ship.take_first            
        h_am = penis()
        while True:
            max_pos = max(h_am, key= h_am.get)
            if not game_map[max_pos].enemy_ship: 
                if ship.position in dibs_pos:
                    if max_pos != ship.position:
                        dibs_pos.remove(ship.position)
                    else:
                        future_pos[ship] = ship.position
                        return
                if max_pos not in dibs_pos:
                    dibs_pos.append(max_pos)
                    picked_location[ship] = max_pos

                    k = True
                    for direction in dir_list:
                        if not game_map[ship.position+Position(*direction)].enemy_ship:
                            k = False
                    if k:   
                        direct = max(h_am, key= h_am.get)
                        move = game_map.get_direction(ship,(direct)) 
                        if not game_map[ship.position+Position(*move)].is_occupied:
                            future_pos[ship] = ship.position+Position(*move)
                            to_move_or_not_to_move(ship, move)
                            break
                        
                        else:
                            ship.take_second
                            move = go_nine_d(move)
                            future_pos[ship] = ship.position+Position(*move)
                            to_move_or_not_to_move(ship, move)
                            break
                        
                    else:
                        evasive_maneuvers()
                        break
                else:
                    h_am.pop(max_pos)
            else:
                h_am.pop(max_pos)

    else:
        for ships, move in picked_location.items():
            if ship.id == ships.id:    
                if not game_map[move].is_occupied:
                    move = game_map.get_direction(ship,move)
                    future_pos[ship] = ship.position+Position(*move)
                    to_move_or_not_to_move(ship, move)
                else:
                    ship.take_second   
                    move = game_map.get_direction(ship,move)
                    future_pos[ship] = ship.position+Position(*move)
                    to_move_or_not_to_move(ship, move)
                    
    
    if ship.position in picked_location.values():
        if ship in picked_location.keys():  
            if regular() == Direction.Still:
                future_pos[ship] = ship.position
            else:
                future_pos[ship] = ship.position+Position(*regular())
                del picked_location[ship]


def collecting():   
    if (game.turn_number + 0.5*constants.MAX_TURNS) <= constants.MAX_TURNS:
        amount_u = (game_map[ship.position].halite_amount)*0.25
        if ship.halite_amount+amount_u >= constants.MAX_HALITE:
            ship_states[ship.id] = "deposit"
            return
    else:
        if game.turn_number >=200:
            amount_u = (game_map[ship.position].halite_amount)*0.25
            if ship.halite_amount+amount_u >= constants.MAX_HALITE*0.83:
                ship_states[ship.id] = "deposit"
                return

    if game.turn_number <=5:
        move = ship.position+Position(*random.choice(dir_list))
        if move != me.shipyard.position:
            future_pos[ship] = move
        else:
            future_pos[ship] = ship.position
    
    else:
        basic_nav()
  

def deposit():
    des = []
    for positions in deposit_locations:
        distance = game_map.calculate_distance(ship.position, positions)
        des.append(distance)
    get_i = min(des)
    index = des.index(get_i)
    nav_dropoff(ship,deposit_locations[index])      


def make_better_drop():
    global drop_ships
    if len(drop_ships) == 0:
        loop = True
    else:
        loop = False
   
    while loop:
        for ship in me.get_ships():
            size = 2
            surroundings = []
            for x in range(-1*size,size+1):
                for y in range(-1*size,size+1): 
                        surroundings.append([x,y])   
            amount = []
            for row,column in surroundings:
                val = game_map[ship.position+Position(row,column)].halite_amount
                amount.append(val)
            sm = sum(amount[0:len(amount)])
            des = []
            for positions in deposit_locations:
                distance = game_map.calculate_distance(ship.position, positions)
                des.append(distance)
            get_i = min(des)
            if get_i >= req_dis:
                if sm >= 5100:
                    distance = []
                    for ships in me.get_ships():
                        dis = game_map.calculate_distance(ships.position, ship.position)
                        if dis <= int(req_dis/1.3):
                            distance.append(dis)
                    if len(distance) >=4:
                        drop_ships.append(ship)
                        future_pos[ship] = ship.position
                        loop = False
                        break
        loop = False

    try:
        ship = drop_ships[0]  
        future_pos[ship] = ship.position
        if me.halite_amount >= constants.DROPOFF_COST+1000:
            command_queue.append(ship.make_dropoff())
            deposit_locations.append(ship.position)
            del future_pos[ship]  
            drop_ships.clear()    
        
        deposit_locations.append(ship.position)          
    except:
        pass
       

def suicide():
    des = []
    for positions in deposit_locations:
        distance = game_map.calculate_distance(ship.position, positions)
        des.append(distance)
    get_i = min(des)
    index = des.index(get_i)
    suicide_cals(ship,deposit_locations[index])


def time_to_suicide():
    global kill
    kill = False
    k = []
    for ship in me.get_ships():
        des = []
        for positions in deposit_locations:
            distance = game_map.calculate_distance(ship.position, positions)
            des.append(distance)
        get_i = min(des)
        index = des.index(get_i)
        k.append((game_map.calculate_distance(ship.position, deposit_locations[index]))+int(len(me.get_ships())/6))
    

    try:
        if max(k)+game.turn_number >= constants.MAX_TURNS:
            kill = True
    except:
        pass


def clear_start():
    if game_map[me.shipyard.position+Position(1,0)].is_occupied == False:
        future_pos[ship] = ship.position+Position(*Direction.East)
        ship_states[ship.id] = "collecting"
        return

    elif game_map[me.shipyard.position+Position(-1,0)].is_occupied == False:
        future_pos[ship] = ship.position+Position(*Direction.West)
        ship_states[ship.id] = "collecting"
        return

    elif game_map[me.shipyard.position+Position(0,1)].is_occupied == False:
        future_pos[ship] = ship.position+Position(*Direction.South)
        ship_states[ship.id] = "collecting"
        return
    
    elif game_map[me.shipyard.position+Position(0,-1)].is_occupied == False:
        future_pos[ship] = ship.position+Position(*Direction.North)
        ship_states[ship.id] = "collecting"
        return
    
    future_pos[ship] = ship.position+Position(*Direction.North)
    ship_states[ship.id] = "collecting"


def clear():   
    h_am = penis()
    direct = max(h_am, key= h_am.get) 
    move_pos = (direct)
    move = game_map.get_direction(ship,(direct))
    future_pos[ship] = ship.position+Position(*move)
    ship_states[ship.id] = "collecting"
    
    if game_map[ship.position+Position(*move)].is_occupied == False:
        future_pos[ship] = ship.position+Position(*move)
        ship_states[ship.id] = "collecting"

    else:
        di = go_nine_d(move)
        if not game_map[ship.position+Position(*di)].is_occupied:
            future_pos[ship] = ship.position+Position(*di)
            ship_states[ship.id] = "collecting"
        else:
            if game_map[me.shipyard.position+Position(1,0)].is_occupied == False:
                future_pos[ship] = ship.position+Position(*Direction.East)
                ship_states[ship.id] = "collecting"

            elif game_map[me.shipyard.position+Position(-1,0)].is_occupied == False:
                future_pos[ship] = ship.position+Position(*Direction.West)
                ship_states[ship.id] = "collecting"
            
            elif game_map[me.shipyard.position+Position(0,1)].is_occupied == False:
                future_pos[ship] = ship.position+Position(*Direction.South)
                ship_states[ship.id] = "collecting"
            
            
            elif game_map[me.shipyard.position+Position(0,-1)].is_occupied == False:
                future_pos[ship] = ship.position+Position(*Direction.North)
                ship_states[ship.id] = "collecting"


def spawn():
    
    if game.turn_number <=100:
        if me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied and(grand_total_current/grand_total_start)*100 >= 47:
            command_queue.append(me.shipyard.spawn())
    else:
    
        if best_fit(X_vals, depletion_per_round) <= -10 and (grand_total_current/grand_total_start)*100 <= 67 and min(depletion_per_round) <= (len(me.get_ships())-3)*28:
            no_more.append(1)
                  
        if len(no_more) == 0 and game.turn_number+170 <= constants.MAX_TURNS and (grand_total_current/grand_total_start)*100 >= 47:
            if me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
                command_queue.append(me.shipyard.spawn())
    
    if game.turn_number + constants.MAX_TURNS/2 >= constants.MAX_TURNS:
        if len(me.get_ships()) >= max(num_enemy_ships):
            if me.halite_amount + 20000 <= max(enemy_halite_amount):
                no_more.append(1)
    
    if len(no_more) == 0 and game.turn_number+170 >= constants.MAX_TURNS:
        no_more.append(1)
    
    if (grand_total_current/grand_total_start)*100 <= 47:
         no_more.append(1)
    if len(no_more) >= 1:
        logging.info(f"NO MORE SHIPS!!!!!!!!!!!!!!!")


def stay(): 
    future_pos[ship] = ship.position


while True:
    t1_start = time.time()
    t1 = time.time()
    game.update_frame()
    enemy_halite_amount = []
    num_enemy_ships = []
    command_queue = []
    dir_list = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
    future_pos = {}
    suicide_pos = {}
    total_collected = []
    time_to_suicide()
    
    k = []
    for position in deposit_locations:
        if position != me.shipyard.position:
            if not game_map[position].has_structure:
                k.append(position)

    for position in k:  
        deposit_locations.remove(position)


    t2 = time.time()
    logging.info(f"basic halite on map loop: {round(t2-t1,15)}")


    player_loop_start = time.time()

    for player in game.players.values():
        if player is not game.me:
            positions = []
            anti_time = []
            for eship in player.get_ships():
                for direction in dir_list:
                    game_map[eship.position+Position(*direction)].mark_e_ship(eship)     
                
                for eship1 in player.get_ships(): 
                    if eship.id != eship1.id:
                        if eship not in anti_time:
                            anti_time.append(eship)

                            surroundings = []
                            for x in range(-1*5,5+1):
                                for y in range(-1*5,5+1): 
                                        surroundings.append([x,y])   
                            r = []
                            for position in surroundings:
                                if game_map.calculate_distance(Position(0,0), Position(0,0)+Position(*position)) > 5:
                                    r.append(position)
                        
                            for position in r:
                                surroundings.remove(position)

                            e_ship1_positions = []
                            e_ship2_positions = []

                            for position in surroundings:
                                e_ship1_positions.append(eship1.position+Position(*position))
                                e_ship2_positions.append(eship.position+Position(*position))       
                            
                            dups = list(set(e_ship1_positions) & set(e_ship2_positions))
                            for locs in dups:
                                positions.append(locs)
                    
                for pos in positions:
                    game_map[pos].mark_insp(eship)


            for dropoffs in player.get_dropoffs():
                if dropoffs.position not in enemy_dropoffs:
                    enemy_dropoffs.append(dropoffs.position)
            
            num_enemy_ships.append(len(player.get_ships()))
            enemy_halite_amount.append(player.halite_amount)
    
    player_loop_end = time.time()
    logging.info(f"the player loop took: {round(player_loop_end-player_loop_start,10)}")

    t1 = time.time()
    halite_amount = map_s(game_map.height)
    t2 = time.time()
    logging.info(f"time to get map dir: {round(t2-t1,5)}")

    a = []
    for amount in halite_amount.values():
        a.append(amount)
    grand_total_current = sum(a[0:len(a)])



    ship_loop_start = time.time()
    for ship in me.get_ships(): 
        
    
        if game.turn_number <=5:
            if ship.id not in ship_states:
                ship_states[ship.id] = "clear_s"
        else: 
            if ship.id not in ship_states:
                ship_states[ship.id] = "clear"

        fuction_table = {
                    "suicide": (lambda : suicide()),
                    "clear": (lambda : clear()),
                    "stay": (lambda : stay()),
                    "clear_s": (lambda : clear_start()),
                    "deposit": (lambda : deposit()),
                    "collecting": (lambda : collecting()),
                    "make_drop":(lambda : dropoff_req())
                }

        if kill == True:
            ship_states[ship.id] = "suicide"
            suicide()

        fuction_table.get(ship_states.get(ship.id))()
    
    
    ship_loop_end = time.time()

    logging.info(f"the ship loop took: {round(ship_loop_end-ship_loop_start,20)}")


    if wait:
        counter +=1

    if counter >= 45:
        wait = False
        drop_ships.clear()
        if ship_states[ship.id] == "stay":
            ship_states[ship.id] = "collecting"

    dropoff_ = {
            0:19,
            1:26,
            2:34,
            3:40,
            4:45,
            5:50,
            6:60,
            7:73,
            8:80,
            9:90
                }
    
    if len(me.get_ships()) >= (dropoff_.get(len(me.get_dropoffs()),120)):
         dropoff_req()


    t1 = time.time()

    for ship, move in future_pos.items():
        total_collected.append(game_map[move].halite_amount*0.25)

    sm = sum(total_collected[0:len(total_collected)])
    depletion_per_round.append(sm)

    if game.turn_number >= 45:
        depletion_per_round.pop(0)

    t = []
    for ship,move in future_pos.items():
        for ship2, move2 in future_pos.items():
            if ship.id != ship2.id:
                if ship_states[ship.id] == "deposit":
                    if move == ship2.position:
                        if ship_states[ship2.id] != "deposit":
                            if ship2.position == move2:
                                t.append([ship2,move2])
    
    for ship, move in t:
        future_pos[ship] = move+Position(*go_nine_d(get_direction(ship.position,move)))

    if not kill:
        for ship,move in future_pos.items():
            if ship.position != me.shipyard.position:
                if game_map[ship.position].halite_amount != 0:
                    if ship.halite_amount < game_map[ship.position].halite_amount/constants.MOVE_COST_RATIO:
                        future_pos[ship] = ship.position

    t = []
    for ship,move in future_pos.items():
        for ship2, move2 in future_pos.items():
            if ship.id != ship2.id:
                if move == ship2.position:
                    if move2 == ship.position:
                        t.append([ship,move])
                        t.append([ship2,move2])
    
    for ship in t:
        t.remove(ship)
    
    for ship, move in t:
        command_queue.append(ship.move(game_map.switch(ship,move)))
        del future_pos[ship]
    
    
    m = []
    for ship,move in future_pos.items():
        for ship2, move2 in future_pos.items():
            if ship.id != ship2.id:  
                    if ship.position == move2:
                        check = game_map.get_direction(ship, move)
                        yes = Direction.invert(check)           
                        if ship.position+Position(*yes) != ship2.position:
                            if move != ship2.position:
                                if ship.position != move:
                                    if ship2.position != move2:
                                        j = []
                                        for shiz, movz in future_pos.items():
                                            if move == movz:
                                                    j.append(1)                                
                                        if len(j) == 2: 
                                            o = []  
                                            for shiz, movz in future_pos.items():
                                                if move == shiz.position:
                                                    if move2 == shiz.position:
                                                        o.append(1)                  
                                            if not o:
                                                m.append([ship,move])
                                                m.append([ship2,move2])
    k = []
    l = []
    for ship, move in m:
        for ship2, move2 in m:
            if ship.id != ship2.id:
                if move2 != move:
                    if move not in l:
                        l.append(move)
                        if ship.id not in k:    
                            k.append(ship.id)
                            del future_pos[ship]
                            command_queue.append(ship.move(game_map.better_nav(ship,move)))

    
    for ship, move in future_pos.items(): 
        if ship.position == move: 
            command_queue.append(ship.move(game_map.better_nav(ship,move)))
        else:
            command_queue.append(ship.move(game_map.better_nav(ship, move)))                       
    
    for ship, move in suicide_pos.items():
        command_queue.append(ship.move(game_map.get_direction(ship, move)))

    if not wait:
        spawn()
    
   

    t2_end = time.time()
    logging.info(f"it took: {round(t2_end-t1,20)} to enter commands")

    logging.info(f"i have: {len(me.get_ships())} ships!")


    logging.info(f"total time is: {round(t2_end-t1_start,4)}")

    game.end_turn(command_queue)
    

