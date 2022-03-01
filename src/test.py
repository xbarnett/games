import pexpect
import json

def get_fname(game_name):
    agda_dir = "/home/will/Documents/personal/x/X/Games/"
    return agda_dir + game_name + ".agda"

def get_agda_command(fname, expr=None):
    if expr is None:
        command = f"Cmd_load \"{fname}\" []"
    else:
        command = f"Cmd_compute_toplevel IgnoreAbstract \"{expr}\""
    return bytes(f"IOTCM \"{fname}\" None Direct ({command})\n", "utf-8")

def agda_initialise(fname):
    child = pexpect.spawn("agda --interaction-json")
    child.expect("JSON> ")
    child.send(get_agda_command(fname))
    child.expect("JSON> ")
    return child

class AgdaError(Exception):
    pass

def agda_compute(child, fname, expr):
    try:
        child.send(get_agda_command(fname, expr))
        child.expect("JSON> ")
        output = child.before.decode("UTF-8")
        return json.loads(output.split("\n")[-2])["info"]["expr"]
    except KeyError:
        raise AgdaError(output)

def get_move(state):
    while True:
        move = input("move: ")
        if move == "flip":
            break
    return f"make-move {state} {move}"

def process_state(game_prefix, state):
    n = len(game_prefix)
    return state[n:]

def main():
    game_name = "BitFlip"
    game_prefix = "X.Games." + game_name + "."
    fname = get_fname(game_name)

    print(f"loading {game_name}...")
    child = agda_initialise(fname)
    print(game_name)
    print()
    state = "initial-state"
    while True:
        print(state)
        expr = get_move(state)
        state = process_state(game_prefix, agda_compute(child, fname, expr))
        print()

if __name__ == "__main__":
    main()
