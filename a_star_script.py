# %%
import pandas as pd
import numpy as np

# %%
dist_retas = pd.read_excel('./retas.xlsx', index_col=0)
dist_estacoes = pd.read_excel('https://github.com/tnpb-1st/if684-projeto-busca-estrela/blob/master/station-distances.xlsx?raw=true',index_col=0)



# %%
df_direto = dist_retas.copy(deep=True)
for r in df_direto.index:
  for c in df_direto.columns:
    if df_direto.loc[r,c]:
      df_direto.loc[r,c] = df_direto.loc[r,c] * 2
      df_direto.loc[c,r] = df_direto.loc[r,c]
df_direto.to_csv('retas.csv')

# %%
# dist_retas.index
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

def distancia_para_tempo_em_minutos(dist):
    return dist*2
# %%
INF = int(2e9)
class Mapa:
    def __init__(self, est_ini, linha_ini, est_fin, debug=False):
        self.dist_real = make_stations_dic(dist_estacoes)
        self.dist_heuristica = {
            'E1' :{
                'E1' : 0,
                'E2' : 10,
                'E3' : 18.5,
                'E4' : 24.8,
                'E5' : 36.4,
                'E6' : 38.8,
                'E7' : 35.8,
                'E8' : 25.4,
                'E9' : 17.6,
                'E10' : 9.1,
                'E11' : 16.7,
                'E12' : 27.3,
                'E13' : 27.6,
                'E14' : 29.8
                
            },
            'E2' :{
                'E1' : 10,
                'E2' : 0,
                'E3' : 8.5,
                'E4' : 14.8,
                'E5' : 26.6,
                'E6' : 29.1,
                'E7' : 26.1,
                'E8' : 17.3,
                'E9' : 10,
                'E10' : 3.5,
                'E11' : 15.5,
                'E12' : 20.9,
                'E13' : 19.1,
                'E14' : 21.8
                },

            'E3' :{
                'E1' : 18.5,
                'E2' : 8.5,
                'E3' : 0,
                'E4' : 6.3,
                'E5' : 18.2,
                'E6' : 20.6,
                'E7' : 17.6,
                'E8' : 13.6,
                'E9' : 9.4,
                'E10' : 10.3,
                'E11' : 19.5,
                'E12' : 19.1,
                'E13' : 12.1,
                'E14' : 16.6
                },
            'E4'  :{
                'E1' : 24.8,
                'E2' : 14.8,
                'E3' : 6.3,
                'E4' : 0,
                'E5' : 12,
                'E6' : 14.4,
                'E7' : 11.5,
                'E8' : 12.4,
                'E9' : 12.6,
                'E10' : 16.7,
                'E11' : 23.6,
                'E12' : 18.6,
                'E13' : 10.6,
                'E14' : 15.4
            },

            'E5'  :{
                'E1' : 36.4,
                'E2' : 26.6,
                'E3' : 18.2,
                'E4' : 12,
                'E5' : 0,
                'E6' : 3,
                'E7' : 2.4,
                'E8' : 19.4,
                'E9' : 23.3,
                'E10' : 28.2,
                'E11' : 34.2,
                'E12' : 24.8,
                'E13' : 14.5,
                'E14' : 17.9
                
            },   
            'E6'  :{
                'E1' : 38.8,
                'E2' : 29.1,
                'E3' : 20.6,
                'E4' : 14.4,
                'E5' : 3,
                'E6' : 0,
                'E7' : 3.3,
                'E8' : 22.3,
                'E9' : 25.7,
                'E10' : 30.3,
                'E11' : 36.7,
                'E12' : 27.6,
                'E13' : 15.2,
                'E14' : 18.2
                
            },    
            'E7'  :{
                'E1' : 35.8,
                'E2' : 26.1,
                'E3' : 17.6,
                'E4' : 11.5,
                'E5' : 2.4,
                'E6' : 3.3,
                'E7' : 0,
                'E8' : 20,
                'E9' : 23,
                'E10' : 27.3,
                'E11' : 34.2,
                'E12' : 25.7,
                'E13' : 12.4,
                'E14' : 15.6

            },    
            'E8'  :{
                'E1' : 25.4,
                'E2' : 17.3,
                'E3' : 13.6,
                'E4' : 12.4,
                'E5' : 19.4,
                'E6' : 22.3,
                'E7' : 20,
                'E8' : 0,
                'E9' : 8.2,
                'E10' : 20.3,
                'E11' : 16.1,
                'E12' : 6.4,
                'E13' : 22.7,
                'E14' : 27.6

            },    
            'E9'  :{
                'E1' : 17.6,
                'E2' : 10,
                'E3' : 9.4,
                'E4' : 12.6,
                'E5' : 23.3,
                'E6' : 25.7,
                'E7' : 23,
                'E8' : 8.2,
                'E9' : 0,
                'E10' : 13.5,
                'E11' : 11.2,
                'E12' : 10.9,
                'E13' : 21.2,
                'E14' : 26.6
            },

            'E10'  :{
                'E1' : 9.1,
                'E2' : 3.5,
                'E3' : 10.3,
                'E4' : 16.7,
                'E5' : 28.2,
                'E6' : 30.3,
                'E7' : 27.3,
                'E8' : 20.3,
                'E9' : 13.5,
                'E10' : 0,
                'E11' : 17.6,
                'E12' : 24.2,
                'E13' : 18.7,
                'E14' : 21.2
            },
            
            'E11'  :{
                'E1' : 16.7,
                'E2' : 15.5,
                'E3' : 19.5,
                'E4' : 23.6,
                'E5' : 34.2,
                'E6' : 36.7,
                'E7' : 34.2,
                'E8' : 16.1,
                'E9' : 11.2,
                'E10' : 17.6,
                'E11' : 0,
                'E12' : 14.2,
                'E13' : 31.5,
                'E14' : 35.5,
            },
            
            'E12'  :{
                'E1' : 27.3,
                'E2' : 20.9,
                'E3' : 19.1,
                'E4' : 18.6,
                'E5' : 24.8,
                'E6' : 27.6,
                'E7' : 25.7,
                'E8' : 6.4,
                'E9' : 10.9,
                'E10' : 24.2,
                'E11' : 14.2,
                'E12' : 0,
                'E13' : 28.6,
                'E14' : 33.6,
                },
            'E13'  :{
                'E1' : 27.6,
                'E2' : 19.1,
                'E3' : 12.1,
                'E4' : 10.6,
                'E5' : 14.5,
                'E6' : 15.2,
                'E7' : 12.4,
                'E8' : 22.7,
                'E9' : 21.2,
                'E10' : 18.7,
                'E11' : 31.5,
                'E12' : 28.8,
                'E13' : 0,
                'E14' : 5.1,
                },
            'E14'  :{
                'E1' : 29.8,
                'E2' : 21.8,
                'E3' : 16.6,
                'E4' : 15.4,
                'E5' : 17.9,
                'E6' : 18.2,
                'E7' : 15.6,
                'E8' : 27.6,
                'E9' : 26.6,
                'E10' : 21.2,
                'E11' : 35.5,
                'E12' : 33.6,
                'E13' : 5.1,
                'E14' : 0,
            }
        }

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

        
        self.grid = {station: {"nome": station, "f": INF, "g": INF, "h": INF, "est_pai": None, "visitado": False} for station in dist_retas.index}

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

    def gera_fronteira(self, est):
        est_vizinhas = list(self.dist_real[est].keys())
        fronteira = est_vizinhas[:]
        for est_vizinha in est_vizinhas:
            est_visitada = self.grid[est_vizinha]['visitado']
            est_pai = self.grid[est_vizinha]['est_pai']
            if est_visitada or est_pai == est:
                fronteira.remove(est_vizinha)
        return fronteira

    @staticmethod
    def calcula_f(est_no_grid):
        return est_no_grid['g'] + est_no_grid['h']


    def atualiza_grid(self, est_atual, fronteira, linha_atual):
        est_pai = self.grid[est_atual]
        g_pai = est_pai["g"] if est_pai and est_pai["g"] < INF else 0


        for est_fronteira in fronteira:
            est_no_grid = self.grid[est_fronteira]
            dist_para_est, linha_para_est = self.dist_real[est_atual][est_fronteira]
            tempo_para_est = distancia_para_tempo_em_minutos(dist_para_est)
            baldeacao = 4 if linha_atual != linha_para_est else 0
            
            g = g_pai + tempo_para_est + baldeacao

            h = self.dist_heuristica[est_fronteira][self.est_final]

            possivel_f = g + h
            f_atual = self.calcula_f(est_no_grid)
            if possivel_f < f_atual:
                est_no_grid['g'] = g
                est_no_grid['h'] = h
                est_no_grid['f'] = possivel_f
                est_no_grid['est_pai'] = self.grid[est_atual]


    def seleciona_menor_f_do_grid(self):
        menor_est = 'E1'
        menor_f = self.grid[menor_est]['f']

        for est, values in self.grid.items():
            if values['f'] < menor_f and not values['visitado']:
                menor_f = values['f']
                menor_est = est
        return menor_est

    def recupera_caminho(self, est_final=None):
        if est_final is None:
            est_final = self.est_final

        est_atual = self.grid[est_final]
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
            fronteira = self.gera_fronteira(est_atual)
            self.atualiza_grid(est_atual, fronteira, linha_atual)

            if self.debug:
                print(f"Estação atual: {est_atual}")
                print(f"Linha atual: {self.get_linha_atual_str(linha_atual)}")
                print(f"Fronteira de {est_atual}:")
                
                for est in fronteira:
                    est_no_grid = self.grid[est]
                    print(f"\t{est}: G = {est_no_grid['g']}, H = {est_no_grid['h']}, F = {est_no_grid['f']}")
                print("\n")

            self.grid[est_atual]['visitado'] = True
            prox_est = self.seleciona_menor_f_do_grid()

            if self.grid[prox_est]['est_pai']:
                est_conectada = self.grid[prox_est]['est_pai']['nome']
            else:
                est_conectada = est_atual
            linha_atual = self.dist_real[est_conectada][prox_est][1]
            est_atual = prox_est
        
        caminho = self.recupera_caminho()
        # formatação do output
        caminho.insert(0, self.est_inicial)
        caminho_str = '\\' + '='*80 + '|\n'
        caminho_str += "o caminho mais rápido é: " + ' -> '.join(caminho) + '\n'
        tempo_final = self.grid[self.est_final]['g']
        caminho_str += f"o tempo total do trajeto é de {round(tempo_final,2)} minutos\n"
        return caminho_str

        
mapa = Mapa('E11', 'R', "E14", debug=True)

print(mapa.melhor_caminho())


# %%



