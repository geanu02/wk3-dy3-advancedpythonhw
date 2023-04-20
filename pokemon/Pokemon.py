from IPython.display import Image, clear_output
import requests

class Pokemon():
    def __init__(self, input_str):
        self.input_str = input_str
        self.poke_name = None
        self.poke_id = None
        self.abilities = []
        self.types = []
        self.weight = None
        self.image = None
        self.evolves_to = []
        self.evo_info = None
        self.all_moves = []
        self.learned_moves = []
        self.call_poke_api()
        
    def call_poke_api(self):
        info_res = self.api_call(f"https://pokeapi.co/api/v2/pokemon/{self.input_str}")
        if info_res[0] == 200:
            data = info_res[1]
            self.poke_id = data['id']
            self.poke_name = data['name']
            self.abilities = [abi['ability']['name'] for abi in data['abilities']]
            self.types = [typ['type']['name'] for typ in data['types']]
            self.weight = data['weight']
            self.image = data['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
            self.all_moves = list(set([move['move']['name'] for move in data['moves']]))
            self.learned_moves = self.fill_learned_moves()
            if not self.image:
                self.image = data['sprites']['front_default']
            species_res = self.api_call(data['species']['url'])
            if species_res[0] == 200:
                evolution_res = self.api_call(species_res[1]['evolution_chain']['url'])
                if evolution_res[0] == 200:
                    self.evo_info = evolution_res[1]
                    self.fill_evolutions()
                else:
                    print(f"Error Get Evolutionary Chain: Status Code {evolution_res[0]}")
                
            else:
                print(f"Error Get Species: Status Code {species_res[0]}")
        else:
            print(f"Error Get Info: Status Code {info_res[0]}")
            
    def print_pokemon(self):
        return display(Image(self.image, width = 200))
    
    def evolve(self):
        if self.evolves_to == None:
            print("This Pokemon does not evolve.")
        else:
            confirm_evo = input(f"Evolve {self.poke_name.title()} to {self.evolves_to.title()}? (y/n) ").lower()
            if confirm_evo == 'y' or confirm_evo == 'yes':
                pass
            elif confirm_evo == 'n' or confirm_evo == 'no':
                print("Evolution cancelled.")
            else:
                print("Not a valid response. Evolution cancelled.")
            
# Recursive Evolutionary Method
#     def get_evolution_chain(self):
#         response = get(self.species_url)
#         if response.status_code == 200:
#             data = response.json()
#         evolution_chain_url = data['evolution_chain']['url']
#         evolution_chain = get(evolution_chain_url)
#         if evolution_chain.status_code == 200:
#             return evolution_chain.json()['chain']
            
    def evolve_pokemon(self, evolution_chain):
        if not evolution_chain['evolves_to']:
            print(f'This is the final from')
            return
        current_pokemon_in_chain = evolution_chain['species']['name']
        next_pokemon_in_chain = evolution_chain['evolves_to'][0]['species']['name']
        if current_pokemon_in_chain == self.name:
            self.name = next_pokemon_in_chain
            self.call_poke_api()
            return
        else:
            return self.evolve_pokemon(evolution_chain['evolves_to'][0])
            
    def fill_evolutions(self):
        self.evolves_to = []
        if self.evo_info['chain']['species']['name'] == self.poke_name:
            for _name in self.evo_info['chain']['evolves_to']:
                self.evolves_to.append(_name['species']['name'])
        elif self.evo_info['chain']['evolves_to'][0]['species']['name'] == self.poke_name:
            for _name in self.evo_info['chain']['evolves_to'][0]['evolves_to']:
                self.evolves_to.append(_name['species']['name'])
        else:
            self.evolves_to = []
    
    def fill_learned_moves(self):
        moves_to_learn = []
        if len(self.all_moves) > 4:
            for idx in range(0, 4):
                moves_to_learn.append(self.all_moves[idx])
        else:
            for idx in range(0, len(self.all_moves)):
                moves_to_learn.append(self.all_moves[idx])
        return moves_to_learn

    def api_call(self, endpoint_url):
        res = requests.get(endpoint_url)
        if res.status_code == 200:
            return (200, res.json())
        else:
            return ({res.status_code}, {})