import re

class TuringMachine:
    def start_machine(path: str = 'table.txt') -> None:
        with open(path, 'r') as f:
            program = f.read()
        line = program.split('\n', maxsplit=1)[0]
        programs = re.findall('q[0-9]{1,}#[0-9]{1,}q[0-9]{1,}#[0-9]{1,}[RLS]', program)

        table = {}
        max_code_for_symbol = 0 
        for program in programs:
            current_state = program.split('q')[1].split('#')[0]
            current_symbol = program.split('q')[1].split('#')[1]
            target_state = program.split('q')[2].split('#')[0]
            target_symbol = program.split('q')[2].split('#')[1][:-1]
            target_move = program.split('q')[2].split('#')[1][-1:]
            program_set = {current_symbol:
                        {'target_state': target_state,
                            'target_symbol': target_symbol,
                            'target_move':target_move}
                        }
            max_code_for_symbol = max(max_code_for_symbol, len(current_symbol), len(target_symbol))
            table.setdefault(current_state, {}).update(program_set)

        current_state = '1'
        comands = [line[i:i+max_code_for_symbol] for i in range(0, len(line), max_code_for_symbol)]
        if len(comands[-1]) != max_code_for_symbol:
            comands[-1] = comands[-1] + '0' * (max_code_for_symbol - len(comands[-1]))

        skip = True
        run = True
        i = 0
        while run:
            if i >= 200:
                run = False
                break
            if skip:
                if int(comands[i]) != 0:
                    skip = False
                    i -= 1
                i+=1
            else:
                if i >= len(comands):
                    comands.append('0' * max_code_for_symbol)
                if table.get(current_state) and table.get(current_state).get(comands[i]):
                    current_state_update = table.get(current_state).get(comands[i]).get('target_state')
                    current_symbol = table.get(current_state).get(comands[i]).get('target_symbol')
                    current_move = table.get(current_state).get(comands[i]).get('target_move')
                    current_state = current_state_update
                    comands[i] = '0' * (max_code_for_symbol - len(current_symbol)) + current_symbol
                    if current_move == 'R':
                        i += 1
                    elif current_move == 'L':
                        i -= 1
                    if current_state == '0':
                        run = False
                    print(''.join(comands))
                else:
                    run = False
        print('---------------', ''.join(comands), 'EXIT', sep='\n')
        return 
if __name__ == '__main__':
    TuringMachine.start_machine()