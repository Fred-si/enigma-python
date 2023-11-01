class Enigma:
    available_rotor = [
        'DMTWSILRUYQNKFEJCAZBPGXOHV',
        'HQZGPJTMOBLNCIFDYAWVEUSRKX',
        'UQNTLSZFMREHDPXKIBVYGJCWOA',
        'JGDQOXUSCAMIFRVTPNEWKBLZYH',
        'NTZPSFBOKMWRCJDIVLAEYUXHGQ',
        'JVIUBHTCDYAKEQZPOSGXNRMWFL',
        'PEZUOHXSCVFMTBGLRINQJWAYDK',
        'ZOUESYDKFWPCIQXHMVBLGNJRAT',
        'EHRVXGAOBQUSIMZFLYNWKTPDJC',
        'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'VZBRGITYUPSDNHLXAWMJQOFECK',
        'JPGVOUMFYQBENHZRDKASXLICTW',
        'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'FKQHTLXOCBJSPDZRAMEWNIUYGV',
    ]
    reflector = ('QYHOGNECVPUZTFDJAXWMKISRBL')

    def __init__(self, *, debug: bool = False):
        self.debug = print if debug else lambda *_, **__: None
        self.plainMessage = None
        self.plugBoard = {}
        self.rotor_place = []
        self.rotor_position = []

    def set_initial_rotor_place(self, rotor_list):
        for r_p in rotor_list.split():
            self.rotor_place.append(self.available_rotor[int(r_p)])

    def set_plugin_board(self, plugin_list):
        if self.is_not_valid_plugin(plugin_list):
            raise ValueError('you can not use a letter already swap or have more than 10 pair')

        self.plugBoard = plugin_list.split()

    def is_not_valid_plugin(self, plugins) -> bool:
        used_letter = set()
        for pair in plugins.split():
            for letter in pair:
                if letter in used_letter:
                    return True
                used_letter.add(letter)
        return False

    def set_initial_rotor_position(self, rotor_position):
        for rotor in rotor_position.split():
            self.rotor_position.append(int(rotor))

    def udpate_rotor_position(self):
        if self.rotor_position[2] == 25:
            self.rotor_position[1] = int(self.rotor_position[1]) + 1
            self.rotor_position[2] = 0
        else:
            self.rotor_position[2] = int(self.rotor_position[2]) + 1

        if self.rotor_position[1] == 25:
            self.rotor_position[0] = int(self.rotor_position[0]) + 1
            self.rotor_position[1] = 0

        if self.rotor_position[0] == 25:
            self.rotor_position[0] = 0

    def set_plain_message(self, plain_message: str):
        self.plainMessage = plain_message

    def output_message(self, message: str) -> str:
        output = []
        for letter in message:
            origin = letter
            p = letter
            self.debug(f'Encode {p}')
            self.udpate_rotor_position()

            letter = self.do_swap_letter(letter)
            self.debug(f'Converted {p} -> {letter}'); p = letter

            for iteration in range(3):
                letter = self.rotor(letter, iteration=iteration)
                self.debug(f'Converted {p} -> {letter}'); p = letter

            letter = self.rotor(letter=letter, reflector=True)
            self.debug(f'Converted {p} -> {letter}'); p = letter

            for iteration in range(3):
                letter = self.rotor(letter=letter, iteration=iteration, revert=True)
                self.debug(f'Converted {p} -> {letter}'); p = letter

            letter = self.do_swap_letter(letter)
            self.debug(f'Converted {p} -> {letter}'); p = letter

            output.append(letter)

            self.debug(f'Encoded {origin} -> {letter}')

        return "".join(output)

    def rotor(self, letter: str, iteration: int = 0, reflector: bool = False, revert: bool = False) -> str:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        rotor_choice = self.rotor_place
        rotor_position = self.rotor_position

        if not revert:
            rotor_choice = self.rotor_place[::-1]
            rotor_position = self.rotor_position[::-1]

        if reflector:
            rotor_choice = [self.reflector]
            rotor_position = [0]

        letter = letter.upper()

        if alphabet.index(letter) + int(rotor_position[iteration]) > 25 and not revert:
            return rotor_choice[iteration][alphabet.index(letter) + int(rotor_position[iteration]) - 26]

        if revert:
            return alphabet[rotor_choice[iteration].index(letter) - int(rotor_position[iteration])]
        return rotor_choice[iteration][alphabet.index(letter) + int(rotor_position[iteration])]

    def do_swap_letter(self, letter: str) -> str:
        for plug in self.plugBoard:
            if letter.upper() == plug[0]:
                return plug[1]
            if letter.upper() == plug[1]:
                return plug[0]
        return letter

if __name__ == '__main__':
    enigma = Enigma(debug=True)
    enigma.set_initial_rotor_place('4 9 10')
    enigma.set_plugin_board('ZL RC WN JP KF IO HV ED GX MT')
    enigma.set_initial_rotor_position('20 23 11')
    print(enigma.output_message('AHAHAHJEVOUSAIBIENNIQUE'.replace(' ', '')))
    # print(enigma.output_message('SPIB UWBJ EDIB CNGG PAKR RQG'.replace(' ', '')))

    from sys import exit
    exit(0)
    enigma = Enigma()

    print('Choose rotor position between those (rotor are place from right to left):')
    for index, a in enumerate(enigma.available_rotor):
        print('{0} : {1}'.format(index, a))
    rotor_place = input('Enter order with whitespace : ')

    enigma.set_initial_rotor_place(rotor_place)

    plugin = input('Enter your pair to swap key with whitespace, 10 pair max (example : AE IO BD) : ')
    enigma.set_plugin_board(plugin)

    rotor_pos = input('Enter {} position of rotor between 0 and 25 separate by whitespace, one for each : '.format(len(enigma.available_rotor)))
    enigma.set_initial_rotor_position(rotor_pos)

    message = input('Enter your message without whitespace : ')
    enigma.set_plain_message(message)

    print(enigma.output_message())