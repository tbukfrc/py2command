global generate_method
command_order = []
repeating = False


def is_repeating(boolean=False):
    global repeating
    if boolean:
        repeating = True
    else:
        repeating = False


def is_list_empty(provided_list):
    if len(provided_list) == 0:
        return True
    return False


def item_startswith(item):
    if item.startswith('minecraft:'):
        return True
    else:
        return False


def nbt_parser(nbt):
    if is_list_empty(nbt):
        return nbt
    else:
        nbt_listed = ['{']
        real_nbt = ''
        for entry in nbt:
            if entry.startswith('Name'):
                if ',' in entry:
                    name_lore = entry.split(',')
                    name = name_lore[0].replace('Name=', '')
                    nbt_listed.append(
                        r'display:{Name:\\\"' + '[{' + r'\\\\\\\"text\\\\\\\":\\\\\\\"' + name + r'\\\\\\\",' +
                        r'\\\\\\\"italic\\\\\\\"' + r':false}]\\\"' + r',Lore:[\\\"' +
                        '[{' + r'\\\\\\\"text\\\\\\\":\\\\\\\"' +
                        name_lore[1] + r'\\\\\\\",\\\\\\\"italic\\\\\\\":false}]' + r'\\\"]}')
                    nbt_listed.append(',')
                else:
                    name = entry.replace('Name=', '')
                    nbt_listed.append(r'display:{Name:\\\"' + r'[{\\\\\\\"text\\\\\\\":\\\\\\\"' + name +
                                      r'\\\\\\\",'
                                      r'\\\\\\\"italic '
                                      r'\\\\\\\":false}]' +
                                      r'\\\"}')
            elif entry.startswith('Enchant='):
                if ',' in entry:
                    enchant = entry.replace('Enchant=', '')
                    enchant_list = enchant.split(',')
                    nbt_listed.append('Enchantments:[')
                    for enchantment in enchant_list:
                        enchant_amp = enchantment.split(':')
                        if item_startswith(enchant_amp[0]):
                            nbt_listed.append(r'{id:\\\"' + enchant_amp[0] + r'\\\",lvl:' + enchant_amp[1] + '}')
                            nbt_listed.append(',')
                        else:
                            nbt_listed.append(
                                r'{id:\\\"minecraft:' + enchant_amp[0] + r'\\\",lvl:' + enchant_amp[1] + '}')
                            nbt_listed.append(',')
                    if nbt_listed[-1] == ',':
                        nbt_listed.pop()
                        nbt_listed.append(']')
                        nbt_listed.append(',')
                else:
                    enchant = entry.replace('Enchant=', '')
                    enchant_amp = enchant.split(':')
                    if item_startswith(enchant_amp[0]):
                        nbt_listed.append(
                            r'Enchantments:[{id:\\\"' + enchant_amp[0] + r'\\\",lvl:' + enchant_amp[1] + '}]')
                        nbt_listed.append(',')
                    else:
                        nbt_listed.append(
                            r'Enchantments:[{id:\\\"minecraft:' + enchant_amp[0] + r'\\\",lvl:' + enchant_amp[1] + '}]')
                        nbt_listed.append(',')
            elif entry == 'Unbreakable':
                nbt_listed.append('Unbreakable:1b')
                nbt_listed.append(',')
        if nbt_listed[-1] == ',':
            nbt_listed.pop()
            nbt_listed.append('}')
        else:
            nbt_listed.append('}')
        for data in nbt_listed:
            real_nbt += data
        return real_nbt


def get_skull(target, player):
    command_order.append('give ' + target + ' minecraft:player_head{SkullOwner:"' + player + '"}')


def say(text):
    command_order.append('say ' + text)


def clear(targets, item=None, max_count=None):
    if item is None:
        command_order.append('clear ' + targets)
    else:
        if max_count is None:
            if item_startswith(item):
                command_order.append('clear ' + targets + ' ' + item)
            else:
                command_order.append('clear ' + targets + ' minecraft:' + item)
        else:
            if item_startswith(item):
                command_order.append('clear ' + targets + ' ' + item + ' ' + str(max_count))
            else:
                command_order.append('clear ' + targets + ' minecraft:' + item + ' ' + str(max_count))


def give(targets, item, nbt=None, count=1):
    if nbt is None:
        nbt = []
    if item_startswith(item):
        command_order.append('give ' + targets + ' ' + item + nbt_parser(nbt) + ' ' + str(count))
    else:
        command_order.append('give ' + targets + ' minecraft:' + item + nbt_parser(nbt) + ' ' + str(count))


def end_code(filename):
    if generate_method == "one_command":
        run_int = 2
        command_string = ''
        print('\033[4;49;93mWARNING\033[0;49;93m:\033[0;49;97m One command creations are still in early testing. '
              'There may be errors '
              'when importing your commands.')
        with open(filename + "_one_command.txt", "w") as file:
            command_string += (
                '/summon minecraft:falling_block ~2 ~2 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:['
                '{id:falling_block,Time:0,BlockState:{Name:dirt},Passengers:[{id:falling_block,Time:1,'
                'BlockState:{Name:activator_rail}},')
            for command in command_order:
                if command == command_order[0] and repeating:
                    command_string += ('{id:command_block_minecart,Command:"setblock ~' + str(
                        run_int) + ' ~-1 ~ minecraft:repeating_command_block[facing=east]{Command:' + r'\"' + command +
                                       r'\"}' + '"},')
                    run_int += 1
                elif command == command_order[0] and repeating is not True:
                    command_string += ('{id:command_block_minecart,Command:"setblock ~' + str(
                        run_int) + ' ~-1 ~ minecraft:command_block[facing=east]{Command:' + r'\"' + command + r'\"}' +
                                       '"},')
                    run_int += 1
                else:
                    command_string += ('{id:command_block_minecart,Command:"setblock ~' + str(
                        run_int) + ' ~-1 ~ minecraft:chain_command_block[facing=east]{auto:1b,Command:' + r'\"' +
                                       command
                                       + r'\"}' + '"},')
                    run_int += 1
            command_string += '{id:command_block_minecart,Command:"kill @e[type=command_block_minecart]"},'
            final_command_string = command_string[:-1]
            final_command_string += ']}]}'
            file.write(final_command_string)
    if generate_method == "plaintext":
        with open(filename + ".txt", "w") as file:
            for command in command_order:
                if command == command_order[0] and repeating:
                    file.write('[REPEAT] ')
                    file.write(command + '\n')
                elif command == command_order[0] and repeating is not True:
                    file.write('[IMPULSE] ')
                    file.write(command + '\n')
                else:
                    file.write('[CHAIN] ')
                    file.write(command + '\n')
