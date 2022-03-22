

def get_print_poke_name(pokemon, shiny, argument=""):
  printpokename = ""
  if shiny:
    printpokename += "shiny "
  if argument.lower() == "alolan":
    printpokename += " alolan "
  if argument.lower() == "galarian":
    printpokename += " galarian "
  printpokename += pokemon
  printpokename = printpokename.strip()
  return printpokename