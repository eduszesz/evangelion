import pygame
import random
import math
import array
import sys
import os
import json

# --- Configurações Gerais ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 980
FONT_SIZE = 24
TILE_WIDTH, TILE_HEIGHT = 20, 30
MAP_WIDTH = (SCREEN_WIDTH - 300) // TILE_WIDTH 
MAP_HEIGHT = (SCREEN_HEIGHT-130 )// TILE_HEIGHT
MAX_INVENTORY = 9
FINAL_LEVEL = 12

#For debug: jogador invensivel
INVENSIVEL = False

# --- Paleta de Cores ---
COLOR_BG = (0, 0, 0)
COLOR_FOG = (40, 40, 45)
COLOR_DARK_FOG = (20, 20, 30)
COLOR_WALL = (160, 170, 180)      
COLOR_FLOOR = (90, 95, 100)       
COLOR_PLAYER = (0, 255, 128)      
COLOR_GUARD = (255, 80, 80)       
COLOR_DRONE = (0, 220, 255)       
COLOR_CAMERA = (220, 120, 255)    
COLOR_LASER_ON = (255, 50, 50)    
COLOR_LASER_OFF = (60, 60, 60)    
COLOR_TERMINAL = (0, 255, 255)
COLOR_ITEM = (255, 255, 0)
COLOR_TEXT_BG = (0, 0, 0)         
COLOR_STUNNED = (100, 180, 255)
COLOR_STAIRS_READY = (255, 255, 0)
COLOR_STAIRS_LOCKED = (80, 80, 80)
COLOR_WIN = (100, 255, 100)
COLOR_MSG_NOTE = (255, 255, 255)
COLOR_DOG = (255, 120, 0) 
COLOR_STAIR_UP = (0,100,255)
COLOR_SECRET_FLOOR = (0,220,80)
COLOR_SECRET_DOOR = (150,150,150)
COLOR_BARS = (140, 140, 150) # Cor metálica para a prisão
COLOR_PANEL = (200, 200, 200)
COLOR_ENG = (200, 200, 100)
COLOR_SHOP = (255, 215, 0) # Dourado para a loja

# Tiles
TILE_WALL, TILE_FLOOR = '#', '.'
TILE_SECRET_DOOR = "%"
TILE_SECRET_FLOOR = "S"
TILE_STAIR_DOWN = '>'
TILE_STAIR_UP = "<"
TILE_SPIKES, TILE_SENSOR, TILE_DRUNK = '^', 's', ";"
TILE_LASER_V, TILE_LASER_H = '|', '-'
TILE_TERMINAL, TILE_ITEM = 'T', '*'
TILE_MESSAGE = chr(9834) # ♪
TILE_BIBLE = "B"
TILE_BARS_1 = '/'
TILE_BARS_2 = '\\'
TILE_PRISON = "p"
TILE_CAMERA = "C"
TILE_PANEL = "&"
TILE_DECOY = chr(0x0394) #delta
TILE_SHOP = '$'

SOUND_CACHE = {}
LAST_BEEP_T = 0


# --- Dicionário de Textos (Bilingue) ---
TEXTS = {
    "EN": {
        "sub_title": "A Stealth Roguelike Game",
        "start_new": "(N / SPACE) NEW GAME",
        "start_load": "(C / L) LOAD GAME",
        "start_music": "(M) MUSIC: {}",
        "start_lang": "(T) LANGUAGE: ENGLISH",
        "start_quit": "(Q) QUIT",
        "music_on": "ON",
        "music_off": "OFF",
        "fail_title": "MISSION FAILED",
        "fail_sub": "Level {}. Press SPACE to restart.",
        "win_title": "MISSION ACCOMPLISHED!",
        "win_sub": "You escaped with the Book. Press SPACE.",
        "hud_lvl": "LEVEL: {}/{}",
        "hud_stun": "PARALYZED: {}",
        "hud_drunk": "POISONED: {}",
        "hud_inv": "INVISIBLE: {}",
        "hud_hack_prog": "HACK PROGRESS:",
        "hud_hack_done": "MESSAGE SENT!",
        "hud_hack_do": "HACK TERMINAL",
        "hud_alarm": "ALARM: {}",
        "hud_inv_title": "INVENTORY ({}/{}):",
        "hud_full": "!! BACKPACK FULL !!",
        "hud_faith": "Faith: {}/100",
        "caught_map": "CAUGHT!",
        "menu_title": "MENU",
        "opt_music": "(M) Toggle Music",
        "opt_restart": "(R) Restart Game",
        "opt_save": "(S) Save Game",
        "opt_load": "(L/C) Load Game",
        "opt_lang": "(T) Language: EN",
        "opt_resume": "(ESC) Resume Game",
        "opt_quit": "(Q) Quit",
        "save_title": "SAVE GAME TO WHICH SLOT?",
        "load_title": "LOAD WHICH SLOT?",
        "slot_occ": "[OCCUPIED]",
        "slot_emp": "[EMPTY]",
        "slot_txt": "({}) - Slot {} {}",
        "slot_del": "(X + Number) DELETE SLOT",
        "slot_back": "(ESC) Back",
        "log_shop_enter": "SYSTEM: SHOP ACCESSED. Press a letter then an inventory number to swap.",
        "log_shop_inst": "SYSTEM: Trades left: {}.",
        "log_shop_swap": "SYSTEM: Swapped {} for {}!",
        "log_shop_closed": "SYSTEM: Shop closed.",
        "log_shop_visited": "SYSTEM: The shop is already closed.",
        "log_shop_sel": "SYSTEM: Selected {} ({}). Choose your inventory item (1-9).",
        "log_intro1": "Descend to level 12 to find the great Book and return with the truth!",
        "log_intro2": "On your journey, find the message and broadcast it to the world!",
        "log_intro3": "Do this stealthily! The enemy wants to stop the good news from reaching everyone!",
        "log_emp": "YOU PUT AN ENEMY TO SLEEP!",
        "log_kit": "ANTIDOTE APPLIED, YOU CAN MOVE NORMALLY!",
        "log_inv1": "SYSTEM: SMOKE BOMB DETONATED!",
        "log_inv2": "YOU ARE INVISIBLE!",
        "log_hack": "DEVICE HACKED!",
        "log_tun_in": "Entering a secret tunnel",
        "log_tun_out": "Leaving a secret tunnel",
        "log_msg_req": "SYSTEM: FIND THE MESSAGE ♪ FIRST!",
        "log_alarm": "ALARM ACTIVE!",
        "log_intruder": "ALERT: INTRUDER DETECTED IN SECTOR!",
        "log_hack_ok": "SYSTEM: ACCESS GRANTED. DATA TRANSMITTED.",
        "log_msg_sent": "MESSAGE SENT!",
        "log_full": "FULL!",
        "log_book_get": "YOU NOW HAVE THE BOOK! RETURN TO LEVEL 1!",
        "log_item": "ITEM ACQUIRED.",
        "log_spike1": "PARALYZED! AWAKE, O SLEEPER!",
        "log_spike2": "SYSTEM: MAPPING DATA CORRUPTED!",
        "log_drunk1": "POISONED! WHAT I WANT TO DO I DO NOT DO...",
        "log_last_lvl": "THIS IS THE LAST LEVEL! GET THE BOOK AND RETURN TO LEVEL 1!",
        "log_need_book": "YOU NEED TO GET THE BOOK ON LEVEL 12 BEFORE ESCAPING!",
        "log_return": "RETURNING TO LEVEL {}",
        "log_dog": "DOG DETECTED SCENT!",
        "log_save_ok": "SYSTEM: GAME SAVED SUCCESSFULLY IN SLOT {}.",
        "log_save_err": "SAVE ERROR: {}",
        "log_load_ok": "SYSTEM: SLOT {} LOADED SUCCESSFULLY.",
        "log_load_emp": "SYSTEM: SLOT {} IS EMPTY.",
        "log_load_err": "LOAD ERROR: {}",
        "log_del_ok": "SYSTEM: SLOT {} DELETED SUCCESSFULLY.",
        "log_del_emp": "SYSTEM: SLOT {} WAS ALREADY EMPTY.",
        "log_del_err": "DELETE ERROR: {}",
        "log_dark": "SYSTEM: POWER RESTORED",
        "log_dark1": "SYSTEM: POWER CUT OFF! REDUCED VISION!",
        "log_dark2": "Banging on the power panel...",
        "log_pray": "Preach and pray",
        "log_convert": "Turn now, each of you, from your evil ways",
        "log_resist": "Cold heart of stone",
        "log_faith": "You are full of faith! Press ""P"" to preach and pray. Maybe someone is going to repent...",
        "desc_DECOY": "DECOY: Drops a device that activates after 7 turns, luring guards.",
        "log_decoy_drop": "DECOY PLANTED! ACTIVATES IN 7 TURNS.",
        "log_decoy_act": "DECOY ACTIVE! GUARDS DISTRACTED!",
        "log_decoy_destroy": "DECOY DESTROYED!",
        "desc_EMP": "EMP: Electromagnetic pulse that stuns guards and dogs, and interferes with cameras and drones.",
        "desc_KIT": "KIT: Antidote kit against paralyzing and hallucinogenic toxins.",
        "desc_INV": "INV: Smoke bomb that prevents enemies from seeing you.",
        "desc_HACK": "HACK: Disposable device to hack drones and cameras.",
        "help_use": "[1-9] Use item",
        "help_info": "[Shift + 1-9] Item info",
        # --- ALLY TEXTS EN ---
        "log_ally_hit1": "Banging on the cell door... (1/2)",
        "log_ally_free": "Cell opened!",
        "log_ally_speak": "Help me escape! Guide me to the stairs where you came from.",
        "log_ally_secret": "The ally revealed a secret passage on your map!",
        "log_ally_escaped": "The ally escaped successfully and left an item!",
        "log_move_explore": "Unknown area! Explore first.",
        "log_move_init": "Automatic movement initiated.",
        "log_move_error": "Path blocked or inaccessible.",
        "log_move_cancel": "Visual contact! Movement canceled.",
        "hover_move": "MOVE",
        # estatísticas
        "stat_turns": "Total Turns: {}",
        "stat_time": "Time Played: {}",
        "stat_stunned": "Enemies Stunned: {}",
        "stat_items": "Items Collected: {}",
        "stat_allies": "Allies Freed: {}",
        "stat_msgs": "Messages Broadcasted: {}",
        "stat_caught_by": "Caught by: {}",
        "stat_convert": "Enemies converted: {}",
        "stat_hack": "Devices hacked: {}",
        "stat_edown": "Energy down: {}",
        "eng": "Engineer",
        "log_fixed": "The Engineer restored a device!",
        "npc_Guard": "Guard",
        "npc_Dog": "Dog",
        "npc_Drone": "Drone",
        "npc_Camera": "Camera",
        "npc_Unknown": "Unknown",
        "ui_visible": "In View:",
        "npc_Guard_plural": "Guards: {}",
        "npc_Dog_plural": "Dogs: {}",
        "npc_Drone_plural": "Drones: {}",
        "npc_Camera_plural": "Cameras: {}",
        "npc_Eng": "Enginner",
        "npc_Laser": "Lasers",
        "npc_Laser_plural": "Lasers",
        "npc_Ally": "Ally",
        "npc_Tiles_Up": "Stairs up",
        "npc_Tiles_Down": "Stairs down",
        "npc_Tiles_Terminal" : "Terminal",
        "npc_Tiles_Message": "Message",
        "npc_Tiles_Bible": "The Book",
        "npc_Tiles_Item": "Item",
        "npc_Tiles_Item_plural": "Itens: {}",
        "npc_Tiles_Down_plural": "Stairs down",
        "npc_Tiles_Traps": "Trap",
        "npc_Tiles_Traps_plural": "Traps: {}",
        "npc_Tiles_Panel": "Power panel",
        "npc_Tiles_Panel_plural": "Power panels: {}",
        "npc_Tiles_Shop": "Shop",
    },
    "PT": {
        "sub_title": "Um Jogo Roguelike Furtivo",
        "start_new": "(N / ESPAÇO) NOVO JOGO",
        "start_load": "(C / L) CARREGAR JOGO",
        "start_music": "(M) MÚSICA: {}",
        "start_lang": "(T) IDIOMA: PORTUGUÊS",
        "start_quit": "(Q) SAIR",
        "music_on": "LIGADA",
        "music_off": "DESLIGADA",
        "fail_title": "MISSÃO FRACASSADA",
        "fail_sub": "Nível {}. Pressione ESPAÇO para reiniciar.",
        "win_title": "MISSÃO CUMPRIDA!",
        "win_sub": "Você escapou com o Livro. Pressione ESPAÇO.",
        "hud_lvl": "NIVEL: {}/{}",
        "hud_stun": "PARALISADO: {}",
        "hud_drunk": "ENVENENADO: {}",
        "hud_inv": "INVISÍVEL: {}",
        "hud_hack_prog": "HACK PROGRESS:",
        "hud_hack_done": "MENSAGEM ENVIADA!",
        "hud_hack_do": "HACKEAR TERMINAL",
        "hud_alarm": "ALARME: {}",
        "hud_inv_title": "INVENTARIO ({}/{}):",
        "hud_full": "!! MOCHILA CHEIA !!",
        "hud_faith": "Fé: {}/100",
        "caught_map": "CAPTURADO!",
        "menu_title": "MENU",
        "opt_music": "(M) Ligar/Desligar Música",
        "opt_restart": "(R) Reiniciar Jogo",
        "opt_save": "(S) Salvar Jogo",
        "opt_load": "(L/C) Carregar Jogo",
        "opt_lang": "(T) Idioma: PT-BR",
        "opt_resume": "(ESC) Voltar ao Jogo",
        "opt_quit": "(Q) Sair",
        "save_title": "SALVAR JOGO EM QUAL SLOT?",
        "load_title": "CARREGAR QUAL SLOT?",
        "slot_occ": "[OCUPADO]",
        "slot_emp": "[VAZIO]",
        "slot_txt": "({}) - Slot {} {}",
        "slot_del": "(X + Número) APAGAR SLOT",
        "slot_back": "(ESC) Voltar",
        "log_shop_enter": "SISTEMA: LOJA ACESSADA. Pressione uma letra e depois um número do inventário para trocar.",
        "log_shop_inst": "SISTEMA: Trocas restantes: {}.",
        "log_shop_swap": "SISTEMA: Você trocou {} por {}!",
        "log_shop_closed": "SISTEMA: A loja fechou.",
        "log_shop_visited": "SISTEMA: A loja já está fechada.",
        "log_shop_sel": "SISTEMA: Selecionado {} ({}). Escolha seu item do inventário (1-9).",
        "log_intro1": "Desça até o nível 12 para encontrar o grande Livro e retorne com a verdade!",
        "log_intro2": "Em sua jornada, encontre a mensagem e transmita-a ao mundo!",
        "log_intro3": "Faça isso de maneira furtiva! O inimigo quer impedir que as boas notícias cheguem a todos!",
        "log_emp": "VOCÊ COLOCOU UM INIMIGO PARA DORMIR!",
        "log_kit": "ANTÍDOTO APLICADO, VOCÊ PODE SE MOVER NORMALMENTE!",
        "log_inv1": "SISTEMA: BOMBA DE FUMAÇA DETONADA!",
        "log_inv2": "VOCÊ ESTÁ INVISÍVEL!",
        "log_hack": "DISPOSITIVO HACKEADO!",
        "log_tun_in": "Entrando em um túnel secreto",
        "log_tun_out": "Saindo de um túnel secreto",
        "log_msg_req": "SISTEMA: ENCONTRE A MENSAGEM ♪ PRIMEIRO!",
        "log_alarm": "ALARME ATIVO!",
        "log_intruder": "ALERTA: INTRUSO DETECTADO NO SETOR!",
        "log_hack_ok": "SISTEMA: ACESSO CONCEDIDO. DADOS TRANSMITIDOS.",
        "log_msg_sent": "MENSAGEM ENVIADA!",
        "log_full": "CHEIO!",
        "log_book_get": "AGORA VOCÊ TEM O LIVRO! VOLTE PARA O NÍVEL 1!",
        "log_item": "ITEM ADQUIRIDO.",
        "log_spike1": "PARALISADO! DESPERTA Ó TU QUE DORMES!",
        "log_spike2": "SISTEMA: DADOS DE MAPEAMENTO CORROMPIDOS!",
        "log_drunk1": "ENVENENADO! O QUE QUERO FAZER NÃO FAÇO...",
        "log_last_lvl": "ESTE É O ÚLTIMO NÍVEL! PEGUE O LIVRO E VOLTE AO NÍVEL 1!",
        "log_need_book": "VOCÊ PRECISA PEGAR O LIVRO NO NÍVEL 12 ANTES DE FUGIR!",
        "log_return": "RETORNANDO AO NÍVEL {}",
        "log_dog": "CÃO DETECTOU CHEIRO!",
        "log_save_ok": "SISTEMA: JOGO SALVO COM SUCESSO NO SLOT {}.",
        "log_save_err": "ERRO AO SALVAR: {}",
        "log_load_ok": "SISTEMA: SLOT {} CARREGADO COM SUCESSO.",
        "log_load_emp": "SISTEMA: O SLOT {} ESTÁ VAZIO.",
        "log_load_err": "ERRO AO CARREGAR: {}",
        "log_del_ok": "SISTEMA: SLOT {} FOI APAGADO COM SUCESSO.",
        "log_del_emp": "SISTEMA: O SLOT {} JÁ ESTAVA VAZIO.",
        "log_del_err": "ERRO AO APAGAR: {}",
        "log_dark": "SISTEMA: ENERGIA RESTABELECIDA",
        "log_dark1": "SISTEMA: ENERGIA CORTADA! VISÃO REDUZIDA!",
        "log_dark2": "Batendo no quadro de energia...",
        "desc_EMP": "EMP: Pulso eletromagnético que atordoa guardas e cães e interfere em câmeras e drones.",
        "desc_KIT": "KIT: Kit de antídotos contra toxinas paralisantes e alucinógenas.",
        "desc_INV": "INV: Bomba de fumaça que impede que inimigos te vejam.",
        "desc_HACK": "HACK: Dispositivo descartável para hackear drones e câmeras.",
        "help_use": "[1-9] Usar item",
        "help_info": "[Shift + 1-9] Detalhes",
        # --- ALLY TEXTS PT ---
        "log_ally_hit1": "Batendo na porta da cela... (1/2)",
        "log_ally_free": "Cela aberta!",
        "log_ally_speak": "Me ajude a fugir! Me guie até a escada de onde você veio.",
        "log_ally_secret": "O aliado revelou uma passagem secreta no seu mapa!",
        "log_ally_escaped": "O aliado escapou com sucesso e deixou um item!",
        "log_pray": "Pregue e ore",
        "log_convert": "Convertei-vos agora cada um do seu mau caminho",
        "log_resist": "Coração endurecido",
        "log_faith": "Você está cheio de fé! Pressione ""P"" para pregar e orar. Talvez alguém se arrependa...",
        "desc_DECOY": "DECOY: Deixa uma isca que ativa em 7 turnos para atrair guardas.",
        "log_decoy_drop": "ISCA PLANTADA! ATIVANDO EM 7 TURNOS.",
        "log_decoy_act": "ISCA ATIVA! GUARDAS DISTRAÍDOS!",
        "log_decoy_destroy": "ISCA DESTRUÍDA!",
        "log_move_explore": "Área desconhecida! Explore primeiro.",
        "log_move_init": "Movimento automático iniciado.",
        "log_move_error": "Caminho bloqueado ou inacessível.",
        "log_move_cancel": "Contato visual! Movimento cancelado.",
        "hover_move": "MOVER",
        # estatísticas
        "stat_turns": "Turnos Totais: {}",
        "stat_time": "Tempo de Jogo: {}",
        "stat_stunned": "Inimigos Atordoados: {}",
        "stat_items": "Itens Coletados: {}",
        "stat_allies": "Aliados Libertos: {}",
        "stat_msgs": "Mensagens Transmitidas: {}",
        "stat_caught_by": "Capturado por: {}",
        "stat_convert": "Inimigos convertidos: {}",
        "stat_hack": "Dispositivos hackeados: {}",
        "stat_edown": "Energia desligada: {}",
        "eng": "Engenheiro",
        "log_fixed": "O Engenheiro restaurou um dispositivo!",
        "npc_Guard": "Guarda",
        "npc_Dog": "Cão",
        "npc_Drone": "Drone",
        "npc_Camera": "Câmera",
        "npc_Eng": "Engenheiro",
        "npc_Unknown": "Desconhecido",
        "ui_visible": "Campo de visão:",
        "npc_Guard_plural": "Guardas: {}",
        "npc_Dog_plural": "Cães: {}",
        "npc_Drone_plural": "Drones: {}",
        "npc_Camera_plural": "Câmeras: {}",
        "npc_Laser": "Lasers",
        "npc_Laser_plural": "Lasers",
        "npc_Ally": "Aliado",
        "npc_Tiles_Up": "Escada para cima",
        "npc_Tiles_Down": "Escada para baixo",
        "npc_Tiles_Terminal" : "Terminal",
        "npc_Tiles_Message": "Mensagem",
        "npc_Tiles_Bible": "O Livro",
        "npc_Tiles_Item": "Item",
        "npc_Tiles_Item_plural": "Itens: {}",
        "npc_Tiles_Down_plural": "Escada para baixo",
        "npc_Tiles_Traps": "Armadilha",
        "npc_Tiles_Traps_plural": "Armadilhas: {}",
        "npc_Tiles_Panel": "Painel elétrico",
        "npc_Tiles_Panel_plural": "Paineis elétrico: {}",
        "npc_Tiles_Shop": "Loja",
        
    }
}

# --- Base de Dados de Mensagens ---
MENSAGENS_DB = {
    1: {
        "PT": {"texto": "Como está escrito: “Não há nenhum justo, nem um sequer...”", "ref": "Rm 3:10"},
        "EN": {"texto": "As it is written: “There is no one righteous, not even one...”", "ref": "Rom 3:10"}
    },
    2: {
        "PT": {"texto": "pois todos pecaram e estão destituídos da glória de Deus", "ref": "Rm 3: 23"},
        "EN": {"texto": "for all have sinned and fall short of the glory of God", "ref": "Rom 3:23"}
    },
    3: {
        "PT": {"texto": "Ninguém pode ver o Reino de Deus, se não nascer de novo", "ref": "Jo 3:3"},
        "EN": {"texto": "No one can see the kingdom of God unless they are born again.", "ref": "John 3:3"}
    },
    4: {
        "PT": {"texto": "Se você confessar que Jesus é Senhor e crer que Deus o ressuscitou, será salvo.", "ref": "Rm 10:9"},
        "EN": {"texto": "If you declare, “Jesus is Lord,” and believe that God raised him, you will be saved.", "ref": "Rom 10:9"}
    },
    5: {
        "PT": {"texto": "Tendo sido, pois, justificados pela fé, temos paz com Deus...", "ref": "Rm 5:1"},
        "EN": {"texto": "We have been justified through faith, we have peace with God...", "ref": "Rom 5:1"}
    },
    6: {
        "PT": {"texto": "Pois vocês são salvos pela graça, por meio da fé...", "ref": "Ef 2:8-9"},
        "EN": {"texto": "For it is by grace you have been saved, through faith...", "ref": "Eph 2:8-9"}
    },
    7: {
        "PT": {"texto": "Vejam como é grande o amor que o Pai nos concedeu: somos filhos de Deus!", "ref": "1 Jo 3:1"},
        "EN": {"texto": "See what great love the Father has lavished on us, that we are called children of God!", "ref": "1 John 3:1"}
    },
    8: {
        "PT": {"texto": "Portanto, sejam imitadores de Deus, como filhos amados...", "ref": "Ef 5:1-2"},
        "EN": {"texto": "Follow God’s example, and walk in the way of love...", "ref": "Eph 5:1-2"}
    },
    9: {
        "PT": {"texto": "Vocês, porém, são geração eleita, sacerdócio real, nação santa, povo de Deus...", "ref": "1 Pe 2:9"},
        "EN": {"texto": "But you are a chosen people, a royal priesthood, a holy nation, God’s possession...", "ref": "1 Pet 2:9"}
    },
    10: {
        "PT": {"texto": "Não se amoldem ao mundo, mas transformem-se pela renovação da sua mente...", "ref": "Rm 12:2"},
        "EN": {"texto": "Do not conform to this world, but be transformed by the renewing of your mind...", "ref": "Rom 12:2"}
    },
    11: {
        "PT": {"texto": "Mas em todas estas coisas somos mais que vencedores, por meio daquele que nos amou.", "ref": "Rm 8:37"},
        "EN": {"texto": "No, in all these things we are more than conquerors through him who loved us.", "ref": "Rom 8:37"}
    },
    12: {
        "PT": {"texto": "Portanto, vão e façam discípulos de todas as nações. E eu estarei sempre com vocês...", "ref": "Mt 28:19-20"},
        "EN": {"texto": "Therefore go and make disciples of all nations. And surely I am with you always...", "ref": "Matt 28:19-20"}
    }
}

# --- Configurações de Dificuldade ---
NPC_CONFIG = {
    "guard":  {"chance_base": 0.10, "escala_nivel": 0.03, "nivel_min": 1},
    "dog":    {"chance_base": 0.05, "escala_nivel": 0.02, "nivel_min": 3},
    "drone":  {"chance_base": 0.05, "escala_nivel": 0.02, "nivel_min": 5},
    "camera": {"chance_base": 0.15, "escala_nivel": 0.01, "nivel_min": 2}
}

# --- Gerador de Som ---
def play_beep(frequency, duration, volume=0.1):
    try:
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array.array('h', [0] * n_samples)
        for i in range(n_samples):
            t = float(i) / sample_rate
            buf[i] = int(volume * 32767 * math.sin(2 * math.pi * frequency * t))
        sound = pygame.mixer.Sound(buf)
        sound.play()
    except: pass

class Entity:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.stun_timer = 0
        self.vision_tiles = set()
        self.detected_player = False

class Tiles_Up(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        
class Tiles_Down(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        
class Tiles_Terminal(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

class Tiles_Message(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

class Tiles_Bible(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)


class Tiles_Item(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

class Tiles_Traps(Entity):
    def __init__(self,x,y):
        super().__init__(x,y)

class Tiles_Panel(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hits = 0

class Tiles_Shop(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

class Ally(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_free = False
        self.door_hits = 0
        self.escaped = False
        self.bars = [] # Lista das coordenadas que formam a prisão dele

class Decoy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.timer = 7
        self.active = False

class Eng(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dir_x, self.dir_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.suspicion = 0
        self.hacked = False 

    def update_vision(self, map_data, is_alarm, is_dark=False):
        self.vision_tiles = set()
        if self.stun_timer > 0: return
        
        v_range = 3 # Visão mais curta que a do guarda
        if is_dark: v_range = 1
        
        angle = {(0, 1): 90, (0, -1): 270, (1, 0): 0, (-1, 0): 180}.get((self.dir_x, self.dir_y), 0)
        fov = 40
        for i in range(0, fov, 3):
            rad = math.radians(angle - fov/2 + i)
            px, py = float(self.x) + 0.5, float(self.y) + 0.5
            for _ in range(v_range * 2):
                px += math.cos(rad)*0.5; py += math.sin(rad)*0.5
                tx, ty = int(px), int(py)
                
                if not (0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT) or map_data[ty][tx] in [TILE_WALL, TILE_SECRET_DOOR, TILE_SECRET_FLOOR]: break
                self.vision_tiles.add((tx, ty))

                if 0 < tx < MAP_WIDTH - 1 and 0 < ty < MAP_HEIGHT - 1:
                    walls = [TILE_WALL, TILE_SECRET_DOOR]
                    if (map_data[ty-1][tx] in walls and map_data[ty+1][tx] in walls) and self.y != ty: break 
                    if (map_data[ty][tx-1] in walls and map_data[ty][tx+1] in walls) and self.x != tx: break

    def move(self, map_data, player_x=None, player_y=None, chase=False, path=None, occupied_tiles=None):
        if self.stun_timer > 0: return None
        if occupied_tiles is None: occupied_tiles = []
        
        if path and len(path) > 0:
            nx, ny = path[0]
            # Engenheiro NÃO captura o jogador (não checa nx == player_x)
            if (nx, ny) not in occupied_tiles and (nx != player_x or ny != player_y):
                self.dir_x, self.dir_y = nx - self.x, ny - self.y
                self.x, self.y = nx, ny
        else:
            nx, ny = self.x + self.dir_x, self.y + self.dir_y
            if (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and 
                map_data[ny][nx] not in [TILE_WALL, 5, TILE_SECRET_DOOR, TILE_SECRET_FLOOR, TILE_BARS_1, TILE_BARS_2, TILE_PANEL, TILE_SHOP] and 
                (nx, ny) not in occupied_tiles and (nx != player_x or ny != player_y)):
                self.x, self.y = nx, ny
            else:
                self.dir_x, self.dir_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        return None

class Guard(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dir_x, self.dir_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.suspicion = 0
        self.hacked = False 

    def get_char(self):
        if self.stun_timer > 0: return 'z'
        return {(0, 1): 'v', (0, -1): '^', (1, 0): '>', (-1, 0): '<'}.get((self.dir_x, self.dir_y), 'G')

    def update_vision(self, map_data, is_alarm, is_dark=False):
        
        self.vision_tiles = set()
        if self.stun_timer > 0: return
        v_range = 6 + (2 if is_alarm else 0)
        
        # LÓGICA DE ESCURIDÃO:
        if is_dark:
            v_range = 1
        
        angle = {(0, 1): 90, (0, -1): 270, (1, 0): 0, (-1, 0): 180}[(self.dir_x, self.dir_y)]
        fov = 80 if is_alarm else 50
        for i in range(0, fov, 3):
            rad = math.radians(angle - fov/2 + i)
            px, py = float(self.x) + 0.5, float(self.y) + 0.5
            for _ in range(v_range * 2):
                px += math.cos(rad)*0.5; py += math.sin(rad)*0.5
                tx, ty = int(px), int(py)
                
                # Se bater numa parede ou limite, para o raio
                if not (0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT) or map_data[ty][tx] in [TILE_WALL, TILE_SECRET_DOOR, TILE_SECRET_FLOOR]: 
                    break
                
                # Adiciona o tile atual à visão
                self.vision_tiles.add((tx, ty))

                # --- LÓGICA CORRIGIDA: BLOQUEAR VISÃO DIAGONAL EM CORREDORES ---
                # Evita IndexErrors checando as bordas do mapa
                if 0 < tx < MAP_WIDTH - 1 and 0 < ty < MAP_HEIGHT - 1:
                    walls = [TILE_WALL, TILE_SECRET_DOOR]
                    
                    # Identifica se o tile atual é um trecho de corredor (paredes opostas)
                    is_horiz_corr = (map_data[ty-1][tx] in walls and map_data[ty+1][tx] in walls)
                    is_vert_corr = (map_data[ty][tx-1] in walls and map_data[ty][tx+1] in walls)
                    
                    # Se for um corredor e o guarda NÃO estiver na mesma linha/coluna, quebra o raio
                    if is_horiz_corr and self.y != ty:
                        break 
                    if is_vert_corr and self.x != tx:
                        break

    def move(self, map_data, player_x=None, player_y=None, chase=False, path=None, occupied_tiles=None):
        self.chase = chase
        if self.stun_timer > 0: return None
        if occupied_tiles is None: occupied_tiles = []
        
        if self.chase and path and len(path) > 0:
            nx, ny = path[0]
            if nx == player_x and ny == player_y and not self.hacked and not INVENSIVEL: return "CAUGHT" 
            if (nx, ny) not in occupied_tiles:
                self.dir_x, self.dir_y = nx - self.x, ny - self.y
                self.x, self.y = nx, ny
        else:
            nx, ny = self.x + self.dir_x, self.y + self.dir_y
            if nx == player_x and ny == player_y and not self.hacked and not INVENSIVEL: return "CAUGHT"
            if (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and 
                map_data[ny][nx] not in [TILE_WALL, 5, TILE_SECRET_DOOR, TILE_SECRET_FLOOR, TILE_BARS_1, TILE_BARS_2, TILE_PANEL, TILE_SHOP] and 
                (nx, ny) not in occupied_tiles):
                self.x, self.y = nx, ny
            else:
                self.dir_x, self.dir_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        return None

class Drone(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dir_x, self.dir_y = random.choice([-1, 1]), random.choice([-1, 1])
        self.suspicion = 0
        self.hacked = False
        
    def update_vision(self, map_data, is_alarm, is_dark=False):
        
        self.vision_tiles = set()
        if self.stun_timer > 0: return
        r = 4 if is_alarm else 3
        
        # NOVA LÓGICA:
        if is_dark:
            r = min(r, 1)
        for dy in range(-r, r+1):
            for dx in range(-r, r+1):
                if dx*dx + dy*dy <= r*r:
                    tx, ty = self.x + dx, self.y + dy
                    if not (0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT) or map_data[ty][tx] in [TILE_WALL, TILE_SECRET_DOOR, TILE_SECRET_FLOOR]: break
                    self.vision_tiles.add((tx, ty))
    
    def move(self, map_data, player_x=None, player_y=None, occupied_tiles=None):
        if occupied_tiles is None: occupied_tiles = []
        for _ in range(2):
            nx, ny = self.x + self.dir_x, self.y + self.dir_y
            if nx == player_x and ny == player_y and not self.hacked and not INVENSIVEL: return "CAUGHT"
            if (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and 
                map_data[ny][nx] not in [TILE_WALL, TILE_TERMINAL, TILE_SECRET_DOOR, TILE_SECRET_FLOOR, TILE_BARS_1, TILE_BARS_2, TILE_PANEL, TILE_SHOP] and
                (nx, ny) not in occupied_tiles): 
                self.x, self.y = nx, ny
            else: 
                self.dir_x, self.dir_y = random.choice([-1, 1]), random.choice([-1, 1])
        return None

class Camera(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.angle, self.focus_time, self.lucky_escape = 0, 0, False
        self.hacked = False
        self.c_range = 4
    
    def update(self, map_data, is_dark=False):
        
        self.vision_tiles, self.lucky_escape = set(), False
        if self.stun_timer > 0: self.stun_timer -= 1; self.focus_time = 0; return
        self.angle = (self.angle + 45) % 360
        
        v_range = 4
        if is_dark:
            v_range = 1

        for i in range(0, 45, 5):
            rad = math.radians(self.angle - 22.5 + i)
            px, py = float(self.x) + 0.5, float(self.y) + 0.5
            for _ in range(v_range):  # Troque o 4 fixo por v_range 
                px += math.cos(rad)*1.0; py += math.sin(rad)*1.0
                tx, ty = int(px), int(py)
                if not (0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT) or map_data[ty][tx] in [TILE_WALL, TILE_SECRET_DOOR, TILE_SECRET_FLOOR]: break
                self.vision_tiles.add((tx, ty))

class Dog(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dir_x, self.dir_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.is_alerting = False 
        self.lucky_escape = False
        self.smell_radius = 2 

    def update_vision(self, map_data, is_alarm,is_dark=False):
        self.vision_tiles = set()
        self.lucky_escape = False
        if self.stun_timer > 0: return
        v_range = 2 
        if (self.dir_x, self.dir_y) == (0, 0): self.dir_x, self.dir_y = (0, 1)
        angle = {(0, 1): 90, (0, -1): 270, (1, 0): 0, (-1, 0): 180}.get((self.dir_x, self.dir_y), 0)
        
        for i in range(-15, 16, 5):
            rad = math.radians(angle + i)
            px, py = float(self.x) + 0.5, float(self.y) + 0.5
            for _ in range(v_range * 2):
                px += math.cos(rad)*0.5; py += math.sin(rad)*0.5
                tx, ty = int(px), int(py)
                if not (0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT) or map_data[ty][tx] in [TILE_WALL, TILE_SECRET_DOOR, TILE_SECRET_FLOOR, TILE_PANEL]: break
                self.vision_tiles.add((tx, ty))
    
    def move(self, map_data, player_x, player_y, path=None, occupied_tiles=None):
        self.is_alerting = False 
        if self.stun_timer > 0: return None
        if occupied_tiles is None: occupied_tiles = []
        
        dist = math.hypot(self.x - player_x, self.y - player_y)
        moves = 2 if dist <= self.smell_radius else 1
        return_signal = None 

        if dist <= self.smell_radius and random.random() < 0.5:
            self.is_alerting = True
            return_signal = "ALERT" 
        
        for i in range(moves):
            nx, ny = self.x, self.y
            if dist <= self.smell_radius and path and len(path) > i:
                nx, ny = path[i]
            else:
                nx, ny = self.x + self.dir_x, self.y + self.dir_y

            if (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and 
                map_data[ny][nx] not in [TILE_WALL, 5, TILE_SECRET_DOOR, TILE_SECRET_FLOOR, TILE_BARS_1, TILE_BARS_2, TILE_PANEL, TILE_SHOP] and 
                (nx, ny) not in occupied_tiles and 
                (nx != player_x or ny != player_y)):
                
                self.dir_x, self.dir_y = nx - self.x, ny - self.y
                self.x, self.y = nx, ny
            else:
                if dist > self.smell_radius: 
                    self.dir_x, self.dir_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            
            dist = math.hypot(self.x - player_x, self.y - player_y)
        return return_signal

class Laser:
    def __init__(self, x, y, is_vertical_beam, offset):
        self.x, self.y, self.active, self.offset, self.is_vertical_beam = x, y, False, offset, is_vertical_beam
    def update(self, t): self.active = (t + self.offset) % 6 < 3

class Game:
    def __init__(self): 
        pygame.init()
        self.held_dirs = set()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION])
        self.tracks = {}        
        
        self.language = "EN"
        
        try:
            pygame.mixer.init()
            self.audio_enabled = True
            self.current_track = None
            self.music_enabled = True 
            pygame.mixer.music.set_volume(0.3)
        except pygame.error as e:
            print(f"Aviso: Dispositivo de áudio não encontrado ({e}). O jogo rodará sem som.")
            self.audio_enabled = False
        
        if self.audio_enabled:
            try:
                self.track1 = self.resource_path("tema_inicio2.mp3")
                self.tracks['inicio'] = pygame.mixer.Sound(self.track1)
                self.track2 = self.resource_path("tema_stealth.mp3")
                self.tracks['stealth'] = pygame.mixer.Sound(self.track2)
                self.track3 = self.resource_path("tema_alerta.mp3")
                self.tracks['alerta'] = pygame.mixer.Sound(self.track3)
                
                for t in self.tracks.values():
                    t.set_volume(1.0)
                self.tracks['alerta'].set_volume(0.2)
                
                
                self.active_sound = None
            except Exception as e:
                print(f"Erro ao carregar trilhas: {e}")
                self.audio_enabled = False
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.virtual_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        
        try:
            self.icon_path = self.resource_path("icon-at.png")
            self.custom_icon = pygame.image.load(self.icon_path)
        except Exception as e:
            pass
        
        pygame.display.set_caption("εv@ngεlion")
                
        self.last_mouse_move_time = pygame.time.get_ticks()
        
        self.auto_path = []           # Armazena a lista de coordenadas até o destino
        self.last_auto_move = 0       # Controla o tempo entre os passos automáticos
        
        self.message_log = []     
        self.log_scroll = 0       
        
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.fade_alpha = 255 
        self.fade_speed = 255 / (2 * 30) 
        
        self.caught_timer = 0
        self.caught_start_time = 0 
               
        self.font = pygame.font.SysFont('Consolas', FONT_SIZE, bold=True)
        self.small_font = pygame.font.SysFont('Consolas', 16, bold=True) 
        self.title_font = pygame.font.SysFont('Consolas', 50, bold=True)
        
        self.clock = pygame.time.Clock()
        self.state = "START"
        self.level, self.inventory = 1, ["EMP", "KIT", "DECOY"]
        self.has_the_book = False
        self.worlds = {}
        
        self.popup_timer = 0
        self.popup_text = ""
        
        self.player_faith = 0
        
        
        self.generate_level()
        self.move_cooldown = 0
        self.update_music()
        self.active_waves = [] 
        self.smoke_tile = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.smoke_tile.fill((200, 200, 210))
        
        self.game_start_time = pygame.time.get_ticks()

    def t(self, key, *args):
        text = TEXTS[self.language].get(key, key)
        if args:
            return text.format(*args)
        return text

    def save_current_level(self):
        self.worlds[self.level] = {
            "map_data": self.map_data,
            "explored": self.explored,
            "terminal_hacked": self.terminal_hacked,
            "message_found": self.message_found,
            "guards": self.guards,
            "dogs": self.dogs,
            "drones": self.drones,
            "cameras": self.cameras,
            "eng": self.engs,
            "lasers": self.lasers,
            "allies": self.allies,
            "stairs_up_x": self.stairs_up_x,
            "stairs_up_y": self.stairs_up_y,
            "exit_x": self.exit_x,
            "exit_y": self.exit_y,
            "panel_x": self.panel_x,
            "panel_y": self.panel_y,
            "tiles": self.tiles,
            "player_heat": self.player_heat,
            "dark": self.dark_turns,
            "n_guards": self.number_guards,
            "decoys": self.decoys,
            "shop_visited": self.shop_visited,
            "shop_trades_left": self.shop_trades_left
        }

    def load_level(self, level_num):
        data = self.worlds[level_num]
        self.map_data = data["map_data"]
        self.explored = data["explored"]
        self.terminal_hacked = data["terminal_hacked"]
        self.message_found = data["message_found"]
        self.guards = data["guards"]
        self.dogs = data["dogs"]
        self.drones = data["drones"]
        self.cameras = data["cameras"]
        self.engs = data["eng"]
        self.lasers = data["lasers"]
        self.allies = data.get("allies", [])
        self.stairs_up_x = data["stairs_up_x"]
        self.stairs_up_y = data["stairs_up_y"]
        self.exit_x = data["exit_x"]
        self.exit_y = data["exit_y"]
        self.panel_x = data["panel_x"]
        self.panel_y = data["panel_y"]
        self.tiles = data["tiles"]
        self.player_heat = data.get("player_heat", 0)
        self.dark_turns = data.get("dark", 0)
        self.number_guards = data.get("n_guards",0)
        self.generate_more_enemies()
        self.shop_visited = data.get("shop_visited")
        self.shop_trades_left = data.get("shop_trades_left",0)
    
    def find_path(self, start_x, start_y, goal_x, goal_y):
        open_list = [(0, start_x, start_y)]
        came_from = {}
        g_score = {(start_x, start_y): 0}
        
        # Tiles que o pathfinding vai desviar
        blocked_tiles = [TILE_WALL, TILE_SECRET_DOOR, TILE_STAIR_DOWN, TILE_STAIR_UP, TILE_SPIKES, TILE_SENSOR, TILE_DRUNK, TILE_LASER_V, TILE_LASER_H, TILE_TERMINAL, TILE_MESSAGE, TILE_BIBLE, TILE_BARS_1, TILE_BARS_2, TILE_CAMERA, TILE_PANEL,TILE_SHOP]
   
        
        while open_list:
            open_list.sort(key=lambda x: x[0]) # Fila de prioridade simples
            _, current_x, current_y = open_list.pop(0)
            
            if current_x == goal_x and current_y == goal_y:
                path = []
                while (current_x, current_y) in came_from:
                    path.append((current_x, current_y))
                    current_x, current_y = came_from[(current_x, current_y)]
                path.reverse()
                return path
                
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = current_x + dx, current_y + dy
                
                # Verifica os limites do mapa
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                    # Verifica se o vizinho avaliado é exatamente o alvo do clique
                    is_goal = (nx == goal_x and ny == goal_y)
                    
                    # Desvia de armadilhas e bloqueios (A NÃO SER que o bloqueio seja o destino!)
                    if self.map_data[ny][nx] in blocked_tiles and not is_goal: 
                        continue
                        
                    tentative_g_score = g_score.get((current_x, current_y), 0) + 1
                    
                    if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                        came_from[(nx, ny)] = (current_x, current_y)
                        g_score[(nx, ny)] = tentative_g_score
                        # Heurística: Distância de Manhattan
                        f_score = tentative_g_score + abs(nx - goal_x) + abs(ny - goal_y)
                        open_list.append((f_score, nx, ny))
                        
        return [] # Retorna vazio se não houver caminho possível
    
    def is_enemy_visible(self):
        for e in self.guards + self.drones + self.dogs + self.cameras + self.engs:
            # Se o inimigo está visível e não está atordoado
            if self.visible[e.y][e.x] and e.stun_timer <= 0:
                # Ignora máquinas aliadas (hackeadas)
                if hasattr(e, "hacked") and e.hacked:
                    continue
                return True
        return False
    
    
    def get_path_to_target(self, start_x, start_y, target_x, target_y):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        queue = [(start_x, start_y, [])]
        visited = set()
        visited.add((start_x, start_y))
        
        while queue:
            cx, cy, path = queue.pop(0)
            if cx == target_x and cy == target_y:
                return path
                
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                    # Inclui barras como obstáculos
                    if self.map_data[ny][nx] not in [TILE_WALL, 5, TILE_SECRET_DOOR, TILE_SECRET_FLOOR, TILE_BARS_1, TILE_BARS_2, TILE_SHOP] and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + [(nx, ny)]))
        return []
    
    def get_path_to_player(self, start_x, start_y):
        if self.player_invisible > 0 or self.alarm_timer <=0:
            return []
        return self.get_path_to_target(start_x, start_y, self.player_x, self.player_y)
    
    def get_path_to_panel(self, start_x, start_y):
        # Correção: A rota deve ser ignorada se a luz estiver ACESA (== 0) ou se houver alarme.
        if self.dark_turns == 0 or self.alarm_timer > 0:
            return []
        return self.get_path_to_target(start_x, start_y, self.panel_x, self.panel_y)
    
    def save_game(self, slot=1):
        self.save_current_level()
        filename = f"savegame_slot{slot}.json"
        
        serialized_worlds = {}
        for lvl_num, data in self.worlds.items():
            serialized_worlds[str(lvl_num)] = {
                "map_data": data["map_data"],
                "explored": data["explored"],
                "terminal_hacked": data["terminal_hacked"],
                "message_found": data["message_found"],
                "stairs_up_x": data["stairs_up_x"],
                "stairs_up_y": data["stairs_up_y"],
                "exit_x": data["exit_x"],
                "exit_y": data["exit_y"],
                "panel_x": data["panel_x"],
                "panel_y": data["panel_y"],
                "guards": [{"x": g.x, "y": g.y, "dx": g.dir_x, "dy": g.dir_y, "stun_timer": g.stun_timer} for g in data["guards"]],
                "eng": [{"x": e.x, "y": e.y, "dx": e.dir_x, "dy": e.dir_y, "stun_timer": e.stun_timer} for e in data["eng"]],
                "dogs": [{"x": d.x, "y": d.y, "dx": d.dir_x, "dy": d.dir_y, "stun_timer": d.stun_timer} for d in data["dogs"]],
                "drones": [{"x": dr.x, "y": dr.y, "dx": dr.dir_x, "dy": dr.dir_y, "stun_timer": dr.stun_timer, "hacked": dr.hacked} for dr in data["drones"]],
                "cameras": [{"x": c.x, "y": c.y, "angle": c.angle, "stun_timer": c.stun_timer, "hacked": c.hacked} for c in data["cameras"]],
                "lasers": [{"x": l.x, "y": l.y, "is_vertical_beam": l.is_vertical_beam, "offset": l.offset} for l in data.get("lasers", [])],
                "allies": [{"x": a.x, "y": a.y, "is_free": a.is_free, "door_hits": a.door_hits, "escaped": a.escaped, "bars": a.bars} for a in data.get("allies", [])],
                "decoys": [{"x": d.x, "y": d.y, "timer": d.timer, "active": d.active} for d in data.get("decoys", [])],
                "tiles": [{"x": t.x, "y": t.y, "name":t.__class__.__name__} for t in data.get("tiles", [])],
                "player_heat": data.get("player_heat", 0),
                "dark": data.get("dark", 0),
                "faith": data.get("faith", 0),
                "n_guards": data.get("n_guards",0),
                "shop_visited": data.get("shop_visited"),
                "shop_trades_left": data.get("shop_trades_left",0)
            }
            
        data_to_save = {
            "level": self.level,
            "inventory": self.inventory,
            "player_x": self.player_x,
            "player_y": self.player_y,
            "alarm_timer": self.alarm_timer,
            "has_the_book": self.has_the_book,
            "player_stun": self.player_stun,
            "player_drunk": self.player_drunk,
            "player_heat": self.player_heat,
            "player_invisible": self.player_invisible,
            "dark_turns": self.dark_turns,
            "faith": self.player_faith,
            "shop_visited": self.shop_visited,
            "shop_trades_left": self.shop_trades_left,
            "worlds": serialized_worlds,
            "total_turns": self.total_turns,
            "accumulated_time": self.accumulated_time + (pygame.time.get_ticks() - self.game_start_time if self.state == "PLAYING" else 0),
            "stats_npcs_stunned": self.stats_npcs_stunned,
            "stats_items_collected": self.stats_items_collected,
            "stats_allies_freed": self.stats_allies_freed,
            "stats_messages_sent": self.stats_messages_sent,
            "stat_convert": self.stats_guards_convert,
            "stat_edown": self.stats_energy_down,
            "stat_hack": self.stats_hack,
            "caught_by_name": self.caught_by_name
        }
        
        try:
            with open(filename, "w") as f:
                json.dump(data_to_save, f)
            self.add_log(self.t("log_save_ok", slot))
            self.set_state("PLAYING")
        except Exception as e:
            self.add_log(self.t("log_save_err", e))
    
    def load_game(self, slot=1):
        filename = f"savegame_slot{slot}.json"
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            self.level = data["level"]
            self.inventory = data["inventory"]
            self.player_x = data["player_x"]
            self.player_y = data["player_y"]
            self.alarm_timer = data["alarm_timer"]
            self.has_the_book = data.get("has_the_book", False)
            self.player_stun = data.get("player_stun", 0)
            self.player_drunk = data.get("player_drunk", 0)
            self.player_heat = data.get("player_heat",0)
            self.player_pray = data.get("pray",0)
            self.player_faith = data.get("faith",0)
            self.player_invisible = data.get("player_invisible", 0)
            self.dark_turns = data.get("dark_turns", 0)
            self.total_turns = data.get("total_turns", 0)
            self.accumulated_time = data.get("accumulated_time", 0)
            self.stats_npcs_stunned = data.get("stats_npcs_stunned", 0)
            self.stats_items_collected = data.get("stats_items_collected", 0)
            self.stats_allies_freed = data.get("stats_allies_freed", 0)
            self.stats_messages_sent = data.get("stats_messages_sent", 0)
            self.stats_guards_convert = data.get("stat_convert",0)
            self.stats_energy_down = data.get("stat_edown",0)
            self.stats_hack = data.get("stat_hack",0)
            self.caught_by_name = data.get("caught_by_name", "npc_Unknown")
            self.shop_visited = data.get("shop_visited", False)
            self.shop_trades_left = data.get("shop_trades_left",0)
            
            self.worlds = {}
            for lvl_str, lvl_data in data["worlds"].items():
                lvl_num = int(lvl_str)
                guards = []
                for g in lvl_data.get("guards", []):
                    new_g = Guard(g["x"], g["y"])
                    new_g.dir_x, new_g.dir_y = g["dx"], g["dy"]
                    new_g.stun_timer = g.get("stun_timer", 0)
                    guards.append(new_g)

                engs = []
                for e in lvl_data.get("eng", []):
                    new_e = Eng(e["x"], e["y"])
                    new_e.dir_x, new_e.dir_y = e["dx"], e["dy"]
                    new_e.stun_timer = e.get("stun_timer", 0)
                    engs.append(new_e)
                
                dogs = []
                for d in lvl_data.get("dogs", []):
                    new_d = Dog(d["x"], d["y"])
                    new_d.dir_x, new_d.dir_y = d["dx"], d["dy"]
                    new_d.stun_timer = d.get("stun_timer", 0)
                    dogs.append(new_d)
                    
                drones = []
                for dr in lvl_data.get("drones", []):
                    new_dr = Drone(dr["x"], dr["y"])
                    new_dr.dir_x, new_dr.dir_y = dr["dx"], dr["dy"]
                    new_dr.stun_timer = dr.get("stun_timer", 0)
                    new_dr.hacked = dr.get("hacked", False)
                    drones.append(new_dr)
                    
                cameras = []
                for c in lvl_data.get("cameras", []):
                    new_c = Camera(c["x"], c["y"])
                    new_c.angle = c["angle"]
                    new_c.stun_timer = c.get("stun_timer", 0)
                    new_c.hacked = c.get("hacked", False)
                    cameras.append(new_c)
                    
                lasers = []
                for l in lvl_data.get("lasers", []):
                    lasers.append(Laser(l["x"], l["y"], l["is_vertical_beam"], l["offset"]))
                    
                allies = []
                for a in lvl_data.get("allies", []):
                    new_a = Ally(a["x"], a["y"])
                    new_a.is_free = a.get("is_free", False)
                    new_a.door_hits = a.get("door_hits", 0)
                    new_a.escaped = a.get("escaped", False)
                    new_a.bars = [tuple(b) for b in a.get("bars", [])]
                    allies.append(new_a)

                decoys = []
                for dec in lvl_data.get("decoys", []):
                    new_dec = Decoy(dec["x"], dec["y"])
                    new_dec.timer = dec.get("timer", 0)
                    new_dec.active = dec.get("active", False)
                    decoys.append(new_dec)
                
                
                tiles=[]
                for t in lvl_data.get("tiles", []):
                    name = t.get("name","")
                    
                    if name == "Tiles_Bible":
                        new_t = Tiles_Bible(t["x"],t["y"])
                    elif name == "Tiles_Down":
                        new_t = Tiles_Down(t["x"],t["y"])
                    elif name == "Tiles_Up":
                        new_t = Tiles_Up(t["x"],t["y"])
                    elif name == "Tiles_Item":
                        new_t = Tiles_Item(t["x"],t["y"])
                    elif name == "Tiles_Message":
                        new_t = Tiles_Message(t["x"],t["y"])
                    elif name == "Tiles_Terminal":
                        new_t = Tiles_Terminal(t["x"],t["y"])
                    elif name == "Tiles_Traps":
                        new_t = Tiles_Traps(t["x"],t["y"])
                    elif name == "Tiles_Panel":
                        new_t = Tiles_Panel(t["x"],t["y"])
                    elif name == "Tiles_Shop":
                        new_t = Tiles_Shop(t["x"],t["y"])
                    tiles.append(new_t)
                
                self.worlds[lvl_num] = {
                    "map_data": lvl_data["map_data"],
                    "explored": lvl_data["explored"],
                    "terminal_hacked": lvl_data["terminal_hacked"],
                    "message_found": lvl_data["message_found"],
                    "stairs_up_x": lvl_data.get("stairs_up_x", 0),
                    "stairs_up_y": lvl_data.get("stairs_up_y", 0),
                    "exit_x": lvl_data.get("exit_x", 0),
                    "exit_y": lvl_data.get("exit_y", 0),
                    "panel_x": lvl_data.get("panel_x", 0),
                    "panel_y": lvl_data.get("panel_y",0),
                    "guards": guards,
                    "dogs": dogs,
                    "drones": drones,
                    "cameras": cameras,
                    "eng": engs,
                    "lasers": lasers,
                    "allies": allies,
                    "tiles": tiles,
                    "player_heat": lvl_data.get("player_heat", 0),
                    "dark": lvl_data.get("dark", 0),
                    "n_guards": lvl_data.get("n_guards",0),
                    "decoys": decoys,
                    
                }

            self.load_level(self.level)
            self.update_player_fov()
            
            self.add_log(self.t("log_load_ok", slot))
            self.set_state("PLAYING")
            
        except FileNotFoundError:
            self.add_log(self.t("log_load_emp", slot))
        except Exception as e:
            self.add_log(self.t("log_load_err", e))
    
    def delete_save(self, slot=1):
        filename = f"savegame_slot{slot}.json"
        if os.path.exists(filename):
            try:
                os.remove(filename)
                self.add_log(self.t("log_del_ok", slot))
            except Exception as e:
                self.add_log(self.t("log_del_err", e))
        else:
            self.add_log(self.t("log_del_emp", slot))
    
    def update_music(self):
        if not self.audio_enabled:
            return

        target_key = None
        if self.music_enabled:
            if self.state == "START":
                target_key = 'inicio'
            elif self.state in ("PLAYING", "MENU", "MENU_SAVE", "MENU_LOAD", "CAUGHT"):
                target_key = 'alerta' if self.alarm_timer > 0 else 'stealth'

        if target_key != self.current_track:
            if self.active_sound:
                self.active_sound.fadeout(1000)
            self.current_track = target_key
            if target_key in self.tracks:
                self.active_sound = self.tracks[target_key]
                self.active_sound.play(loops=-1, fade_ms=1000)
            else:
                self.active_sound = None    
   
    def resource_path(self, relative_path): 
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def add_log(self, text):
        self.message_log.append(text)
        self.log_scroll = 0 
        if len(self.message_log) > 100:
            self.message_log.pop(0)
    
    
    def get_formatted_time(self):
        total_ms = self.accumulated_time
        if self.state in ["PLAYING", "CAUGHT"]:
            total_ms += pygame.time.get_ticks() - self.game_start_time
        seconds = (total_ms // 1000) % 60
        minutes = (total_ms // 60000)
        return f"{minutes:02d}:{seconds:02d}"

    def reset_game_stats(self):
        self.level, self.inventory = 1, ["EMP", "KIT", "DECOY"]
        self.total_turns = 0
        self.accumulated_time = 0
        self.game_start_time = pygame.time.get_ticks()
        self.stats_npcs_stunned = 0
        self.stats_items_collected = 0
        self.stats_allies_freed = 0
        self.stats_messages_sent = 0
        self.stats_guards_convert = 0
        self.stats_hack = 0
        self.stats_energy_down = 0
        self.caught_by_name = "npc_Unknown"
        self.message_log = []
        self.log_scroll = 0
        self.worlds = {}
        self.has_the_book = False
        self.generate_level()
        self.add_log(self.t("log_intro1"))
        self.add_log(self.t("log_intro2"))
        self.add_log(self.t("log_intro3"))

    def set_state(self, new_state):
        # Pausa e resume o cronômetro do jogo
        if self.state == "PLAYING" and new_state in ("MENU", "CAUGHT", "WIN"):
            self.accumulated_time += pygame.time.get_ticks() - self.game_start_time
        elif self.state in ("MENU", "START") and new_state == "PLAYING":
            self.game_start_time = pygame.time.get_ticks()
            
        self.state = new_state
        if new_state != "CAUGHT":
            self.fade_alpha = 255 
        self.update_music()

    def trigger_caught(self, npc_type="npc_Unknown"):
        if not INVENSIVEL:
            self.caught_by_name = npc_type
            self.set_state("CAUGHT")
            self.caught_start_time = pygame.time.get_ticks()
            play_beep(100, 0.4)
            play_beep(80, 0.4)

        
    def add_secret_passages(self, max_passages=0):
       
        corridors = self.corridor_tiles.copy()
        random.shuffle(corridors)
        passages_created = 0

        for cx, cy in corridors:
            if passages_created >= max_passages: break
            if not (0 < cx < MAP_WIDTH-1 and 0 < cy < MAP_HEIGHT-1): continue

            is_horizontal = (self.map_data[cy-1][cx] == TILE_WALL and self.map_data[cy+1][cx] == TILE_WALL)
            is_vertical = (self.map_data[cy][cx-1] == TILE_WALL and self.map_data[cy][cx+1] == TILE_WALL)

            dirs = []
            if is_horizontal: dirs = [(0, -1), (0, 1)] 
            elif is_vertical: dirs = [(-1, 0), (1, 0)] 

            passage_built = False
            for dx, dy in dirs:
                if passage_built: break
                tx, ty = cx + dx, cy + dy
                tunnel = []
                valid = False

                while 0 < tx < MAP_WIDTH-1 and 0 < ty < MAP_HEIGHT-1:
                    if self.map_data[ty][tx] == TILE_WALL:
                        if dx == 0: 
                            if self.map_data[ty][tx-1] != TILE_WALL or self.map_data[ty][tx+1] != TILE_WALL:
                                valid = False
                                break 
                        else: 
                            if self.map_data[ty-1][tx] != TILE_WALL or self.map_data[ty+1][tx] != TILE_WALL:
                                valid = False
                                break 
                        tunnel.append((tx, ty))
                        
                    elif self.map_data[ty][tx] == TILE_FLOOR:
                        valid = True 
                        break
                    else:
                        valid = False
                        break 
                    
                    tx += dx
                    ty += dy

                if valid and 4 <= len(tunnel) <= 12:
                    for i, (px, py) in enumerate(tunnel):
                        if i == 0 or i == len(tunnel) - 1:
                            self.map_data[py][px] = TILE_SECRET_DOOR
                        else:
                            self.map_data[py][px] = TILE_SECRET_FLOOR
                    passages_created += 1
                    passage_built = True
    
    def generate_more_enemies(self):
        if self.has_the_book:
            n_guards = self.number_guards 
            for r in self.rooms:
                cx, cy = r.center()
                # Ignora as posições se estiverem ocupadas pelo aliado ou grades
                if self.map_data[cy][cx] in [TILE_BARS_1, TILE_BARS_2, TILE_PRISON]: continue

                if len(self.guards) < (1.5*n_guards): self.guards.append(Guard(cx, cy))
                
    
    def generate_level(self):
        self.map_data = [[TILE_WALL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.explored = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.visible = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.alarm_timer, self.turn_count, self.player_stun = 0, 0, 0
        self.player_heat = 0
        self.player_drunk = 0
        self.player_invisible = 0
        self.player_pray = 0
        self.terminal_hacked, self.hack_progress = False, 0
        self.message_found = False 
        self.guards, self.cameras, self.drones, self.lasers, self.dogs, self.allies, self.tiles, self.decoys, self.engs = [], [], [], [], [], [], [], [], []
        self.msg_timer, self.msg_text = 0, ""
        self.shop_visited = False
        self.shop_active = False
        self.shop_inventory = []
        self.shop_trades_left = 0
        self.pending_trade_index = -1
        self.dark_turns = 0
        self.panel_x, self.panel_y = -1, -1 # Salva a posição do painel para os NPCs
        
        rooms = []
        self.corridor_tiles = []
        for _ in range(15 + self.level * 2):
            w, h = random.randint(6, 11), random.randint(5, 8)
            x, y = random.randint(1, MAP_WIDTH-w-1), random.randint(1, MAP_HEIGHT-h-1)
            new_room = type('R', (), {'x1':x, 'y1':y, 'x2':x+w, 'y2':y+h, 'center': lambda s: ((s.x1+s.x2)//2, (s.y1+s.y2)//2)})()
            if not any(not (new_room.x2 < r.x1 or new_room.x1 > r.x2 or new_room.y2 < r.y1 or new_room.y1 > r.y2) for r in rooms):
                for rx in range(new_room.x1+1, new_room.x2):
                    for ry in range(new_room.y1+1, new_room.y2): self.map_data[ry][rx] = TILE_FLOOR
                if rooms:
                    px, py = rooms[-1].center(); cx, cy = new_room.center()
                    for tx in range(min(px, cx), max(px, cx)+1):
                        if self.map_data[py][tx] == TILE_WALL: self.map_data[py][tx] = TILE_FLOOR; self.corridor_tiles.append((tx, py))
                    for ty in range(min(py, cy), max(py, cy)+1):
                        if self.map_data[ty][cx] == TILE_WALL: self.map_data[ty][cx] = TILE_FLOOR; self.corridor_tiles.append((cx, ty))
                rooms.append(new_room)
        self.rooms = rooms
        
        self.player_x, self.player_y = rooms[0].center()
        self.stairs_up_x, self.stairs_up_y = rooms[0].center()
        self.map_data[self.stairs_up_y][self.stairs_up_x] = TILE_STAIR_UP
        self.tiles.append(Tiles_Up(self.stairs_up_x,self.stairs_up_y))
        self.exit_x, self.exit_y = rooms[-1].center()
        self.map_data[self.exit_y][self.exit_x] = TILE_STAIR_DOWN
        self.tiles.append(Tiles_Down(self.exit_x,self.exit_y))
        self.term_x, self.term_y = rooms[len(rooms)//2].center()
        self.map_data[self.term_y][self.term_x] = TILE_TERMINAL
        
        
        idx_terminal = len(rooms) // 2
        self.term_x, self.term_y = rooms[idx_terminal].center()
        self.map_data[self.term_y][self.term_x] = TILE_TERMINAL
        self.tiles.append(Tiles_Terminal(self.term_x,self.term_y))
        
        possible_rooms = [i for i in range(len(rooms)) if i != 0 and i != len(rooms)-1 and i != idx_terminal]
        idx_msg = -1
        if possible_rooms:
            idx_msg = random.choice(possible_rooms)
            mx, my = rooms[idx_msg].center()
            self.map_data[my][mx] = TILE_MESSAGE
            self.tiles.append(Tiles_Message(mx,my))
            
        idx_bible = -1    
        if self.level == FINAL_LEVEL:
            possible_room_bible = [i for i in range(len(rooms)) if i != 0 and i != len(rooms)-1 and i != idx_terminal and i!= idx_msg]
            if possible_room_bible:
                idx_bible = random.choice(possible_room_bible)
                bx, by = rooms[idx_bible].center()
                self.map_data[by][bx] = TILE_BIBLE
                self.tiles.append(Tiles_Bible(bx,by))    
        
        
        
        
        # --- NOVO: GERADOR DO ALIADO / PRISÃO ---
        used_rooms = {0, len(rooms)-1, idx_terminal, idx_msg, idx_bible}
        possible_ally_rooms = [i for i in range(len(rooms)) if i not in used_rooms]
        
        if self.level % 3 == 0 and possible_ally_rooms and random.random() < 0.5:
        #if self.level == 1 and possible_ally_rooms and random.random() < 1.0: #debug da prisão
            idx_ally = random.choice(possible_ally_rooms)
            ax, ay = rooms[idx_ally].center()
            ally = Ally(ax, ay)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        self.map_data[ay+dy][ax+dx] = TILE_PRISON
                        ally.bars.append((ax+dx, ay+dy))
                        
                    if self.map_data[ay+dy][ax+dx] == TILE_FLOOR:
                        bar_char = random.choice([TILE_BARS_1, TILE_BARS_2])
                        self.map_data[ay+dy][ax+dx] = bar_char
                        ally.bars.append((ax+dx, ay+dy))
            self.allies.append(ally)
        
        
        # --- Limites Dinâmicos de População ---
        # Garante que o número de inimigos móveis nunca ultrapasse um limite frustrante
        max_mobile_enemies = len(rooms) // 2  # Ex: 12 inimigos para 25 salas
        max_cameras = len(rooms) // 3
        
        for r in rooms[1:]:
            cx, cy = r.center()
            # Ignora as posições se estiverem ocupadas pelo aliado ou grades
            if self.map_data[cy][cx] in [TILE_BARS_1, TILE_BARS_2, TILE_PRISON]: continue
            
            # --- Spawn de Guardas ---
            conf = NPC_CONFIG["guard"]
            if self.level >= conf["nivel_min"] and len(self.guards) + len(self.dogs) + len(self.drones) < max_mobile_enemies:
                if random.random() < (conf["chance_base"] + self.level * conf["escala_nivel"]): 
                    self.guards.append(Guard(cx, cy))
            if len(self.guards) <= 1: self.guards.append(Guard(cx, cy))

            self.number_guards = len(self.guards)    
            
            # --- Spawn de Cães ---
            conf = NPC_CONFIG["dog"]
            if self.level >= conf["nivel_min"] and len(self.guards) + len(self.dogs) + len(self.drones) < max_mobile_enemies:
                if random.random() < (conf["chance_base"] + self.level * conf["escala_nivel"]): 
                    self.dogs.append(Dog(cx, cy))
            
            # --- Spawn de Drones ---
            conf = NPC_CONFIG["drone"]
            if self.level >= conf["nivel_min"] and len(self.guards) + len(self.dogs) + len(self.drones) < max_mobile_enemies:
                if random.random() < (conf["chance_base"] + self.level * conf["escala_nivel"]): 
                    self.drones.append(Drone(cx, cy))

            if self.level >= 6 and self.level % 2 == 0: #normal será level 6
                if len(self.engs) == 0:
                    for _ in range(50): # Tenta achar um lugar livre
                        rx, ry = random.randint(1, MAP_WIDTH-2), random.randint(1, MAP_HEIGHT-2)
                        if self.map_data[ry][rx] == TILE_FLOOR and (rx, ry) != (self.player_x, self.player_y):
                            self.engs.append(Eng(rx, ry))
                            break
            
            # --- Spawn de Câmeras ---
            conf = NPC_CONFIG["camera"]
            if self.level >= conf["nivel_min"] and len(self.cameras) < max_cameras:
                if random.random() < (conf["chance_base"] + self.level * conf["escala_nivel"]):
                    corners = [(r.x1+1, r.y1+1), (r.x2-1, r.y1+1), (r.x1+1, r.y2-1), (r.x2-1, r.y2-1)]
                    random.shuffle(corners)
                    for lx, ly in corners:
                        # Verifica se o próprio canto ou qualquer um dos 8 vizinhos ao redor é parte de um corredor
                        area_livre_de_corredor = True
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                if (lx + dx, ly + dy) in self.corridor_tiles:
                                    area_livre_de_corredor = False
                                    break
                            if not area_livre_de_corredor:
                                break
                        
                        if area_livre_de_corredor and self.map_data[ly][lx] not in [TILE_BARS_1, TILE_BARS_2]: 
                            self.cameras.append(Camera(lx, ly))
                            self.map_data[ly][lx] = TILE_CAMERA
                            break
            
            for _ in range(2):
                tx, ty = cx + random.randint(-2, 2), cy + random.randint(-2, 2)
                if 0 < tx < MAP_WIDTH and 0 < ty < MAP_HEIGHT and self.map_data[ty][tx] == TILE_FLOOR and (tx, ty) != (cx, cy):
                    if self.level >= 4 and random.random() > 0.5:
                        self.map_data[ty][tx] = TILE_DRUNK
                        self.tiles.append(Tiles_Traps(tx,ty))
                    else:
                        self.map_data[ty][tx] = TILE_SPIKES
                        self.tiles.append(Tiles_Traps(tx,ty))
            
            for _ in range(3):
                rx, ry = random.randint(r.x1+1, r.x2-1), random.randint(r.y1+1, r.y2-1)
                if self.map_data[ry][rx] == TILE_FLOOR and (rx, ry) != (cx, cy):
                    roll = random.random()
                    if roll < 0.15: self.map_data[ry][rx] = TILE_ITEM; self.tiles.append(Tiles_Item(rx,ry))
                    elif roll < 0.22 and self.level >= 5: self.map_data[ry][rx] = TILE_SENSOR
                    
        if self.level >= 3:
            for lx, ly in self.corridor_tiles:
                if random.random() < 0.05:
                    if self.map_data[ly][lx-1] == TILE_WALL and self.map_data[ly][lx+1] == TILE_WALL:
                        self.lasers.append(Laser(lx, ly, False, random.randint(0,5))); self.map_data[ly][lx] = TILE_LASER_H
                    elif self.map_data[ly-1][lx] == TILE_WALL and self.map_data[ly+1][lx] == TILE_WALL:
                        self.lasers.append(Laser(lx, ly, True, random.randint(0,5))); self.map_data[ly][lx] = TILE_LASER_V
        n_passages = random.randint(0,1)
        if len(self.allies) > 0:
            self.add_secret_passages(2)
        else:
             self.add_secret_passages(n_passages)

        if random.random() < 0.6:
            if rooms:
                panel_room = random.choice(rooms)
                valid_spots = []
                
                for y in range(panel_room.y1 + 1, panel_room.y2):
                    for x in range(panel_room.x1 + 1, panel_room.x2):
                        if self.map_data[y][x] == TILE_FLOOR:
                            # Checa os 4 vizinhos buscando parede
                            if any(self.map_data[ny][nx] == TILE_WALL for nx, ny in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]):
                                # Checa se está longe de corredores (zona de segurança 3x3)
                                longe_de_corredor = True
                                for dy in [-1, 0, 1]:
                                    for dx in [-1, 0, 1]:
                                        if (x+dx, y+dy) in self.corridor_tiles:
                                            longe_de_corredor = False
                                
                                if longe_de_corredor:
                                    valid_spots.append((x, y))
                
                if valid_spots:
                    px, py = random.choice(valid_spots)
                    self.map_data[py][px] = TILE_PANEL
                    self.tiles.append(Tiles_Panel(px, py))
                    self.panel_x, self.panel_y = px, py
        # --- Geração da Loja (Níveis 6 e 12 com 75% de chance) ---
        if self.level ==1: #in (6, 12) and random.random() < 0.75: #normal será 6 e 12
            # Pega uma sala aleatória que não seja a primeira
            self.shop_trades_left = 2 if self.level < 8 else 3
            if len(self.rooms) > 1:
                shop_room = random.choice(self.rooms[1:])
                valid_spots = []
                for y in range(shop_room.y1 + 1, shop_room.y2):
                    for x in range(shop_room.x1 + 1, shop_room.x2):
                        if self.map_data[y][x] == TILE_FLOOR:
                            valid_spots.append((x, y))
                if valid_spots:
                    px, py = random.choice(valid_spots)
                    self.map_data[py][px] = TILE_SHOP
        
        self.update_player_fov()

    def update_player_fov(self):
        self.visible = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        view_range = 1 if self.player_stun > 0 else 12
        if self.dark_turns > 0:
            view_range = min(view_range, 2)
        for i in range(1, 360, 2):
            rad = math.radians(i); px, py = float(self.player_x), float(self.player_y)
            for _ in range(view_range):
                px += math.cos(rad); py += math.sin(rad); ix, iy = int(round(px)), int(round(py))
                if 0 <= ix < MAP_WIDTH and 0 <= iy < MAP_HEIGHT:
                    self.visible[iy][ix] = True; self.explored[iy][ix] = True
                    if self.map_data[iy][ix] in [TILE_WALL, TILE_SECRET_DOOR]: break 
                    if self.map_data[iy][ix] == TILE_SECRET_FLOOR and self.map_data[int(self.player_y)][int(self.player_x)] != TILE_SECRET_FLOOR: break
                else: break

        for e in self.drones + self.cameras:
            if e.hacked and e.stun_timer == 0:
                for vx, vy in e.vision_tiles:
                    if 0 <= vx < MAP_WIDTH and 0 <= vy < MAP_HEIGHT:
                        self.visible[vy][vx] = True
                        self.explored[vy][vx] = True
    
    def get_room_at(self, x, y):
            for r in self.rooms:
                if r.x1 <= x <= r.x2 and r.y1 <= y <= r.y2:
                    return r
            return None       
        
    def use_item(self, idx):
        if idx < len(self.inventory):
            item = self.inventory.pop(idx)
            if item == "EMP":
                play_beep(300, 0.2)
                for e in self.guards + self.cameras + self.drones + self.dogs + getattr(self, 'engs', []):
                    if self.visible[e.y][e.x]:
                        if hasattr(e, "hacked") and e.hacked:
                            pass
                        else:
                            self.active_waves.append({"x": self.player_x, "y": self.player_y, "r": 0, "max_r": 8, "color": (0, 255, 255)})
                            e.stun_timer = 25
                            self.stats_npcs_stunned += 1
                            self.add_log(self.t("log_emp"))
            elif item == "KIT": 
                self.player_stun = 0; self.player_drunk = 0
                self.add_log(self.t("log_kit"))
                play_beep(300, 0.2)
            elif item == "INV": 
                self.player_invisible = 11
                self.add_log(self.t("log_inv1"))
                self.add_log(self.t("log_inv2"))
                play_beep(300, 0.2)
            elif item == "DECOY":
                self.decoys.append(Decoy(self.player_x, self.player_y))
                self.add_log(self.t("log_decoy_drop"))
                play_beep(400, 0.1)
                self.player_heat +=15
            
            elif item == "HACK":
                for e in self.drones + self.cameras:
                    if self.visible[e.y][e.x]:
                        self.add_log(self.t("log_hack"))
                        play_beep(300, 0.2)
                        e.hacked = True
                        e.suspicion = 0
                        self.stats_hack +=1
                        self.active_waves.append({"x": self.player_x, "y": self.player_y, "r": 0, "max_r": 5, "color": (0, 255, 100)})
            self.move_entities(0, 0)

    def convert(self):
        i=0
        for e in self.guards + getattr(self, 'engs', []):
                    if self.visible[e.y][e.x] and not e.hacked:
                        
                        self.player_faith = 0
                        chance = random.random()
                        c_limit = (0.35+(self.level/100))*math.exp(-1.8*i) #(0.6+(self.level/100))*math.exp(-1.8*i)
                        #print(str(chance)+"<="+str(c_limit)) #debug convert
                        i+=1
                        if chance <= c_limit:
                            self.add_log(self.t("log_convert"))
                            play_beep(300, 0.2)
                            e.hacked = True
                            e.suspicion = 0
                            self.stats_guards_convert += 1
                            self.active_waves.append({"x": self.player_x, "y": self.player_y, "r": 0, "max_r": 5, "color": (0, 255, 100)})
                        else:
                            self.add_log(self.t("log_resist"))
                            play_beep(150, 1)
                            play_beep(120, 1)
        self.move_entities(0, 0)


    def move_entities(self, dx, dy):
        old_faith = self.player_faith
        nx = self.player_x + dx
        ny = self.player_y + dy
        heat = int(1+30*(1+(self.player_heat/10)))
        
        # Fecha a loja se o jogador se mover para longe
        if getattr(self, 'shop_active', False) and (dx != 0 or dy != 0):
            nx, ny = self.player_x + dx, self.player_y + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and self.map_data[ny][nx] != TILE_SHOP:
                self.shop_active = False
                self.pending_trade_index = -1
                self.add_log(self.t("log_shop_closed"))
                play_beep(150, 0.2)
        
        if dx != 0 or dy != 0:
            if self.player_faith < 100 and self.turn_count % 12 == 0:
                self.player_faith +=1
            
            if self.map_data[ny][nx] == TILE_WALL or any(c.x == nx and c.y == ny for c in self.cameras):
                return  
            
            # --- NOVO: Bater nas grades da prisão ---
            if self.map_data[ny][nx] in [TILE_BARS_1, TILE_BARS_2]:
                for ally in self.allies:
                    if (nx, ny) in ally.bars:
                        ally.door_hits += 1
                        if ally.door_hits == 1:
                            self.add_log(self.t("log_ally_hit1"))
                            play_beep(200, 0.1)
                        else:
                            self.add_log(self.t("log_ally_free"))
                            self.add_log(self.t("log_ally_speak"))
                            play_beep(400, 0.2)
                            
                            # Transforma a cela inteira de volta em chão
                            for bx, by in ally.bars:
                                self.map_data[by][bx] = TILE_FLOOR
                            ally.bars = []
                            ally.is_free = True
                            self.stats_allies_freed += 1
                            
                            # REVELAÇÃO DA PASSAGEM SECRETA
                            for sy in range(MAP_HEIGHT):
                                for sx in range(MAP_WIDTH):
                                    if self.map_data[sy][sx] in [TILE_SECRET_DOOR, TILE_SECRET_FLOOR]:
                                        self.explored[sy][sx] = True
                                        self.active_waves.append({"x": sx, "y": sy, "r": 0, "max_r": 10, "color": COLOR_SECRET_FLOOR})
                            self.add_log(self.t("log_ally_secret"))
                dx, dy = 0, 0
                #return # Gasta o turno batendo na grade
                
            if self.map_data[self.player_y][self.player_x] == TILE_FLOOR and self.map_data[ny][nx] == TILE_SECRET_DOOR:
                self.add_log(self.t("log_tun_in"))
                play_beep(80, 0.1)
            if self.map_data[self.player_y][self.player_x] == TILE_SECRET_DOOR and self.map_data[ny][nx] == TILE_FLOOR:
                self.add_log(self.t("log_tun_out"))
                play_beep(80, 0.1)
        
        old_alarm = self.alarm_timer
        self.turn_count += 1
        self.total_turns += 1

        # Atualiza os Decoys no chão
        for d in getattr(self, 'decoys', []):
            if not d.active and d.timer > 0:
                d.timer -= 1
                if d.timer == 0:
                    d.active = True
                    self.add_log(self.t("log_decoy_act"))
                    self.active_waves.append({"x": d.x, "y": d.y, "r": 0, "max_r": 8, "color": (255, 255, 0)})
                    play_beep(800, 0.3)
        
        if self.msg_timer > 0: self.msg_timer -= 1
        for l in self.lasers: l.update(self.turn_count)
        
        if self.player_stun > 0:
            self.player_stun -= 1
        else:
            if self.player_drunk > 0:
                self.player_drunk -= 1
            if self.player_invisible > 0:
                self.player_invisible -= 1
            nx, ny = self.player_x + dx, self.player_y + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                tile = self.map_data[ny][nx]
                
                if tile == TILE_TERMINAL and not self.terminal_hacked:
                    if not self.message_found:
                        self.add_log(self.t("log_msg_req")); self.msg_timer = 15; play_beep(150, 0.3)
                    elif self.alarm_timer > 0:
                        self.add_log(self.t("log_alarm")); self.msg_timer = 10; play_beep(150, 0.3)
                        self.add_log(self.t("log_intruder"))
                    else:
                        self.hack_progress += 1
                        if self.hack_progress >= 5: 
                            self.terminal_hacked = True; self.alarm_timer = 60; play_beep(880, 0.4)
                            self.stats_messages_sent += 1
                            self.add_log(self.t("log_hack_ok"))
                            self.add_log(self.t("log_msg_sent"))
                            self.add_log(self.t("log_alarm"))
                            if self.player_faith <= 90:
                                self.player_faith +=10
                            elif self.player_faith > 90:
                                self.player_faith = 100
                        else: 
                            play_beep(440, 0.1)
                
                elif tile == TILE_SHOP:
                    if not self.shop_visited:
                        
                        self.shop_active = True
                        #self.shop_trades_left = 2 if self.level < 8 else 3
                        items_pool = ["EMP", "KIT", "INV", "HACK", "DECOY"]
                        self.shop_inventory = [random.choice(items_pool) for _ in range(5)]
                        self.pending_trade_index = -1
                        
                        self.add_log(self.t("log_shop_enter"))
                        shop_str = ", ".join([f"{chr(97+i)}) {item}" for i, item in enumerate(self.shop_inventory)])
                        self.add_log(shop_str)
                        self.add_log(self.t("log_shop_inst", self.shop_trades_left))
                        play_beep(600, 0.2)
                        
                    elif self.shop_active:
                        self.add_log(self.t("log_shop_inst", self.shop_trades_left))
                    else:
                        self.add_log(self.t("log_shop_visited"))
                        play_beep(150, 0.2)
                    
                    # O jogador apenas esbarra na loja, não sobe nela
                    if not self.shop_visited:
                        self.player_x, self.player_y = self.player_x, self.player_y
                    else:
                        self.player_x, self.player_y = self.player_x + dx, self.player_y +dy
                
                elif tile == TILE_PANEL:
                    panel = next((p for p in self.tiles if isinstance(p, Tiles_Panel) and p.x == nx and p.y == ny), None)
                    if panel:
                        panel.hits += 1
                        if panel.hits < 3:
                            self.add_log(self.t("log_dark2"))
                            play_beep(200, 0.1)
                        elif panel.hits == 3:
                            self.add_log(self.t("log_dark1"))
                            play_beep(100, 0.5)
                            self.dark_turns = 20
                            self.player_heat +=5
                            self.stats_energy_down +=1
                        else:
                            self.add_log(self.t("log_dark1"))
                    #return # Gasta o turno batendo no painel
                
                
                
                elif tile != TILE_WALL:
                    if tile == TILE_ITEM and len(self.inventory) >= MAX_INVENTORY:
                        self.add_log(self.t("log_full"))
                        self.msg_timer = 10
                        play_beep(200, 0.1)
                        self.player_x, self.player_y = nx, ny
                    else:
                        enemy = next((e for e in self.guards + self.drones + self.dogs + self.engs if e.x == nx and e.y == ny), None)
                        if enemy and enemy.stun_timer == 0:
                            if hasattr(enemy, "hacked") and enemy.hacked:
                                # Troca as posições para não haver bloqueio em corredores estreitos
                                enemy.x, enemy.y = self.player_x, self.player_y
                                self.player_x, self.player_y = nx, ny
                            else:    
                                can_stun = isinstance(enemy, (Dog, Eng)) or \
                                (dx != 0 and dx == getattr(enemy, 'dir_x', 0)) or \
                                (dy != 0 and dy == getattr(enemy, 'dir_y', 0))

                                if can_stun:
                                    enemy.stun_timer = 25; play_beep(150, 0.2); self.add_log(self.t("log_emp"))
                                    self.stats_npcs_stunned += 1
                                else: 
                                    self.trigger_caught(); return
                        else:
                            self.player_x, self.player_y = nx, ny


                            
                            if tile == TILE_MESSAGE:
                                self.message_found = True
                                if self.player_faith <= 90:
                                    self.player_faith +=10
                                elif self.player_faith > 90:
                                    self.player_faith = 100
                                self.map_data[ny][nx] = TILE_FLOOR
                                for i in self.tiles:
                                    if isinstance(i,Tiles_Message):
                                        if i.x == nx and i.y == ny:
                                            self.tiles.remove(i)

                                lang_db = MENSAGENS_DB[self.level][self.language]
                                txt = f"♪ {lang_db['ref']}: {lang_db['texto']}"
                                self.add_log(txt) 
                                play_beep(600, 0.1); play_beep(800, 0.2)

                            if tile == TILE_BIBLE and self.terminal_hacked:
                                self.has_the_book = True
                                if self.player_faith < 100:
                                    self.player_faith = 100
                                self.map_data[ny][nx] = TILE_FLOOR
                                for i in self.tiles:
                                    if isinstance(i,Tiles_Bible):
                                        if i.x == nx and i.y == ny:
                                            self.tiles.remove(i)
                                self.add_log(self.t("log_book_get"))
                                play_beep(600, 0.1); play_beep(800, 0.2)
                            elif tile == TILE_BIBLE and not self.terminal_hacked:
                                #self.player_x, self.player_y = self.player_x - dx, self.player_y - dy
                                self.add_log(self.t("log_msg_req")); self.msg_timer = 15; play_beep(150, 0.3)



                            if tile == TILE_ITEM:
                                self.inventory.append(random.choice(["EMP", "KIT", "INV","HACK","EMP","INV","HACK", "DECOY"]))
                                self.stats_items_collected += 1
                                self.map_data[ny][nx] = TILE_FLOOR
                                for i in self.tiles:
                                    if isinstance(i,Tiles_Item):
                                        if i.x == nx and i.y == ny:
                                            self.tiles.remove(i)
                                self.add_log(self.t("log_item"))
                                play_beep(600, 0.1)
                            elif any(l.x == nx and l.y == ny and l.active for l in self.lasers):
                                if self.alarm_timer <=0 and self.dark_turns == 0 and self.player_invisible <= 0:
                                    self.alarm_timer = max(self.alarm_timer, heat)
                                    self.player_heat +=1
                            elif tile == TILE_SPIKES:
                                self.player_stun = 5
                                self.map_data[ny][nx] = TILE_FLOOR
                                for i in self.tiles:
                                    if isinstance(i,Tiles_Traps):
                                        if i.x == nx and i.y == ny:
                                            self.tiles.remove(i)
                                play_beep(200, 0.3)
                                self.add_log(self.t("log_spike1"))
                                self.add_log(self.t("log_spike2"))
                                self.explored = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]                                
                            elif tile == TILE_DRUNK:
                                self.player_drunk = 7
                                self.map_data[ny][nx] = TILE_FLOOR
                                for i in self.tiles:
                                    if isinstance(i,Tiles_Traps):
                                        if i.x == nx and i.y == ny:
                                            self.tiles.remove(i)
                                play_beep(200, 0.3)
                                self.add_log(self.t("log_drunk1"))
                                self.add_log(self.t("log_spike2"))
                                self.explored = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
                            elif tile == TILE_SENSOR:
                                if self.alarm_timer <=0:
                                    self.alarm_timer = max(self.alarm_timer, heat)
                                    self.player_heat +=1
                            elif tile == TILE_STAIR_DOWN:
                                if self.alarm_timer > 0:
                                    self.add_log(self.t("log_alarm"))
                                    self.msg_timer = 10
                                    play_beep(150, 0.3)
                                    self.player_x, self.player_y = self.player_x - dx, self.player_y - dy
                                    self.update_music()                                 
                                elif self.terminal_hacked:
                                    if self.level == FINAL_LEVEL:
                                        self.add_log(self.t("log_last_lvl"))
                                        self.player_x, self.player_y = self.player_x - dx, self.player_y - dy
                                    else:
                                        self.save_current_level() 
                                        self.level += 1
                                        if self.level in self.worlds:
                                            self.load_level(self.level)
                                            self.player_x, self.player_y = self.stairs_up_x, self.stairs_up_y
                                            self.update_player_fov() 
                                        else:
                                            self.generate_level() 
                                        return
                            elif tile == TILE_STAIR_UP:
                                if self.alarm_timer > 0:
                                    self.add_log(self.t("log_alarm"))
                                    self.msg_timer = 10
                                    play_beep(150, 0.3)
                                    self.player_x, self.player_y = self.player_x - dx, self.player_y - dy
                                    self.update_music()
                                else:
                                    if self.level == 1:
                                        if self.has_the_book:
                                            self.set_state("WIN")
                                        else:
                                            self.add_log(self.t("log_need_book"))
                                            self.player_x, self.player_y = self.player_x - dx, self.player_y - dy
                                    else:
                                        self.save_current_level()
                                        self.level -= 1
                                        self.load_level(self.level)
                                        self.player_x, self.player_y = self.exit_x, self.exit_y 
                                        self.update_player_fov() 
                                        self.add_log(self.t("log_return", self.level))
                                        return                                        

        is_alarm = self.alarm_timer > 0
        old_alarm = self.alarm_timer
        
        
        
        entities = self.guards + self.dogs + self.drones + getattr(self, 'engs', [])
        
        for e in entities:
            # Checa se há um decoy ativo no mapa
            active_decoy = next((d for d in getattr(self, 'decoys', []) if d.active), None)
            if e.stun_timer > 0: 
                e.stun_timer -= 1
            elif is_alarm or self.dark_turns > 0 or self.turn_count % 2 == 0 or isinstance(e, Dog) or active_decoy:
                
                occupied = [(other.x, other.y) for other in entities if other != e]
                occupied.extend([(c.x, c.y) for c in self.cameras])
                occupied.append((self.player_x, self.player_y))
                
                if isinstance(e, Dog):
                    dist = math.hypot(e.x - self.player_x, e.y - self.player_y)
                    path = self.get_path_to_player(e.x, e.y) if dist <= e.smell_radius else None
                    status = e.move(self.map_data, self.player_x, self.player_y, path, occupied)
                    if status == "ALERT":
                        if self.alarm_timer <=0:
                            self.alarm_timer = max(self.alarm_timer, heat)
                            self.player_heat +=1
                            if old_alarm == 0: self.add_log(self.t("log_dog"))
                
                elif isinstance(e, Guard):
                    
                    self.chase = is_alarm

                    if active_decoy:
                        self.chase = True
                        path = self.get_path_to_target(e.x, e.y, active_decoy.x, active_decoy.y)
                        
                        # Se o guarda pisou no decoy ou está adjacente
                        if math.hypot(e.x - active_decoy.x, e.y - active_decoy.y) < 1.5:
                            self.decoys.remove(active_decoy)
                            self.add_log(self.t("log_decoy_destroy"))
                            play_beep(200, 0.2)
                    else:
                        path = self.get_path_to_player(e.x, e.y) if self.chase else None
                        if self.dark_turns > 0 and not is_alarm and e.stun_timer <= 0:
                            self.chase = True
                            path = self.get_path_to_panel(e.x, e.y)
                    
                    status = e.move(self.map_data, self.player_x, self.player_y, self.chase, path, occupied)
                    
                    if status == "CAUGHT":
                        self.trigger_caught()
                        self.trigger_caught(f"npc_{e.__class__.__name__}")
                        return
                
                elif isinstance(e, Eng):
                    # 1. Checa Decoy
                    active_decoy = next((d for d in getattr(self, 'decoys', []) if d.active), None)
                    target_path = None
                    
                    if active_decoy:
                        target_path = self.get_path_to_target(e.x, e.y, active_decoy.x, active_decoy.y)
                    
                    # 2. Alarme se ver o jogador (usando os tiles atualizados)
                    if (self.player_x, self.player_y) in e.vision_tiles and self.player_invisible <= 0 and not e.hacked:
                        if self.alarm_timer <= 0:
                            self.alarm_timer = max(self.alarm_timer, heat)
                            self.add_log(self.t("log_alarm"))
                            self.player_heat += 1

                    # 3. Lógica de Reparo (Câmeras e Drones)
                    for device in (self.cameras + self.drones):
                        if (device.x, device.y) in e.vision_tiles and getattr(device, 'hacked', False):
                            if random.random() < 0.08 and not e.hacked: # 8% de chance de restaurar
                                device.hacked = False
                                self.add_log(self.t("log_fixed"))
                                play_beep(500, 0.2)

                    # 4. Movimento de Patrulha (passa chase=False pois ele não persegue o jogador)
                    status = e.move(self.map_data, self.player_x, self.player_y, False, target_path, occupied)
                
                
                elif isinstance(e, Drone):
                    status = e.move(self.map_data, self.player_x, self.player_y, occupied)
                    if status == "CAUGHT":
                        self.trigger_caught()
                        self.trigger_caught(f"npc_{e.__class__.__name__}")
                        return

            e.update_vision(self.map_data, is_alarm, self.dark_turns > 0)
        
        # --- NOVO: Movimentação de Fuga do Aliado ---
        for a in self.allies:
            if a.is_free and not a.escaped:
                if a.x == self.stairs_up_x and a.y == self.stairs_up_y:
                    a.escaped = True
                    self.add_log(self.t("log_ally_escaped"))
                    if len(self.inventory) < MAX_INVENTORY:
                        self.inventory.append(random.choice(["EMP", "KIT", "INV", "HACK", "DECOY"]))
                        self.stats_items_collected += 1
                else:
                    dist = math.hypot(a.x - self.player_x, a.y - self.player_y)
                    if dist > 1.5:  # Não pisa exatamente em cima do jogador
                        path = self.get_path_to_target(a.x, a.y, self.player_x, self.player_y)
                        if path:
                            nx, ny = path[0]
                            occ = [(e.x, e.y) for e in self.guards + self.dogs + self.drones + self.cameras + self.engs]
                            occ.append((self.player_x, self.player_y))
                            if (nx, ny) not in occ:
                                a.x, a.y = nx, ny
                                
        for c in self.cameras: c.update(self.map_data,self.dark_turns > 0)

        visible_npcs = []
        for e in self.guards + self.drones:
            
            if self.visible[e.y][e.x] and e.stun_timer <= 0:
                visible_npcs.append(e)
            
        closest_npc = None
        min_dist = float('inf')

        for npc in visible_npcs:
            # Calcula a distância euclidiana (hipotenusa) entre o jogador e o NPC
            dist = math.hypot(self.player_x - npc.x, self.player_y - npc.y)
                
            if dist < min_dist:
                min_dist = dist
                closest_npc = npc
                    
        for e in self.guards + self.drones + self.cameras + self.dogs + self.engs:
            e.detected_player = False
                        
            if self.player_invisible > 0 and hasattr(e, "suspicion"):
                e.suspicion = 0
            if hasattr(e, "hacked") and e.hacked:
                pass
            else:
                if e.stun_timer == 0 and self.player_invisible <=0 and (self.player_x, self.player_y) in e.vision_tiles:
                    if isinstance(e, Camera):
                        e.focus_time += 1
                        if random.random() < (0.4 if e.focus_time == 1 else 0.75 if e.focus_time == 2 else 1.0): 
                            if self.alarm_timer <=0:
                                self.alarm_timer = max(self.alarm_timer, heat)
                                e.detected_player = True
                                self.player_heat +=1
                        else: e.lucky_escape = True 
                    elif isinstance(e, Dog):
                        pass 
                    else:
                        e.detected_player = True
                        if hasattr(e, 'suspicion'):
                            if not INVENSIVEL and e == closest_npc:
                                e.suspicion += 1
                            if e.suspicion == 4:
                                if self.alarm_timer <=0:
                                    self.alarm_timer = max(self.alarm_timer, heat)
                                    self.add_log(self.t("log_alarm"))
                                    self.player_heat +=1
                            if e.suspicion >= 8:
                                self.trigger_caught()
                                self.trigger_caught(f"npc_{e.__class__.__name__}"); return
                elif hasattr(e, 'suspicion') and e.suspicion > 0: e.suspicion -= 1

        if self.alarm_timer > 0: self.alarm_timer -= 1
        if old_alarm == 0 and self.alarm_timer > 0:
            play_beep(600, 0.15)
            play_beep(800, 0.15)
        # No final de move_entities
        if self.dark_turns > 0:
            self.dark_turns -= 1
            # Se houver um engenheiro ativo, a luz volta mais rápido
            if any(e.stun_timer <= 0 for e in getattr(self, 'engs', [])):
                self.dark_turns -= 1 
            if self.dark_turns <= 0:
                self.add_log(self.t("log_dark"))
            
            
            if self.dark_turns == 0:
                
                self.add_log(self.t("log_dark"))
                play_beep(300, 0.3)
                # Reseta o painel para poder ser hackeado de novo
                panel = next((p for p in self.tiles if isinstance(p, Tiles_Panel)), None)
                if panel:
                    panel.hits = 0
        
        if old_faith < 100 and self.player_faith >= 100:
            self.add_log(self.t("log_faith"))
            play_beep(600, 0.2)
            play_beep(800, 0.2)
        
        self.update_music()
        self.update_player_fov()
    
    def draw_text_on_map(self, text, x_tile, y_tile, color, offset_y=-1):
        text_surf = self.font.render(str(text), True, color)
        px = x_tile * TILE_WIDTH + (TILE_WIDTH // 2) - (text_surf.get_width() // 2)
        py = (y_tile + offset_y) * TILE_HEIGHT
        bg_rect = (px - 2, py - 2, text_surf.get_width() + 4, text_surf.get_height() + 4)
        pygame.draw.rect(self.virtual_surface, COLOR_TEXT_BG, bg_rect)
        self.virtual_surface.blit(text_surf, (px, py))

    def draw_log(self):
        pygame.draw.rect(self.virtual_surface, (20, 20, 30), (0, 850, SCREEN_WIDTH, 130))
        pygame.draw.rect(self.virtual_surface, (50, 50, 70), (0, 850, SCREEN_WIDTH, 2)) 

        visible_lines = 4
        line_height = 25
        start_y = 860

        if self.message_log:
            end_idx = len(self.message_log) - self.log_scroll
            start_idx = max(0, end_idx - visible_lines)
            display_slice = self.message_log[start_idx:end_idx]

            for i, msg in enumerate(display_slice):
                alpha = 255 if (i + start_idx) == len(self.message_log) - 1 else 180
                color = (alpha, alpha, alpha)
                
                if "♪" in msg: color = (200, 255, 200)
                if "ALERTA" in msg or "ALERT" in msg: color = (255, 100, 100)
                
                lbl = self.font.render(msg, True, color)
                self.virtual_surface.blit(lbl, (20, start_y + i * line_height))

        if self.log_scroll > 0:
            scroll_msg = self.font.render(f"▲ +{self.log_scroll}", True, (255, 255, 0))
            self.virtual_surface.blit(scroll_msg, (SCREEN_WIDTH - 150, 860))
 
    def draw(self):
        self.virtual_surface.fill(COLOR_BG)
        
        if self.state == "START":
            txt = self.title_font.render("εv@ngεlion", True, COLOR_PLAYER)
            self.virtual_surface.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, 300))
            sub = self.font.render(self.t("sub_title"), True, (255,255,255))
            self.virtual_surface.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 400))
            
            music_txt = self.t("music_on") if self.music_enabled else self.t("music_off")
            start_options = [
                self.t("start_new"),
                self.t("start_load"),
                self.t("start_music", music_txt),
                self.t("start_lang"),
                self.t("start_quit")
            ]
            
            for i, text in enumerate(start_options):
                color = (255, 255, 255)
                if i == 2 and not self.music_enabled: color = (100, 100, 100)
                txt_surf = self.font.render(text, True, color)
                self.virtual_surface.blit(txt_surf, (SCREEN_WIDTH//2 - txt_surf.get_width()//2, SCREEN_HEIGHT//2 + i * 50))
        
        
        elif self.state in ("GAMEOVER", "WIN"):
            title_text = self.t("fail_title") if self.state == "GAMEOVER" else self.t("win_title")
            color = (255, 50, 50) if self.state == "GAMEOVER" else COLOR_WIN
            txt = self.title_font.render(title_text, True, color)
            self.virtual_surface.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, 150))
            
            sub_text = self.t("fail_sub", self.level) if self.state == "GAMEOVER" else self.t("win_sub")
            sub = self.font.render(sub_text, True, (255,255,255))
            self.virtual_surface.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 220))
            
            stats_y = 300
            stats = [
                self.t("stat_turns", self.total_turns),
                self.t("stat_time", self.get_formatted_time()),
                self.t("stat_stunned", self.stats_npcs_stunned),
                self.t("stat_items", self.stats_items_collected),
                self.t("stat_allies", self.stats_allies_freed),
                self.t("stat_msgs", self.stats_messages_sent),
                self.t("stat_convert",self.stats_guards_convert),
                self.t("stat_hack", self.stats_hack),
                self.t("stat_edown", self.stats_energy_down),
            ]
            
            if self.state == "GAMEOVER":
                caught_str = self.t("stat_caught_by", self.t(self.caught_by_name))
                stats.insert(0, caught_str)
                
            for i, st in enumerate(stats):
                st_txt = self.font.render(st, True, (200, 200, 200))
                self.virtual_surface.blit(st_txt, (SCREEN_WIDTH//2 - st_txt.get_width()//2, stats_y + i * 35))
        
        
       
        
        elif self.state == "PLAYING" or self.state == "CAUGHT":
            is_alarm = self.alarm_timer > 0       
            
            occupied = {(e.x, e.y) for e in self.guards + self.cameras + self.drones + self.dogs + self.engs
                        if self.visible[e.y][e.x] or e.stun_timer > 0}
            occupied.add((self.player_x, self.player_y))
            
            v_map = {}
            
            for e in self.guards + self.cameras + self.drones + self.dogs + self.engs:
                if e.stun_timer == 0:
                    c = (255, 80, 80) if (is_alarm or e.detected_player) else (180, 180, 40)
                    for pos in e.vision_tiles: v_map[pos] = c
                    
            smell_surf = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
            smell_surf.fill((150, 0, 255, 60))

            
            
            
            for dog in getattr(self, 'dogs', []):
                if abs(dog.x - self.player_x) < 6 and abs(dog.y - self.player_y) < 6:
                    for dx in range(-dog.smell_radius, dog.smell_radius + 1):
                        for dy in range(-dog.smell_radius, dog.smell_radius + 1):
                            if abs(dx) + abs(dy) <= dog.smell_radius:
                                target_x = dog.x + dx
                                target_y = dog.y + dy
                                if 0 <= target_x < MAP_WIDTH and 0 <= target_y < MAP_HEIGHT:
                                    self.virtual_surface.blit(smell_surf, (target_x * TILE_WIDTH, target_y * TILE_HEIGHT))        
            
            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    if not self.explored[y][x]:
                        #fog_col = (60, 20, 20) if is_alarm else COLOR_FOG
                        if self.dark_turns > 0:
                            fog_col = (5,5,5)
                        elif is_alarm:
                            fog_col = (60, 20, 20)
                        else:
                            fog_col = COLOR_FOG
                        pygame.draw.rect(self.virtual_surface, fog_col, (x*TILE_WIDTH, y*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)); continue
                    
                    if (x, y) in occupied:
                        continue 
                    
                    
                    
                    char, color = self.map_data[y][x], COLOR_FLOOR

                    if self.dark_turns > 0:
                        if char == TILE_FLOOR: color = COLOR_DARK_FOG
                        elif char == TILE_WALL: color = COLOR_DARK_FOG
                        elif char in [TILE_SPIKES, TILE_SENSOR, TILE_DRUNK]: color = COLOR_DARK_FOG
                        elif char == TILE_SECRET_FLOOR: char = TILE_FLOOR; color = COLOR_DARK_FOG
                        elif char == TILE_SECRET_DOOR: char = TILE_WALL; color = COLOR_DARK_FOG
                    else:    
                    
                        if char == TILE_WALL: color = COLOR_WALL
                        elif char in [TILE_SPIKES, TILE_SENSOR, TILE_DRUNK]: color = COLOR_FLOOR
                        elif char == TILE_PANEL: color = COLOR_PANEL    
                        elif char == TILE_SECRET_FLOOR: char = TILE_FLOOR; color = COLOR_SECRET_FLOOR
                        elif char == TILE_SECRET_DOOR: char = TILE_WALL; color = COLOR_SECRET_DOOR
                        elif char == TILE_CAMERA: char = TILE_FLOOR; color = COLOR_FLOOR
                        elif char == TILE_PRISON: color = COLOR_FLOOR; char = TILE_FLOOR
                        elif char in [TILE_BARS_1, TILE_BARS_2]: color = COLOR_BARS # Pinta as barras de metálico
                        elif (x,y) in v_map: color = v_map[(x,y)]
                        elif char == TILE_TERMINAL:
                            if not self.terminal_hacked:
                                color = COLOR_TERMINAL
                            else:
                                color = COLOR_STAIRS_LOCKED
                        elif char == TILE_ITEM: color = COLOR_ITEM
                        elif char == TILE_SHOP: 
                            color = COLOR_SHOP if not getattr(self, 'shop_visited', False) else (100, 100, 100)
                        elif char == TILE_MESSAGE: color = COLOR_MSG_NOTE
                        elif char == TILE_BIBLE:
                            if self.terminal_hacked:
                                color = COLOR_PLAYER
                            else:
                                color = COLOR_STAIRS_LOCKED
                        elif char == TILE_STAIR_UP: color = COLOR_STAIR_UP
                        elif char == TILE_STAIR_DOWN: 
                            color = COLOR_STAIRS_LOCKED
                            if self.terminal_hacked: color = COLOR_STAIRS_READY if not is_alarm else (255, 100, 0)
                        elif char in [TILE_LASER_V, TILE_LASER_H]:
                            act = any(l.x == x and l.y == y and l.active for l in self.lasers)
                            color = COLOR_LASER_ON if act else COLOR_LASER_OFF
                    
                    
                    
                    if is_alarm: color = (min(255, color[0] + 60), color[1] // 2, color[2] // 2)
                    if not self.visible[y][x]: color = [c // 2 for c in color]
                    
                    
                    
                    tempo = pygame.time.get_ticks() * 0.005
                
                    if self.map_data[y][x] == TILE_SECRET_DOOR and self.visible[y][x]:
                        variacao = math.sin(tempo + (x * 0.5) + (y * 0.5)) * 30
                        color_base = 100 + variacao
                        color = (color_base, color_base, color_base)
                    
                    self.virtual_surface.blit(self.font.render(char, True, color), (x*TILE_WIDTH, y*TILE_HEIGHT))
            
            for wave in self.active_waves[:]:
                cx = wave["x"] * TILE_WIDTH + TILE_WIDTH // 2
                cy = wave["y"] * TILE_HEIGHT + TILE_HEIGHT // 2
                pix_r = int(wave["r"] * TILE_WIDTH)
                pygame.draw.circle(self.virtual_surface, wave["color"], (cx, cy), pix_r, 2)
                wave["r"] += 0.5 
                if wave["r"] > wave["max_r"]:
                    self.active_waves.remove(wave)
            
            # Desenha os Decoys
            for d in getattr(self, 'decoys', []):
                if self.visible[d.y][d.x]:
                    if d.active:
                        # Pisca entre amarelo e laranja
                        color = (255, 255, 0) if pygame.time.get_ticks() % 500 < 250 else (255, 100, 0)
                        self.virtual_surface.blit(self.font.render(TILE_DECOY, True, color), (d.x*TILE_WIDTH, d.y*TILE_HEIGHT))
                    else:
                        # Decoy inativo (cinza) com contagem regressiva
                        self.virtual_surface.blit(self.font.render(TILE_DECOY, True, (100, 100, 100)), (d.x*TILE_WIDTH, d.y*TILE_HEIGHT))
                        self.draw_text_on_map(str(d.timer), d.x, d.y, (200, 200, 200), offset_y=-1)
            
            
            
            # --- NOVO: DESENHA O ALIADO ---
            for a in self.allies:
                if not a.escaped and self.visible[a.y][a.x]:
                    self.virtual_surface.blit(self.font.render('a', True, COLOR_PLAYER), (a.x*TILE_WIDTH, a.y*TILE_HEIGHT))
            
            for e in self.guards + self.cameras + self.drones + self.dogs + self.engs:
                should_draw = self.visible[e.y][e.x] or e.stun_timer > 0
                if isinstance(e, Dog) and e.is_alerting: should_draw = True
                
                if should_draw:
                    char, color = '?', (220, 220, 220)
                    if isinstance(e, Guard):
                        char = e.get_char()
                        color = COLOR_PLAYER if e.hacked else COLOR_GUARD
                    elif isinstance(e, Drone):
                        char = "d"
                        color = COLOR_PLAYER if e.hacked else COLOR_DRONE
                    elif isinstance(e, Camera):
                        char = "C"
                        color = COLOR_PLAYER if e.hacked else COLOR_CAMERA
                    elif isinstance(e, Dog): char, color = 'c', COLOR_DOG
                    elif isinstance(e, Eng):
                        char = 'e'
                        color = COLOR_PLAYER if e.hacked else COLOR_ENG
                    
                    if e.stun_timer > 0: char, color = 'z', COLOR_STUNNED;
                    
                    self.virtual_surface.blit(self.font.render(char, True, color), (e.x*TILE_WIDTH, e.y*TILE_HEIGHT))
                    
                    if e.stun_timer == 0:
                        if e.detected_player: 
                            self.draw_text_on_map("!", e.x, e.y, (255, 50, 50))
                        elif isinstance(e, Dog) and e.is_alerting:
                            self.draw_text_on_map("!", e.x, e.y, (255, 100, 0), offset_y=-1.5)
                        
                        if isinstance(e, (Guard, Drone, Eng)) and e.suspicion >= 1: self.draw_text_on_map(f"!{8-e.suspicion}", e.x, e.y, (255, 50, 50))
                        elif isinstance(e, Camera) and e.lucky_escape: self.draw_text_on_map("?", e.x, e.y, (200, 100, 255)) 
                        elif isinstance(e, Dog) and e.lucky_escape: self.draw_text_on_map("?", e.x, e.y, COLOR_DOG) 
                        elif e.detected_player: self.draw_text_on_map("!", e.x, e.y, (255, 50, 50))
            
            if self.player_stun > 0: p_c = (255, 50, 50)
            elif self.player_drunk >0: p_c = (200, 200, 0)
            elif self.player_invisible > 0: p_c = (150, 150, 150)
            else: p_c = COLOR_PLAYER
            
            self.virtual_surface.blit(self.font.render("@", True, p_c), (self.player_x*TILE_WIDTH, self.player_y*TILE_HEIGHT))
            
            if self.player_stun > 0: self.draw_text_on_map(str(self.player_stun), self.player_x, self.player_y, (255, 50, 50))
            if self.player_drunk > 0: self.draw_text_on_map(str(self.player_drunk), self.player_x, self.player_y, (200, 200, 0))
            if self.player_invisible > 0: self.draw_text_on_map(str(self.player_invisible), self.player_x, self.player_y, (150, 150, 150))
            if self.msg_timer > 0: self.draw_text_on_map(self.msg_text, self.player_x, self.player_y, (255, 255, 0), offset_y=-2)
            
            if self.player_invisible > 0:
                tempo = pygame.time.get_ticks() * 0.005 
                for y in range(MAP_HEIGHT):
                    for x in range(MAP_WIDTH):
                        if self.map_data[y][x] == TILE_FLOOR and self.visible[y][x]:
                            variacao = math.sin(tempo + (x * 0.5) + (y * 0.5)) * 30
                            alpha_base = 100 + variacao
                            self.smoke_tile.set_alpha(int(alpha_base))
                            self.virtual_surface.blit(self.smoke_tile, (x * TILE_WIDTH, y * TILE_HEIGHT))
            
            now = pygame.time.get_ticks()
            mouse_idle_time = now - self.last_mouse_move_time
            
            if mouse_idle_time > 2000:
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)
                # --- INÍCIO: EFEITO DE HOVER DO MOUSE ---
                if self.state == "PLAYING":
                    mx, my = pygame.mouse.get_pos()
                    scale_x = SCREEN_WIDTH / self.current_window_size[0]
                    scale_y = SCREEN_HEIGHT / self.current_window_size[1]
                    
                    hover_x = int(mx * scale_x) // TILE_WIDTH
                    hover_y = int(my * scale_y) // TILE_HEIGHT
                    
                    if 0 <= hover_x < MAP_WIDTH and 0 <= hover_y < MAP_HEIGHT:
                        # Só mostra se a área foi explorada e não for o tile do jogador
                        if self.explored[hover_y][hover_x] and (hover_x != self.player_x or hover_y != self.player_y):
                            
                            # 1. Cria a superfície amarela semi-transparente
                            hover_surf = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
                            hover_surf.fill((255, 255, 0, 70)) # 70 é a transparência (Alpha de 0 a 255)
                            self.virtual_surface.blit(hover_surf, (hover_x * TILE_WIDTH, hover_y * TILE_HEIGHT))
                            
                            # 2. Prepara o texto "MOVER"
                            text_str = self.t("hover_move")
                            text_surf = self.small_font.render(text_str, True, (255, 255, 255))
                            
                            # Calcula a posição para o texto ficar centralizado e acima do tile
                            px = hover_x * TILE_WIDTH + (TILE_WIDTH // 2) - (text_surf.get_width() // 2)
                            py = hover_y * TILE_HEIGHT - 20 
                            
                            # 3. Desenha um fundo preto pequeno para garantir a leitura do texto
                            bg_rect = (px - 2, py - 2, text_surf.get_width() + 4, text_surf.get_height() + 4)
                            pygame.draw.rect(self.virtual_surface, COLOR_TEXT_BG, bg_rect)
                            self.virtual_surface.blit(text_surf, (px, py))
                # --- FIM: EFEITO DE HOVER DO MOUSE ---
            
            
            sx = MAP_WIDTH * TILE_WIDTH + 20
            pygame.draw.rect(self.virtual_surface, (30,30,40), (sx-10, 0, 300, SCREEN_HEIGHT))
            self.virtual_surface.blit(self.font.render(self.t("hud_lvl", self.level, FINAL_LEVEL), True, (255,255,255)), (sx, 20))
            
            hud_y = 80 
            
            if self.player_stun > 0: 
                self.virtual_surface.blit(self.font.render(self.t("hud_stun", self.player_stun), True, (255, 50, 50)), (sx, hud_y))
                hud_y += 30 
                
            if self.player_drunk > 0: 
                self.virtual_surface.blit(self.font.render(self.t("hud_drunk", self.player_drunk), True, (200, 200, 0)), (sx, hud_y))
                hud_y += 30
                
            if self.player_invisible > 0: 
                self.virtual_surface.blit(self.font.render(self.t("hud_inv", self.player_invisible), True, (255, 255, 255)), (sx, hud_y))
                hud_y += 30
                
            if hud_y > 80: hud_y += 10
            else: hud_y = 90
            if self.player_faith >= 100:
                variacao = math.sin(tempo + (x * 0.5) + (y * 0.5)) * 30
                color_base = 100 + variacao
                color = (color_base, color_base, color_base)
            else: color = (150,150,150)
            self.virtual_surface.blit(self.font.render(self.t("hud_faith", self.player_faith), True, color), (sx, 50))
            
            self.virtual_surface.blit(self.font.render(self.t("hud_hack_prog"), True, (150,150,150)), (sx, hud_y))
            pygame.draw.rect(self.virtual_surface, (50, 50, 50), (sx, hud_y + 30, 200, 15))
            
            if not self.terminal_hacked:
                fill_w = (self.hack_progress / 5) * 200
                pygame.draw.rect(self.virtual_surface, COLOR_TERMINAL, (sx, hud_y + 30, fill_w, 15))
            else: 
                pygame.draw.rect(self.virtual_surface, COLOR_STAIRS_READY, (sx, hud_y + 30, 200, 15))
                
            msg = self.t("hud_hack_done") if self.terminal_hacked else self.t("hud_hack_do")
            self.virtual_surface.blit(self.font.render(msg, True, (255,100,100) if is_alarm else (100,255,150)), (sx, hud_y + 60))
            
            y_curr = hud_y + 100
            
            
            
            
            if is_alarm: self.virtual_surface.blit(self.font.render(self.t("hud_alarm", self.alarm_timer), True, (255,50,50)), (sx, y_curr)); y_curr += 40
            self.virtual_surface.blit(self.font.render(self.t("hud_inv_title", len(self.inventory), MAX_INVENTORY), True, (150,150,150)), (sx, y_curr))
            y_curr += 30
            
            for i, item in enumerate(self.inventory):
                self.virtual_surface.blit(self.font.render(f"{i+1}. {item}", True, (0,255,255)), (sx, y_curr)); y_curr += 30
            if len(self.inventory) >= MAX_INVENTORY: 
                self.virtual_surface.blit(self.font.render(self.t("hud_full"), True, (255, 255, 0)), (sx, y_curr))
                y_curr += 30
            
            y_curr += 10
            self.virtual_surface.blit(self.small_font.render(self.t("help_use"), True, (120,120,120)), (sx, y_curr))
            y_curr += 20
            self.virtual_surface.blit(self.small_font.render(self.t("help_info"), True, (120,120,120)), (sx, y_curr))
            
            
            # --- HUD DA LOJA ---
            if getattr(self, 'shop_active', False):
                y_curr += 20
                self.virtual_surface.blit(self.font.render("--- LOJA ---", True, COLOR_SHOP), (sx, y_curr))
                y_curr += 25
                self.virtual_surface.blit(self.small_font.render(f"Trocas: {self.shop_trades_left}", True, (200, 200, 200)), (sx, y_curr))
                y_curr += 20
                for i, s_item in enumerate(self.shop_inventory):
                    # Destaca a letra de amarelo se foi selecionada
                    c_color = (255, 255, 0) if getattr(self, 'pending_trade_index', -1) == i else (150, 150, 150)
                    self.virtual_surface.blit(self.small_font.render(f"{chr(97+i)}) {s_item}", True, c_color), (sx, y_curr))
                    y_curr += 20
            
            # --- INÍCIO: ENTIDADES NA VISÃO ---
            y_curr += 40 # Dá um espaço após os textos de ajuda
            
            visible_entities = {}
            # Junta todas as listas de ameaças para verificar
            for e in self.guards + self.dogs + self.drones + self.cameras + self.lasers + self.allies + self.tiles + self.engs:
                if self.visible[e.y][e.x]:
                    name = e.__class__.__name__
                    visible_entities[name] = visible_entities.get(name, 0) + 1
                    
            if visible_entities:
                self.virtual_surface.blit(self.font.render(self.t("ui_visible"), True, (255, 200, 0)), (sx, y_curr))
                y_curr += 30
                for name, count in visible_entities.items():
                    if count == 1:
                        text_str = self.t(f"npc_{name}")
                    else:
                        text_str = self.t(f"npc_{name}_plural", count)
                    
                    self.virtual_surface.blit(self.font.render(f"- {text_str}", True, (200, 200, 200)), (sx, y_curr))
                    y_curr += 25
            # --- FIM: ENTIDADES NA VISÃO ---
            
            if self.popup_timer > 0:
                self.popup_timer -= 1
                pop_w = 260
                pop_x = sx - 10
                pop_y = hud_y + 120 
                
                words = self.popup_text.split(' ')
                lines = []
                curr_line = ""
                for w in words:
                    if self.small_font.size(curr_line + w)[0] < pop_w - 20:
                        curr_line += w + " "
                    else:
                        lines.append(curr_line)
                        curr_line = w + " "
                lines.append(curr_line)
                
                pop_h = len(lines) * 20 + 20
                pygame.draw.rect(self.virtual_surface, (20, 20, 40), (pop_x, pop_y, pop_w, pop_h))
                pygame.draw.rect(self.virtual_surface, (0, 255, 255), (pop_x, pop_y, pop_w, pop_h), 2)
                
                for i, line in enumerate(lines):
                    self.virtual_surface.blit(self.small_font.render(line, True, (255, 255, 255)), (pop_x + 10, pop_y + 10 + i * 20))
            
            self.draw_log()  

            if self.state == "CAUGHT":
                self.draw_text_on_map(self.t("caught_map"), self.player_x, self.player_y, (255, 50, 50), offset_y=-2)
                
        elif self.state in ("MENU", "MENU_SAVE", "MENU_LOAD"):
            map_px_width = SCREEN_WIDTH
            map_px_height = SCREEN_HEIGHT - 130
            
            overlay = pygame.Surface((map_px_width, map_px_height))
            overlay.set_alpha(200) 
            overlay.fill((0, 0, 0))
            self.virtual_surface.blit(overlay, (0, 0))

            center_x = map_px_width // 2

            if self.state == "MENU":
                title = self.title_font.render(self.t("menu_title"), True, COLOR_PLAYER)
                self.virtual_surface.blit(title, (center_x - title.get_width()//2, 200))
                
                menu_options = [
                    self.t("opt_music"),
                    self.t("opt_restart"),
                    self.t("opt_save"),
                    self.t("opt_load"),
                    self.t("opt_lang"),
                    self.t("opt_resume"),
                    self.t("opt_quit")
                ]
                
                for i, option in enumerate(menu_options):
                    color = (255, 255, 255)
                    if "Música" in option or "Music" in option:
                        if not self.music_enabled: color = (100, 100, 100)
                    txt = self.font.render(option, True, color)
                    self.virtual_surface.blit(txt, (center_x - txt.get_width()//2, 350 + i * 50))

            elif self.state in ("MENU_SAVE", "MENU_LOAD"):
                title_text = self.t("save_title") if self.state == "MENU_SAVE" else self.t("load_title")
                title = self.title_font.render(title_text, True, COLOR_PLAYER)
                self.virtual_surface.blit(title, (center_x - title.get_width()//2, 200))

                for slot in range(1, 4):
                    status_key = "slot_occ" if os.path.exists(f"savegame_slot{slot}.json") else "slot_emp"
                    status = self.t(status_key)
                    color = (200, 200, 200) if status_key == "slot_emp" else COLOR_ITEM
                    
                    texto_slot = self.t("slot_txt", slot, slot, status)
                    txt = self.font.render(texto_slot, True, color)
                    self.virtual_surface.blit(txt, (center_x - txt.get_width()//2, 350 + (slot-1) * 60))

                delete_hint = self.font.render(self.t("slot_del"), True, (255, 100, 100))
                self.virtual_surface.blit(delete_hint, (center_x - delete_hint.get_width()//2, 500))
                
                txt_voltar = self.font.render(self.t("slot_back"), True, (150, 150, 150))
                self.virtual_surface.blit(txt_voltar, (center_x - txt_voltar.get_width()//2, 550))
            
            self.draw_log()
            
        if self.fade_alpha > 0:
            self.fade_surface.set_alpha(int(self.fade_alpha))
            self.virtual_surface.blit(self.fade_surface, (0, 0))
            self.fade_alpha -= self.fade_speed
            if self.fade_alpha < 0:
                self.fade_alpha = 0
        
        window_size = self.screen.get_size()
        scaled_surface = pygame.transform.scale(self.virtual_surface, window_size)
        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def run(self):
        dir_keys = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN}

        while True:
            for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,pygame.MOUSEMOTION, pygame.VIDEORESIZE]):
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.VIDEORESIZE:
                    self.current_window_size = event.size 
                    continue
                
                if event.type == pygame.KEYUP:
                    if event.key in dir_keys:
                        self.held_dirs.discard(event.key)
                    continue

                
                # --- INSIRA AQUI: Tratamento do mouse ANTES de filtrar o teclado ---
                if event.type == pygame.MOUSEMOTION:
                    # Atualiza o cronômetro sempre que o mouse se mover
                    self.last_mouse_move_time = pygame.time.get_ticks()
                    
                    # Se o cursor do sistema estava invisível, volta a mostrá-lo
                    pygame.mouse.set_visible(True)
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "PLAYING":
                        mx, my = event.pos
                        
                        # Calcula a proporção da tela real vs a superfície virtual do jogo
                        scale_x = SCREEN_WIDTH / self.current_window_size[0]
                        scale_y = SCREEN_HEIGHT / self.current_window_size[1]
                        
                        # Ajusta a coordenada do clique aplicando a escala
                        target_x = int(mx * scale_x) // TILE_WIDTH
                        target_y = int(my * scale_y) // TILE_HEIGHT
                        
                        if 0 <= target_x < MAP_WIDTH and 0 <= target_y < MAP_HEIGHT:
                            if target_x == self.player_x and target_y == self.player_y:
                                continue # Ignora clique em cima do próprio herói
                                
                            # Permite o auto-move apenas para áreas que o herói já viu
                            if not self.explored[target_y][target_x]:
                                self.add_log(self.t("log_move_explore"))
                                continue

                            self.auto_path = self.find_path(self.player_x, self.player_y, target_x, target_y)
                            if self.auto_path:
                                self.add_log(self.t("log_move_init")) 
                            else:
                                self.add_log(self.t("log_move_error"))
                    continue # Volta para o topo do loop de eventos
                # -------------------------------------------------------------------
                
                if event.type != pygame.KEYDOWN:
                    continue

                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self.set_state("MENU")
                    elif self.state == "MENU":
                        self.set_state("PLAYING")
                    elif self.state in ("MENU_SAVE", "MENU_LOAD"):
                        if getattr(self, "origin_state", "MENU") == "START":
                            self.set_state("START")
                            self.origin_state = "MENU" 
                        else:
                            self.set_state("MENU")
                    continue
                                
                if self.state == "START":
                    if event.key in (pygame.K_SPACE, pygame.K_n): 
                        self.level, self.inventory = 1, ["EMP", "KIT", "DECOY"]
                        self.generate_level()
                        self.reset_game_stats()
                        self.set_state("PLAYING")
                        self.message_log = []
                        self.log_scroll = 0
                        self.reset_game_stats() # Inicializa as estatísticas ao carregar o jogo
                    elif event.key in (pygame.K_c, pygame.K_l): 
                        self.origin_state = "START" 
                        self.state = "MENU_LOAD"
                    elif event.key == pygame.K_m: 
                        self.music_enabled = not self.music_enabled
                        self.update_music() 
                    elif event.key == pygame.K_t: 
                        self.language = "PT" if self.language == "EN" else "EN"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    continue 

                if self.state in ("GAMEOVER", "WIN"):
                    if event.key == pygame.K_SPACE:
                        self.level, self.inventory = 1, ["EMP", "KIT", "DECOY"]
                        self.generate_level()
                        self.reset_game_stats()
                        self.set_state("START")
                        self.message_log = []
                        self.log_scroll = 0
                        self.worlds = {}
                        self.has_the_book = False
                        self.player_faith = 0
                    continue
                
                if self.state in ("MENU", "MENU_SAVE", "MENU_LOAD"):
                    if self.state == "MENU":                        
                        if event.key == pygame.K_m:
                            self.music_enabled = not self.music_enabled
                            self.update_music()
                        elif event.key == pygame.K_t: 
                            self.language = "PT" if self.language == "EN" else "EN"
                        elif event.key == pygame.K_r:
                            self.level, self.inventory = 1, ["EMP", "KIT", "DECOY"]
                            self.generate_level()
                            self.reset_game_stats()
                            self.message_log = []
                            self.log_scroll = 0
                            self.worlds = {}
                            self.has_the_book = False
                            self.player_faith = 0
                            self.add_log(self.t("log_intro1"))
                            self.add_log(self.t("log_intro2"))
                            self.add_log(self.t("log_intro3"))
                            self.set_state("PLAYING")
                        elif event.key == pygame.K_s:
                            self.state = "MENU_SAVE" 
                        elif event.key in (pygame.K_l, pygame.K_c):
                            self.state = "MENU_LOAD" 
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

                    elif self.state == "MENU_SAVE":
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_x]:
                            if event.key == pygame.K_1: self.delete_save(1)
                            elif event.key == pygame.K_2: self.delete_save(2)
                            elif event.key == pygame.K_3: self.delete_save(3)
                        else:
                            if event.key == pygame.K_1: self.save_game(1)
                            elif event.key == pygame.K_2: self.save_game(2)
                            elif event.key == pygame.K_3: self.save_game(3)

                    elif self.state == "MENU_LOAD":
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_x]:
                            if event.key == pygame.K_1: self.delete_save(1)
                            elif event.key == pygame.K_2: self.delete_save(2)
                            elif event.key == pygame.K_3: self.delete_save(3)
                        else:
                            if event.key == pygame.K_1: self.load_game(1)
                            elif event.key == pygame.K_2: self.load_game(2)
                            elif event.key == pygame.K_3: self.load_game(3)
                       
                    continue 
                
                if self.state == "PLAYING":
                    
                    #if event.key == pygame.K_f:
                        #self.player_faith = 100
                    # --- CONTROLE DA LOJA ---
                    if pygame.K_a <= event.key <= pygame.K_e and getattr(self, 'shop_active', False):
                        idx = event.key - pygame.K_a
                        self.pending_trade_index = idx
                        self.add_log(self.t("log_shop_sel", chr(97+idx), self.shop_inventory[idx]))
                        continue

                    # --- CONTROLE DE ITENS (E TROCA NA LOJA) ---
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        keys = pygame.key.get_pressed()
                        
                        # Se estiver fazendo uma troca na loja
                        if getattr(self, 'shop_active', False) and getattr(self, 'pending_trade_index', -1) != -1:
                            if idx < len(self.inventory):
                                p_item = self.inventory[idx]
                                s_item = self.shop_inventory[self.pending_trade_index]
                                
                                # Efetua a troca
                                self.inventory[idx] = s_item
                                self.shop_inventory[self.pending_trade_index] = p_item
                                self.shop_trades_left -= 1
                                self.pending_trade_index = -1
                                
                                self.add_log(self.t("log_shop_swap", p_item, s_item))
                                play_beep(800, 0.1)
                            
                                if self.shop_trades_left <= 0:
                                    self.shop_visited = True
                                    self.shop_active = False
                                    self.add_log(self.t("log_shop_closed"))
                                else:
                                    # Mostra a loja atualizada
                                    shop_str = ", ".join([f"{chr(97+i)}) {item}" for i, item in enumerate(self.shop_inventory)])
                                    self.add_log(shop_str)
                            continue
                        
                        # Lógica original para USAR o item
                        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                            if idx < len(self.inventory):
                                item_name = self.inventory[idx]
                                self.popup_text = self.t(f"desc_{item_name}")
                                self.popup_timer = 90 
                        else:
                            self.use_item(idx)
                            self.popup_timer = 0 
                        continue

                    if event.key == pygame.K_SPACE:
                        self.move_entities(0, 0)
                        continue
                    
                    if event.key == pygame.K_PAGEUP:
                        max_scroll = max(0, len(self.message_log) - 4)
                        self.log_scroll = min(self.log_scroll + 1, max_scroll)
                        continue 
                    elif event.key == pygame.K_PAGEDOWN:
                        self.log_scroll = max(0, self.log_scroll - 1)
                        continue 
                    if event.key == pygame.K_p:
                        self.add_log(self.t("log_pray"))
                        if self.player_faith >= 100:
                            self.convert()
                        self.move_entities(0, 0)
                        continue
                    
                    
                    if event.key in dir_keys:
                        self.auto_path = [] # Cancela o auto-move se o jogador assumir o controle
                        if event.key in self.held_dirs:
                            continue
                        self.held_dirs.add(event.key)

                        dx = dy = 0
                        
                        if self.player_drunk > 0:
                            if random.random() < 0.7: m=-1
                            else: m=1
                        else:
                            m=1    
                            
                        if event.key == pygame.K_LEFT: dx = -1*m
                        elif event.key == pygame.K_RIGHT: dx = 1*m
                        elif event.key == pygame.K_UP: dy = -1*m
                        elif event.key == pygame.K_DOWN: dy = 1*m

                        self.move_entities(dx, dy)
            
            if self.state == "CAUGHT":
                now = pygame.time.get_ticks()
                if now - self.caught_start_time > 2000:
                    self.set_state("GAMEOVER") 
            
            if self.state == "PLAYING" and self.auto_path:
                now = pygame.time.get_ticks()
                # Espera 100 milissegundos entre cada passo
                if now - self.last_auto_move > 100: 
                    if self.is_enemy_visible():
                        self.auto_path = []
                        self.add_log(self.t("log_move_cancel"))
                        play_beep(200, 0.1) # Um bipe para avisar que parou
                    else:
                        next_x, next_y = self.auto_path.pop(0)
                        
                        dx = next_x - self.player_x
                        dy = next_y - self.player_y
                        
                        self.move_entities(dx, dy)
                        self.last_auto_move = now
            
            self.draw()
            self.clock.tick(30)
                
if __name__ == "__main__": Game().run()
