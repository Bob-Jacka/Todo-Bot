commands: dict[str, str] = {
    "helpBot": "help",
    "delTask": "delete",
    "notifTask": "notify",
    "addTask": "add",
    "viewTask": "view",
    "changeTask": "change",
    "all_to_do": "all"
}
"""
Map with bot commands to action
"""

other_handlers: dict[str, str] = {
    "HiHandler": "привет"
}

"""
List of the command for bot interaction
"""

hello_words: tuple = ("привет", "hello", "hi")

bye_words: tuple = ("пока", "bye", "goodbye")

dirty_words: tuple = ("жопа ленивая", "зайчик", "котик", "ежик", "пингвиненок")
"""
Dirty words that bot might say to you
"""
