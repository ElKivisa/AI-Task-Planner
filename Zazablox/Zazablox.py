import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

console = Console()

# -------------------------------
# Configuración de archivo y colores
# -------------------------------

SCRIPT_DIR = Path(__file__).parent  # carpeta donde está el script
ITEMS_FILE = SCRIPT_DIR / "items.json"

RARITIES = ["Comun", "Raro", "Epico", "Legendario"]

RAREZA_COLOR = {
    "Comun": "green",
    "Raro": "blue",
    "Epico": "magenta",
    "Legendario": "yellow"
}

stats_list = [
    "HP",
    "VidaMax",
    "Daño%",
    "Velocidad%",
    "Defensa%",
    "Evasion%",
    "Critico%",
    "Curacion%",
    "XP%",
    "Oro%",
    "Suerte%",
    "VelocidadAtaque%"
]

players = {}

# -------------------------------
# Funciones de guardar/cargar
# -------------------------------

def guardar_items():
    with open(ITEMS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4, ensure_ascii=False)

def cargar_items():
    global items
    if ITEMS_FILE.exists() and ITEMS_FILE.stat().st_size > 0:
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
    else:
        # Objetos iniciales
        items = {
            "Fabada": {"rareza": "Comun", "stats": {"VidaMax": 25}},
            "Botiquin": {"rareza": "Comun", "stats": {"HP": 45}},
            "Guantes de Boxeo": {"rareza": "Comun", "stats": {"Daño%": 8}},
            "Calcetines Turbo": {"rareza": "Comun", "stats": {"Velocidad%": 15}},
            "Anillo Ligero": {"rareza": "Comun", "stats": {"Evasion%": 10}},
            "Testosterona": {"rareza": "Raro", "stats": {"Daño%": 10}},
            "Zapatillas Deslizantes": {"rareza": "Raro", "stats": {"Evasion%": 15}},
            "Trebol": {"rareza": "Raro", "stats": {"Suerte%": 7.5}},
            "Richard Mille": {"rareza": "Raro", "stats": {"XP%": 8}},
            "Bateria": {"rareza": "Raro", "stats": {"VelocidadAtaque%": 8}},
            "Casco Reforzado": {"rareza": "Raro", "stats": {"Defensa%": 15}},
            "Batido Proteico": {"rareza": "Epico", "stats": {"Daño%": 15}},
            "Pulsera del Tiempo": {"rareza": "Epico", "stats": {"XP%": 12}},
            "Guante Dorado": {"rareza": "Epico", "stats": {"Oro%": 15}},
            "Moneda Antigua": {"rareza": "Epico", "stats": {"Oro%": 20}},
            "Plato Combinado": {"rareza": "Epico", "stats": {"VidaMax": 40}},
            "Armadura Pesada": {"rareza": "Epico", "stats": {"Defensa%": 25}},
            "Trebol de Cuatro Hojas": {"rareza": "Legendario", "stats": {"Suerte%": 12}},
            "Motor Ilegal": {"rareza": "Legendario", "stats": {"VelocidadAtaque%": 12}},
            "Mira Laser": {"rareza": "Legendario", "stats": {"Critico%": 15}},
            "Moneda Dorada": {"rareza": "Legendario", "stats": {"Oro%": 30}},
            "Cronometro Roto": {"rareza": "Legendario", "stats": {"XP%": 20}}
        }
        guardar_items()

# -------------------------------
# Funciones para manejar el juego
# -------------------------------

def crear_objeto():
    item_name = Prompt.ask("Nombre del objeto")
    if item_name in items:
        console.print(f"[red]El objeto {item_name} ya existe[/red]")
        return
    
    boosts = {}
    while True:
        stat = Prompt.ask("Estadística a potenciar (o 'fin' para terminar)")
        if stat.lower() == "fin":
            break
        if stat not in stats_list:
            console.print(f"[red]Esa estadística no existe[/red]")
            continue
        value = IntPrompt.ask(f"Cuánto aumenta {stat}?")
        boosts[stat] = value
    
    rareza = Prompt.ask("Rareza del objeto", choices=RARITIES)
    
    items[item_name] = {
        "rareza": rareza,
        "stats": boosts
    }

    guardar_items()
    console.print(f"[green]Objeto {item_name} creado con rareza {rareza} y boosts: {boosts}[/green]")

        # Pausa antes de volver al menú
    input("\nPresiona ENTER para regresar al menú...")



def crear_jugador():
    player_name = Prompt.ask("Nombre del jugador")
    if player_name in players:
        console.print(f"[red]El jugador {player_name} ya existe[/red]")
        return
    
    base_stats = {}
    for stat in stats_list:
        base_stats[stat] = IntPrompt.ask(f"Valor base de {stat}")
    
    players[player_name] = {
        "base_stats": base_stats,
        "items": []
    }
    console.print(f"[green]Jugador {player_name} creado[/green]")

        # Pausa antes de volver al menú
    input("\nPresiona ENTER para regresar al menú...")

def asignar_objeto_a_jugador():
    if not players or not items:
        console.print("[red]Necesitas tener jugadores y objetos creados[/red]")
        return
    
    player_name = Prompt.ask("Jugador al que asignar objeto", choices=list(players.keys()))
    item_name = Prompt.ask("Objeto a asignar", choices=list(items.keys()))
    
    players[player_name]["items"].append(item_name)
    console.print(f"[green]{item_name} asignado a {player_name}[/green]")

        # Pausa antes de volver al menú
    input("\nPresiona ENTER para regresar al menú...")

def ver_estadisticas_jugador():
    if not players:
        console.print("[red]No hay jugadores creados[/red]")
        input("Presiona ENTER para regresar al menú...")
        return
    
    player_name = Prompt.ask("Jugador a mostrar", choices=list(players.keys()))
    player = players[player_name]
    
    final_stats = player["base_stats"].copy()
    for item_name in player["items"]:
        boosts = items.get(item_name, {}).get("stats", {})  # más seguro
        for stat, value in boosts.items():
            if stat in final_stats:
                final_stats[stat] += value
            else:
                final_stats[stat] = value
    
    table = Table(title=f"Estadísticas de {player_name}")
    table.add_column("Estadística", style="cyan", no_wrap=True)
    table.add_column("Valor", style="magenta")
    
    for stat, value in final_stats.items():
        table.add_row(stat, str(value))
    
    console.print(table)

    # Pausa antes de volver al menú
    input("\nPresiona ENTER para regresar al menú...")


# -------------------------------
# Función ver objetos con pausa
# -------------------------------

def ver_objetos():
    if not items:
        console.print("[red]No hay objetos creados[/red]")
        input("Presiona ENTER para regresar al menú...")
        return

    table = Table(title="Objetos disponibles")
    table.add_column("Objeto y Efectos", style="bold")

    for item_name, data in items.items():
        rareza = data.get("rareza", "Comun")
        stats = data.get("stats", {})
        color = RAREZA_COLOR.get(rareza, "white")
        efectos_texto = ", ".join([f"{stat} +{value}" for stat, value in stats.items()])
        table.add_row(f"[{color}]{item_name} ({efectos_texto})[/{color}]")

    console.print(table)
    input("\nPresiona ENTER para regresar al menú...")  # pausa antes de volver al menú

# -------------------------------
# Menú principal y main
# -------------------------------

def mostrar_menu():
    console.clear()
    titulo = Panel(
        Align.center(
            Text("ZazaStats", style="bold magenta") + "\n" +
            Text("Simulador de Estadísticas", style="bold green"),
            vertical="middle"
        ),
        border_style="bright_magenta",
        padding=(1, 4)
    )

    opciones = Table.grid(padding=1)
    opciones.add_column(justify="left")

    opciones.add_row("[cyan]1[/cyan] 🧱  Crear objeto")
    opciones.add_row("[cyan]2[/cyan] 👤  Crear jugador")
    opciones.add_row("[cyan]3[/cyan] 🎒  Asignar objeto a jugador")
    opciones.add_row("[cyan]4[/cyan] 📊  Ver estadísticas de jugador")
    opciones.add_row("[cyan]5[/cyan] 🗂️  Ver objetos disponibles")
    opciones.add_row("")
    opciones.add_row("[red]0[/red] 🚪  Salir")

    menu = Panel(
        Align.center(opciones),
        title="[bold yellow]Menú Principal[/bold yellow]",
        border_style="bright_blue",
        padding=(1, 4)
    )

    console.print(titulo)
    console.print(menu)

    choice = IntPrompt.ask("[bold green]Elige una opción[/bold green]")
    return choice

# -------------------------------
# Ejecución principal
# -------------------------------

cargar_items()  # cargar objetos desde JSON al inicio

def main():
    while True:
        choice = mostrar_menu()
        if choice == 1:
            crear_objeto()  # tu función de crear objetos, no incluida aquí
        elif choice == 2:
            crear_jugador()  # tu función
        elif choice == 3:
            asignar_objeto_a_jugador()  # tu función
        elif choice == 4:
            ver_estadisticas_jugador()  # tu función
        elif choice == 5:
            ver_objetos()  # muestra objetos con pausa
        elif choice == 0:
            console.print("[bold red]Saliendo...[/bold red]")
            break
        else:
            console.print("[red]Opción inválida[/red]")

main()
