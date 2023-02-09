# %%
import pandas as pd
import numpy as np

# %%
dist_retas = pd.read_excel('./retas.xlsx', index_col=0)
dist_estacoes = pd.read_excel('https://github.com/tnpb-1st/if684-projeto-busca-estrela/blob/master/station-distances.xlsx?raw=true',index_col=0)
all_dists = pd.read_excel('https://github.com/tnpb-1st/if684-projeto-busca-estrela/blob/master/all_distances.xlsx?raw=true',index_col=0)

def make_stations_dic(dist_estacoes):
  # Dado que B = Linha Blue, Y = Linha Yellow, G = Linha Green, R = Linha Red;
  dici = {}
  for ind in dist_estacoes.index:
    for col in dist_estacoes.columns:
      if type(dist_estacoes.loc[ind,col]) != type(np.nan):
        e1, e2 = ind, col
        dist,line = dist_estacoes.loc[ind,col].split('-')
        dist = float(dist.replace(',','.'))
        if line == 'yellow':
          line = 'Y'
        elif line == 'green':
          line = 'G'
        elif line == 'blue':
          line = 'B'
        else:
          line = 'R'
        if e1 not in dici:
          dici[e1] = {e2: (dist, line)}
        else:
          dici[e1][e2] = (dist, line)
        if e2 not in dici:
          dici[e2] = {e1 : (dist, line)}
        else:
          dici[e2][e1] = (dist, line)
  return dici

def make_heuristic_dic(all_dists):
    dic = {}
    for ind in all_dists.index:
        for col in all_dists.columns:
            if type(all_dists.loc[ind,col] != np.nan):
                e1, e2 = ind, col
                dist = all_dists.loc[ind,col]
                # dist = float(dist.replace('.', ','))
                if e1 not in dic:
                    dic[e1] = {}
                if e2 not in dic:
                    dic[e2] = {}
                
                if e1 == e2:
                    dic[e1][e2] = 0
                elif not np.isnan(dist):

                    dic[e1][e2] = dist
                    dic[e2][e1] = dist

    return dic


def distancia_para_tempo_em_minutos(dist):
    return dist*2
# %%
INF = int(2e9)
class Mapa:
    def __init__(self, est_ini, linha_ini, est_fin, debug=False):
        self.dist_real = make_stations_dic(dist_estacoes)
        self.dist_heuristica =  make_heuristic_dic(all_dists)
        self.linhas_possiveis = {
            'E1':['B'],  
            'E2': ['B','Y'],
            'E3': ['B','R'],
            'E4': ['B','G'],
            'E5': ['B','Y']        ,
            'E6': ['B'],
            'E7': ['Y'],
            'E8': ['G','Y'],
            'E9': ['R','Y'],
            'E10': ['Y'],
            'E11': ['R'],
            'E12': ['G'],
            'E13': ['G','R'],
            'E14': ['G']
        }

        
        self.grid = {}
        for station in dist_retas.index:
            for linha in self.linhas_possiveis[station]:
                self.grid[(station, linha)] = {"nome": station, "f": INF, "g": INF, "h": INF, "est_pai": None, "visitado": False}

        self.linhas_percorridas = []
        self.est_to_idx = {}

        for i,est in enumerate(dist_retas.index):
            self.est_to_idx[est] = i
        self.est_inicial = est_ini
        self.linha_ini = linha_ini
        self.est_final = est_fin
        self.debug = debug

        if self.linha_ini not in self.linhas_possiveis[self.est_inicial]:
            raise TypeError(f"A linha {self.get_linha_atual_str(self.linha_ini)} não passa pela estação {self.est_inicial}")

    def gera_fronteira(self, est, linha_atual):
        est_vizinhas = self.dist_real[est]
        est_on_grid = self.grid[(est, linha_atual)]

        fronteira = []
        for est_vizinha, info in est_vizinhas.items():
            linha_vizinha = info[1]
            est_visitada = self.grid[(est_vizinha, linha_vizinha)]['visitado']
            est_pai = self.grid[(est_vizinha, linha_vizinha)]['est_pai']
            if est_visitada or est_pai == est_on_grid:
                continue
            fronteira.append((est_vizinha, linha_vizinha))
        return fronteira

    @staticmethod
    def calcula_f(est_no_grid):
        return est_no_grid['g'] + est_no_grid['h']


    def atualiza_grid(self, est_atual, fronteira, linha_atual):
        est_pai = self.grid[(est_atual, linha_atual)]
        g_pai = est_pai["g"] if est_pai and est_pai["g"] < INF else 0


        for est_fronteira, linha_para_est in fronteira:
            est_no_grid = self.grid[(est_fronteira, linha_para_est)]
            dist_para_est = self.dist_real[est_atual][est_fronteira][0]
            tempo_para_est = distancia_para_tempo_em_minutos(dist_para_est)
            baldeacao = 4 if linha_atual != linha_para_est else 0
            
            g = g_pai + tempo_para_est + baldeacao

            h = distancia_para_tempo_em_minutos(self.dist_heuristica[est_fronteira][self.est_final])

            possivel_f = g + h
            f_atual = self.calcula_f(est_no_grid)
            if possivel_f < f_atual:
                est_no_grid['g'] = g
                est_no_grid['h'] = h
                est_no_grid['f'] = possivel_f
                est_no_grid['est_pai'] = self.grid[(est_atual, linha_atual)]


    def seleciona_menor_f_do_grid(self):
        menor_est = (None, None)
        menor_f = INF

        for key, values in self.grid.items():
            est, linha = key

            if values['f'] < menor_f and not values['visitado']:
                menor_f = values['f']
                menor_est = (est, linha)
        return menor_est

    def recupera_caminho(self, est_final, linha_final):
        est_atual = self.grid[(est_final, linha_final)]
        caminho = []
        while est_atual.get('est_pai'):
            caminho.append(est_atual['nome'])
            est_atual = est_atual['est_pai']
        caminho.reverse()
        return caminho
    
    def get_linha_atual_str(self, linha):
        linha_dict = {
            'G': 'verde',
            'Y': 'amarela',
            'B': 'azul',
            'R': 'vermelha'
        }
        return linha_dict.get(linha, "N/A")

    def melhor_caminho(self):
        est_atual = self.est_inicial
        linha_atual = self.linha_ini
        while est_atual != self.est_final:
            fronteira = self.gera_fronteira(est_atual, linha_atual)
            self.atualiza_grid(est_atual, fronteira, linha_atual)

            if self.debug:
                print(f"Estação atual: {est_atual}")
                print(f"Linha atual: {self.get_linha_atual_str(linha_atual)}")
                print(f"Fronteira de {est_atual}:")
                
                for est in fronteira:
                    est_no_grid = self.grid[est]
                    print(f"\t{est}: G = {est_no_grid['g']}, H = {est_no_grid['h']}, F = {est_no_grid['f']}")
                print("\n")

            self.grid[(est_atual, linha_atual)]['visitado'] = True
            prox_est = self.seleciona_menor_f_do_grid()

            if self.grid[prox_est]['est_pai']:
                est_conectada = self.grid[prox_est]['est_pai']['nome']
            else:
                est_conectada = est_atual
            linha_atual = self.dist_real[est_conectada][prox_est[0]][1]
            est_atual = prox_est[0]
        
        caminho = self.recupera_caminho(self.est_final, linha_atual)
        # formatação do output
        caminho.insert(0, self.est_inicial)
        caminho_str = '\\' + '='*80 + '|\n'
        caminho_str += "o caminho mais rápido é: " + ' -> '.join(caminho) + '\n'
        tempo_final = self.grid[(self.est_final, linha_atual)]['g']
        caminho_str += f"o tempo total do trajeto é de {round(tempo_final,2)} minutos\n"
        return caminho_str

        
mapa1 = Mapa('E1', 'B', "E14", debug=False)
# print(mapa1.melhor_caminho())

# mapa2 = Mapa('E12', 'G', 'E5', debug=True)
# print(mapa2.melhor_caminho())


# %%



