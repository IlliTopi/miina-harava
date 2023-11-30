import sweeperlib
import random
import math
import copy

state = {
    "field": [],
    "visible_field": [],
    "status": "game",
    "info": "Hidden safe tiles: 0 | Mines: 10",
    "height": 0,
    "width": 0,
}



def place_mines(field_to_mine,available_tiles,num_of_mines):
    """
    Places N mines to a field in random tiles.
    """
    mines = random.sample(range(0,len(available_tiles)),num_of_mines)
    for mine_index in mines:
        field_to_mine[available_tiles[mine_index][1]][available_tiles[mine_index][0]] = "x"
    
def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    global height
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    if state["status"] == "game":
        for y in range(len(state["visible_field"])):
            for x in range(len(state["visible_field"][y])):
                sweeperlib.prepare_sprite(state["visible_field"][y][x],x*40,y*40)
                
    if state["status"] == "ending":
        for y in range(len(state["field"])):
            for x in range(len(state["field"][y])):
                sweeperlib.prepare_sprite(state["field"][y][x],x*40,y*40)
    sweeperlib.draw_sprites()
    sweeperlib.draw_text(state["info"], 10, state["height"] + 40,font='arial', size = 10)

def click_handler(x,y,button,_):
    if y  <= state["height"] and state["status"] == "game":
        click_tile = {"col": math.floor(x/40), "row": math.floor(y/40)}
        if button == sweeperlib.MOUSE_LEFT:
            floodfill(state["field"],click_tile["col"],click_tile["row"])
        if button == sweeperlib.MOUSE_RIGHT:
            """ state["field"][click_tile["row"]][click_tile["col"]] = "f" """
            state["visible_field"][click_tile["row"]][click_tile["col"]] = "f"
    

def floodfill(planet,x_pos,y_pos):
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """
    #If the clicked tile is a bomb
    if(planet[y_pos][x_pos] == "x"):
        state["status"] = "ending" 
        return
    check_tiles = [(x_pos,y_pos)]
    #Directions for checking tiles
    directions = [(1,1),(0,1),(-1,1),(1,0),(-1,0),(1,-1),(0,-1),(-1,-1)]   
    while len(check_tiles) > 0:
        x, y = check_tiles.pop()
        surrounding_tiles = []
        #Tiles surrounding bombs count
        bomb_count = 0
        for dir_x, dir_y in directions:
            tile_x = x + dir_x
            tile_y = y + dir_y
            #Checks if tile is inside of the bounds.
            if(0 <= tile_x < len(planet[0]) and 0 <= tile_y < len(planet)):
                #Checks if tile is a bomb
                if planet[tile_y][tile_x] == "x":
                    bomb_count += 1
                #Checks if tile is not checked before
                elif planet[tile_y][tile_x] == " ":
                    surrounding_tiles.append((tile_x,tile_y))
        if bomb_count == 0:
            for tile in surrounding_tiles:
                #Surrounding x and y coordinates
                surr_x,surr_y = tile
                planet[surr_y][surr_x] = "0"
                state["visible_field"][surr_y][surr_x] = "0"
                if tile not in check_tiles:
                    check_tiles.append(tile)
        planet[y][x] = str(bomb_count)
        state["visible_field"][y][x] = str(bomb_count)

def main():
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """
    sweeperlib.load_sprites("./sprites")
    sweeperlib.create_window(state["width"],state["height"]+80)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.set_mouse_handler(click_handler)
    sweeperlib.start()
    
def input_int(prompt):
    while True:
        try:
            given_number = int(input(prompt))
            return given_number
        except ValueError:
            print("It has to be whole numbers")

def start_game():
    state["width"] = input_int("Number of columns: ") * 40
    state["height"] = input_int("Number of rows: ") * 40
    number_of_mines = input_int("Number of mines: ")

    field = []
    available_tiles = []
    for row in range(math.floor(state["height"]/40)):
        field.append([])
        for col in range(math.floor(state["width"]/40)):
            field[-1].append(" ")
            available_tiles.append((col,row))
    state["field"] = field
    state["visible_field"] = copy.deepcopy(field)
    place_mines(state["field"],available_tiles,number_of_mines)
    main()

if __name__ == "__main__":
    start_game()
