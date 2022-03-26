# py2command
 py2command is a Minecraft command block wrapper for Python. It provides a simple way to write long command block chains while maintaining the ability to see multiple "command blocks" at once. It can also generate working NBT data for you, making it much easier to use correct syntax.
# Usage:
A pip package for py2command is coming soon, when the project is more developed.

If you would like to test py2command early, simply put the ```py2command.py``` file in the same folder as your python script, and import it! (it is recommended to import py2command like: ```import py2command as p2c``` to avoid typing as many characters).

Read the [docs](https://github.com/tbukfrc/py2command/wiki) to see the full list of supported commands and features!

# Example:
Here's a comparison of the same exact command (give unbreakable named knockback stick with mending, knockback 15, and lore) written in game vs. in py2command.

In game: `give @p minecraft:stick{display:{Name:'[{"text":"Knockback Stick","italic":false}]',Lore:['[{"text":"A stick with extreme knockback","italic":false}]']},Enchantments:[{id:"minecraft:knockback",lvl:15},{id:"minecraft:mending",lvl:1}],Unbreakable:1b} 1`

With py2command: `p2c.give('@p', 'stick', ['Name=Knockback Stick,A stick with extreme knockback', 'Enchant=knockback:15,mending:1', 'Unbreakable'], 1)`

py2command takes the command and automatically parses and converts it into something you can paste into Minecraft. Think of it as multiple command generators built-in to one Python module, with a system to automagically convert them to command blocks.
