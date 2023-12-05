import uiautomator2 as u2
from ppadb.client import Client
import time
from datetime import datetime
import logging
import os
import re
import traceback
from collections import OrderedDict
from skyrimvsep.enemies import enemies_list
from skyrimvsep.shouts import shouts_list



command_count = 1


setting = ''

# We are using an OrderedDict so that specific enemy types, such as "Ancient Dragon" are tested before general
# enemy types, such as "Dragon".
enemies = OrderedDict({'Arch Necromancer': 'Shout', 'Adoring Fan': 'Weapon', 'Ancient Dragon': 'Shout',
           'Death Hound': 'Weapon', 'Dragon Priest': 'Weapon',
           'Dremora Markynaz': 'Shout', 'Dremora Valkynaz': 'Shout',
           'Elder Dragon': 'Shout', 'Forsworn Ravager': 'Weapon',
           'Forsworn Warlord': 'Weapon', 'Frost Dragon': 'Shout',
           'Frost Troll': 'Weapon', 'Frostbite Spider': 'Weapon', 'Ghost': 'Shout', 'Giant Mudcrab': 'Weapon',
           'Ice Wolf': 'Weapon',
           'Large Mudcrab': 'Weapon',
           'Master Necromancer': 'Shout', 'Renegade Storm Cloak': 'Weapon', 'Sabre Cat': 'Weapon',
           'Bear': 'Weapon', 'Chaurus': 'Weapon', 'Conjurer': 'Shout', 'Cryomancer': 'Shout',
           'Dragon': 'Shout', 'Draugr': 'Shout',
           'Dremora': 'Shout', 'Electromancer': 'Shout', 'Falmer': 'Shout', 'Forsworn': 'Weapon', 'Giant': 'Shout',
           'Mage': 'Shout', 'Mudcrab': 'Weapon', 'Pyromancer': 'Shout', 'Thalmor': 'Shout', 'Troll': 'Weapon',
           'Vampire': 'Shout', 'Werewolf': 'Weapon', 'Wolf': 'Weapon'})
paths = ['Black Iron Gate', 'Broken Open Gate', 'Cobwebbed Passageway', 'Crumbling Staircase',
         'Decoratively Carved Door', 'Definitley Not Booby Trapped Hallway', 'Dimly-Lit Hallway',
         'Foul Smelling Hallway', 'Half-Collapsed Archway', 'Heavy Wooden Door', 'Hidden Staircase',
         'Metal Banded Door', 'Musty Passageway', 'Peaked Archway', 'Portcullis Gate',
         'Sagging Wooden Archway', 'Scarred Iron Door', 'Secret Passageway', 'Simple Wooden Gate',
         'Spiral Staircase', 'Stone Archway', 'Stone Staircase', 'Suspiciously Ordinary Door',
         'Tall Ancient Archway', 'Tapestry-Lined Hallway', 'Torchlit Passageway', 'Unlocked Gate',
         'Well-Worn Passageway', 'Winding Hallway', 'Wooden Staircase', 'shady grove', 'blossoming grove',
         'flooded evergreen grove',
         'trail', 'bridge', 'door', 'gate', 'hill', 'scramble', 'ridge', 'mineshaft', 'tunnel', 'footpath',
         'plateau', 'ladder', 'corridor',
         'ancestral grove', 'foggy deadwood grove',
         'glade', 'path']

locations = ['Abandoned Tower', 'Ancient Standing Stone', 'Bustling Tavern', 'Busy Trading Post',
             'Daedric Shrine', 'Dusty Old Wood Mill', 'Fishing Camp', 'Foggy Dock', 'Fortified Town',
             'Isolated Shack', 'Nordh Village', 'Quaint Farm', 'Small Hamlet', 'Spooky Lighthouse']

objectives = ['will you avenge', 'will you lend', 'will you help']
confirmations = ['face the peril ahead', 'charge into danger', 'wish to proceed',
                 'forward on your quest', 'venture in']


class SkyrimVSEPlayer():
    def __init__(self, outfile='skyrim.txt'):
        self.outfile = outfile
        self.serial = 'emulator-5554'
        self.host = '127.0.0.1'
        self.port = 5037

        outfile_exists = True
        if not os.path.exists(self.outfile):
            outfile_exists = False

        self.my_outfile = open(self.outfile, 'a+', encoding='utf-8')
        if not outfile_exists:
            headers = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n"\
                .format("Timestamp", "Setting", "Command", "ShoutLevel", "SpellLevel", "WeaponLevel",
                        "NewShout", "NewShout2", "CurrentShout", "NewSpell", "CurrentSpell", "NewWeapon",
                        "CurrentWeapon", "NewEnemy", "CurrentEnemy", "Dialog")
            self.my_outfile.write(headers)
            self.my_outfile.flush()
        logging.basicConfig(filename='skyrim_errors.log', format='%(asctime)s %(levelname)-8s %(message)s',
                            level=logging.WARNING, datefmt='%Y-%m-%d %H:%M:%S')
        
        self.enemies = enemies
        self.paths = paths
        self.locations = locations
        self.objectives = objectives
        self.confirmations = confirmations

        self.d = u2.connect('emulator-5554')
        self.command = 'Top'
        self.start_time = datetime.now()
        self.current_time = None
        self.end_time = None

        self.text = ''
        self.special_text = None
        self.special_command = None

        self.command_count = 1
        self.current_time_string = ''

        self.shout_level = 1
        self.spell_level = 1
        self.weapon_level = 1
        self.new_shout = 'Unrelenting Force'
        self.new_shout2 = ''
        self.new_spell = 'Flames'
        self.new_weapon = 'Dagger'
        self.new_enemy = ''
        self.current_enemy = ''
        self.current_weapon = ''
        self.current_shout = ''
        self.current_spell = ''

        self.enemy_dict = {}
        self.spell_dict = {"Flames": 1}
        self.shout_dict = {"Fus!": 1}
        self.weapon_dict = {"Dagger": 1}

        self.high_level = False

    def _get_messages(self):
        try:
            self.special_text = None

            # Send a request other than an answer to Alexa's latest message.
            self.special_command = None

            # Store all requests and responses
            last_texts = []

            # Append responses
            last_responses = self.d(className="android.widget.TextView",
                                    resourceId="com.amazon.dee.app:id/alexa_response")

            if last_responses.count:
                last_response = last_responses[-1]
            for i in range(last_responses.count):
                last_response = last_responses[i]
                last_texts.append(
                    (last_response, "response", last_response.info['bounds']['top'], last_response.info['text']))

            print('last_responses count', last_responses.count)
            last_responses_count = last_responses.count
            if last_responses_count > 0:
                last_response = last_responses[-1]

            # Append requests
            last_requests = self.d(className="android.widget.TextView", resourceId="com.amazon.dee.app:id/user_request")
            for i in range(last_requests.count):
                last_request = last_requests[i]
                last_texts.append(
                    (last_request, "request", last_request.info['bounds']['top'], last_request.info['text']))

            print('last_requests count', last_requests.count)

            # Put messages in the correct order.
            # Higher index value means lower on the screen.
            last_texts.sort(key=lambda x: x[2])

            '''
            # Wait and then see if an additional response has appeared on the screen.
            # I have only ever observed one additional response; so it can be appended without
            # aligning the current and previous responses.
            # Two seconds was not sufficient in my tests. 
            '''
            time.sleep(3.0)
            last_responses2 = self.d(className="android.widget.TextView", resourceId="com.amazon.dee.app:id/alexa_response")
            if last_responses2.count > 0:
                last_response2 = last_responses2[-1]
                text2 = last_response2.info['text']
                if last_texts[-1][1] == "response" and last_texts[-1][3] != text2:
                    last_texts.append((last_response2, "response", last_response2.info['bounds']['top'],
                                       last_response2.info['text']))
                    a = 1

        except u2.exceptions.UiObjectNotFoundError as uonfe:
            # -32001 Jsonrpc error: <androidx.test.uiautomator.UiObjectNotFoundException> data:
            # UiSelector[CLASS=android.widget.TextView, INSTANCE=1, RESOURCE_ID=com.amazon.dee.app:id/user_request],
            # method: objInfo
            print(str(uonfe))
            logging.error(uonfe.message)
            time.sleep(2.0)
            #self.d.screenshot(r'screens\\' + self.current_time_string + "A" + ".jpg")
            return self._get_messages()

        except Exception as e:
            logging.error("GENERAL EXCEPTION " + str(e))
            print(e)
            self._handle_alexa_home_screen()

        return last_texts

    def _combine_messages(self, last_texts):
        if len(last_texts) >= 2:
            if last_texts[-1][1] == "request" and last_texts[-2][1] == "request":
                self.special_command = "Skyrim"

        if len(last_texts) >= 2:
            if last_texts[-1][1] == "response" and last_texts[-2][1] == "response":
                self.special_text = last_texts[-2][0].info['text'] + " " + last_texts[-1][0].info['text']

        if len(last_texts) >= 3:
            if last_texts[-1][1] == "response" and last_texts[-2][1] == "response" and last_texts[-3][1] == "response":
                self.special_text = last_texts[-3][0].info['text'] + " " + last_texts[-2][0].info['text'] + " " + \
                               last_texts[-1][0].info['text']

    def _handle_alexa_home_screen(self):
        time.sleep(30)

        # Check System UI failure
        system_ui_failure = self.d(className="android.widget.TextView", resourceId="android:id/alertTitle")
        if system_ui_failure.count > 0:
            if system_ui_failure[0].info['text'] == "System UI isn't responding":
                self._reboot_phone()

        # Check whether we are at the Alexa home screen.
        vox_buttons = self.d(className="android.widget.ImageView", resourceId="com.amazon.dee.app:id/vox_button")
        if vox_buttons.count > 0 or vox_buttons.count <= 0:
            # Tap circle
            self.d.press("home")  # press the home key, with key name
            time.sleep(5)
            # Stop Alexa
            self.d.app_stop('com.amazon.dee.app')
            time.sleep(10)
            # Start Alexa
            self.d.app_start('com.amazon.dee.app')
            time.sleep(10)
            # Tap typewriter
            # content-desc="Type with Alexa"
            typewriter = self.d(className="android.widget.ImageView",
                           resourceId="com.amazon.dee.app:id/home_header_twa_keyboard")

            if typewriter.count == 0:
                self._reboot_phone()
            try:
                typewriter.click()
                time.sleep(10)
            except Exception as e3:
                self._reboot_phone()

    def _reboot_phone(self):
        print("REBOOTING")
        logging.error("REBOOTING")
        adb = Client(host=self.host, port=self.port)
        adb_device = adb.device(self.serial)
        adb_device.reboot()
        time.sleep(240.0)

    def _setup_files(self):
        if os.path.exists(self.outfile):
            with open(self.outfile, "r", encoding="utf-8") as f2:
                for line in f2:
                    line_chunks = re.split("\t", line)

                    # If the line is malformed, do not collect data from it.
                    if len(line_chunks) < 16:
                        continue

                    # Shout level
                    if line_chunks[3].isnumeric():
                        self.shout_level = int(line_chunks[3])
                    else:
                        if "Level " in line_chunks[3] and 'Shout Skill has increased' in line_chunks[3]:
                            matches = re.finditer(r'Level ([0-9]+)', line_chunks[3])
                            for match in matches:
                                self.shout_level = int(match.group(1))

                    # Spell level
                    if line_chunks[4].isnumeric():
                        self.spell_level = int(line_chunks[4])
                    else:
                        if "Level " in line_chunks[4] and 'Magic Skill has increased' in line_chunks[4]:
                            matches = re.finditer(r'Level ([0-9]+)', line_chunks[4])
                            for match in matches:
                                self.spell_level = int(match.group(1))

                    # Weapon level
                    if line_chunks[5].isnumeric():
                        self.weapon_level = int(line_chunks[5])
                    else:
                        if "Level " in line_chunks[5] and 'Shout Skill has increased' in line_chunks[5]:
                            matches = re.finditer(r'Level ([0-9]+)', line_chunks[5])
                            for match in matches:
                                self.weapon_level = int(match.group(1))

                    combined_level = self.shout_level + self.spell_level + self.weapon_level

                    # Current Shout
                    if line_chunks[8] and not line_chunks[8] == "CurrentShout":
                        self.current_shout = str(line_chunks[8])
                        if self.current_shout not in self.shout_dict:
                            self.shout_dict[self.current_shout] = self.shout_level

                    # New Spell
                    if line_chunks[9] and not line_chunks[9] == "NewSpell":
                        self.new_spell = str(line_chunks[9])
                        if self.new_spell not in self.spell_dict:
                            self.spell_dict[self.new_spell] = self.spell_level

                    # Current Spell
                    if line_chunks[10] and not line_chunks[10] == "CurrentSpell":
                        self.current_spell = str(line_chunks[10])
                        if self.current_spell not in self.spell_dict:
                            self.spell_dict[self.current_spell] = self.spell_level

                    # New Weapon
                    '''
                    if line_chunks[11] and not line_chunks[11] == "NewWeapon":
                        self.new_weapon = str(line_chunks[11]).strip()
                        if self.new_weapon not in self.weapon_dict:
                            self.weapon_dict[self.new_weapon] = self.weapon_level
                    '''

                    # Current Weapon
                    '''
                    if line_chunks[12] and not line_chunks[12] == "CurrentWeapon":
                        self.current_weapon = str(line_chunks[12])
                        if self.current_weapon not in self.weapon_dict:
                            self.weapon_dict[self.current_weapon] = self.weapon_level
                    '''

                    # Current Enemy
                    if line_chunks[14] and not line_chunks[14] == "CurrentEnemy":
                        self.current_enemy = str(line_chunks[14])
                    elif line_chunks[1] in ("Enemy", "Path", "Dungeon", "Exit"):
                        self.current_enemy = self._get_enemy_from_text(line)
                    if self.current_enemy and self.current_enemy not in self.enemy_dict:
                        self.enemy_dict[self.current_enemy] = combined_level

                    # Current Weapon 2
                    # This block is useful to parse logs where NewWeapon was not implemented.
                    if line_chunks[15] and "cast aside your old weapon" in line_chunks[15]:
                        matches = list(re.finditer(r"find (a |an )*(.*), and cast aside", line_chunks[15]))
                        if matches:
                            self.new_weapon = matches[0].group(2).strip()
                            if self.new_weapon not in self.weapon_dict:
                                self.weapon_dict[self.new_weapon] = self.weapon_level

            if self.shout_level + self.spell_level + self.weapon_level >= 143:
                self.high_level = True
        else:
            self.my_outfile.write("Timestamp\tSetting\tRequest\tShout\tSpell\tWeapon\tResponse\n")
            self.my_outfile.flush()
        return True

    def _setup_files2(self):
        # This is a legacy function.
        if os.path.exists(self.outfile):
            with open(self.outfile, "r", encoding="utf-8") as f2:
                for line in f2:
                    line_chunks = re.split("\t", line)
                    if "Level " in line:
                        matches = re.finditer(r'Level ([0-9]+)', line)
                        for match in matches:
                            level = match.group(1)
                            if 'skill with arms has increased' in line:
                                self.weapon_level = int(level)
                            elif 'Shout Skill has increased' in line:
                                self.shout_level = int(level)
                            else:
                                self.spell_level = int(level)
                    if line_chunks[1] in ("Enemy", "Path", "Dungeon", "Exit"):
                        self.current_enemy = self._get_enemy_from_text(line)

            if self.shout_level + self.spell_level + self.weapon_level >= 143:
                self.high_level = True
        else:
            self.my_outfile.write("Timestamp\tSetting\tRequest\tShout\tSpell\tWeapon\tResponse\n")
            self.my_outfile.flush()
        return True

    def _get_enemy_from_text(self, text):
        # This function could have been written to parse enemy names from text, but it is more
        # error-resistant to cycle through the list of all enemy names.
        # The goal is to find the enemy with the longest name to avoid selecting a generic type, such as
        # "Dragon", rather than a specific type, such as "Ancient Dragon".
        possible_enemies = []
        for enemy in enemies_list:
            if enemy in text:
                possible_enemies.append(enemy)
        possible_enemies.sort(key=lambda x: len(x))
        if len(possible_enemies) > 0:
            self.current_enemy = possible_enemies[-1]
            if self.current_enemy not in self.enemy_dict:
                self.enemy_dict[self.current_enemy] = self.shout_level + self.spell_level + self.weapon_level
        else:
            self.current_enemy = ''
        return self.current_enemy

    def _get_shout_from_text(self, text):
        possible_shouts = []
        for shout in shouts_list:
            if shout in text:
                possible_shouts.append(shout)

    def start(self):
        print("STARTING")
        self._setup_files()

        while True:
            current_time = datetime.now()

            self.current_time_string = str(current_time).replace(":", "_").replace(" ", "_")[:19]
            #self.d.screenshot(r'screens\\' + self.current_time_string + ".jpg")

            self.my_outfile.write(str(current_time) + "\t")
            self.my_outfile.flush()
            elapsed = current_time - self.start_time
            print("ELAPSED TIME:", elapsed, "CURRENT TIME", current_time)
            if elapsed.total_seconds() >= 360000:
                break

            last_texts = self._get_messages()
            #with open(r"texts\\" + self.current_time_string + ".txt", "w") as f2:
            #    for lt in last_texts:
            #        f2.write(lt[3] + "\n\n")

            responses = [x for x in last_texts if x[1] == "response"]

            if not len(responses) > 0:
                self.my_outfile.write("\t\t\n")
                self.my_outfile.flush()
                self._handle_alexa_home_screen()
                continue

            text_segments = []
            i = len(last_texts) - 1
            while True:
                if i < 0:
                    break
                if last_texts[i][1] != "response":
                    break
                text_segments.append(last_texts[i][3])
                i -= 1
            text_segments.reverse()
            printable_text = ' '.join(text_segments)


            text = responses[-1][3]
            # print(text)
            text = printable_text


            command = ''

            if not self.special_command:
                if 'ask me anything' in text.lower():
                    setting = "Startup"
                    command = "Skyrim"
                elif 'would you like to continue' in text.lower():
                    setting = "Startup"
                    command = "Yes"
                elif 'what would you like to do' in text.lower():
                    setting = "Enemy"
                    command = None
                    for enemy in enemies.keys():
                        if enemy in text:
                            command = enemies[enemy]
                            break
                    if not command:
                        command = "Shout"
                        print(text)

                    if self.weapon_level < 99:
                        command = "Weapon"
                    elif self.weapon_level + self.spell_level + self.shout_level < 140:
                        command = "Spell"
                    else:
                        command = "Shout"
                elif 'which do you choose' in text.lower():
                    setting = "Path"
                    command = None
                    for path in paths:
                        if path.lower() in text.lower():
                            command = path.title()
                            break
                    if not command:
                        print(text)
                elif 'where would you like to go' in text.lower():
                    command = None
                    setting = "Dungeon"
                    for location in locations:
                        if location.lower() in text.lower():
                            command = location.title()
                            break
                    if not command:
                        print(text)
                elif objectives[0] in text.lower() or objectives[1] in text.lower() or objectives[2] in text.lower():

                    '''
                    if self.weapon_level + self.spell_level + self.shout_level == 145:
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        print("USE SHOUT AT LEVEL 1")
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        break
                    '''

                    #if self.high_level:
                    #    break

                    setting = "Objective"
                    if self.high_level and not 'cave' in printable_text.lower():
                        command = "No"
                    else:
                        command = "Yes"
                    #command = "Yes"
                elif confirmations[0] in text.lower() or confirmations[1] in text.lower() or confirmations[2] in text.lower() or confirmations[3] in text.lower() or confirmations[4] in text.lower():
                    setting = "Confirmation"
                    if self.high_level and 'cave' in printable_text.lower():
                        command = "No"
                    else:
                        command = "Yes"
                    command = "Yes"
                elif 'walking in a circle' in text.lower() or "find yourself at the cave's entrance. neat!" in text.lower() or "path opens to the fort's entrance" in text.lower():
                    setting = "Exit"
                    command = "Skyrim"
                elif 'having trouble accessing your skyrim very special edition' in text.lower():
                    setting = "Failure"
                    command = "Skyrim"
                    time.sleep(20.0)
                else:
                    setting = "Unexpected"
                    command = "Skyrim"
            else:
                command = self.special_command

            # text_box

            if "find yourself at the cave's entrance" in text or 'loops back' in text:
                a = 1

            if self.special_text:
                text = self.special_text
            text = text.replace("\n", " ")

            # Update level
            if "Level " in printable_text:
                matches = re.finditer(r'Level ([0-9]+)', printable_text)
                for match in matches:
                    level = match.group(1)
                    if 'skill with arms has increased' in printable_text:
                        self.weapon_level = int(level)
                    elif 'Shout Skill has increased' in printable_text:
                        self.shout_level = int(level)
                    elif 'Magic Skill has increased' in printable_text:
                        self.spell_level = int(level)

            # Update weapon
            if "cast aside your old weapon" in printable_text:
                matches = list(re.finditer(r"find (a |an )*(.*), and cast aside", printable_text))
                if matches:
                    self.new_weapon = matches[0].group(2).strip()
                    if self.new_weapon not in self.weapon_dict:
                        self.weapon_dict[self.new_weapon] = self.weapon_level

            # Update shout
            if "You now command" in printable_text:
                matches = re.finditer(r"You now command (.*?)\.", printable_text)
                for match in matches:
                    self.new_shout = match.group(1)

            if '!' in printable_text[:17]:
                matches = re.finditer(r'^([A-Z].{1,25}!)', printable_text[:17])
                for match in matches:
                    self.current_shout = match.group(1)
                    if self.current_shout not in self.shout_dict:
                        self.shout_dict[self.current_shout] = self.shout_level
                        self.new_shout2 = self.current_shout

            # Update spell
            if printable_text[0:5] == "Your ":
                # matches = list(re.finditer(r"Your (([A-Z][a-z]* ){1,3})", printable_text))
                matches = list(re.finditer(r"Your ((conjured ){0,1}(([A-Z][a-z']* (of )*){1,3}))", printable_text))
                if matches:
                    self.current_spell = matches[0].group(1)[: -1]
                    self.current_spell = self.current_spell.title().replace(' Of ', ' of ')
                    if self.current_spell not in self.spell_dict:
                        self.spell_dict[self.current_spell] = self.spell_level
                        self.new_spell = self.current_spell

            if setting in ("Enemy", "Path", "Dungeon", "Exit"):
                possible_enemies = []
                from skyrimvsep.enemies import enemies_list
                for enemy in enemies_list:
                    if enemy in printable_text:
                        possible_enemies.append(enemy)

                # Make corrections for specific enemies
                if "Dragon" in possible_enemies:
                    # Dragon is in "Dragonborn".
                    if not re.findall(r"Dragon\b", printable_text) and not list(re.finditer(r"Dragon(?! Claw)", printable_text)):
                        possible_enemies.remove("Dragon")
                if "Falmer" in possible_enemies:
                    # Falmer is in "Falmer ladder"
                    if not list(re.finditer(r"Falmer(?! ladder)", printable_text)):
                        possible_enemies.remove("Falmer")
                if "It's a bear!" in possible_enemies:
                    possible_enemies.remove("It's a bear!")
                    possible_enemies.append("Bear")
                if "bloodthirsty vampire" in possible_enemies:
                    possible_enemies.remove("bloodthirsty vampire")
                    possible_enemies.append("Vampire")

                if printable_text == "You can attack with weapon, cast spell, use shout, or flee. What would you like to do?":
                    possible_enemies.append(self.current_enemy)

                possible_enemies = [x.title() for x in possible_enemies]
                possible_enemies.sort(key=lambda x: len(x))

                if len(possible_enemies) > 0:
                    self.current_enemy = possible_enemies[-1]
                    if self.current_enemy not in self.enemy_dict:
                        self.enemy_dict[self.current_enemy] = self.shout_level + self.spell_level + self.weapon_level
                        self.new_enemy = self.current_enemy
            else:
                self.current_enemy = ''


            if printable_text:
                printable_text = printable_text.replace("\n", " ")

            out_line = setting + "\t" + str(command) + "\t" + str(self.shout_level) + "\t" + \
                str(self.spell_level) + "\t" + str(self.weapon_level) + "\t" + printable_text

            out_line = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'\
                .format(setting, str(command), str(self.shout_level), self.spell_level, self.weapon_level,
                        self.new_shout, self.new_shout2, self.current_shout, self.new_spell, self.current_spell, self.new_weapon,
                        self.current_weapon, self.new_enemy, self.current_enemy, printable_text)

            print(out_line)
            # print(self.special_text)
            self.my_outfile.write(out_line + "\n")
            self.my_outfile.flush()

            self.new_shout = ''
            self.new_shout2 = ''
            self.new_spell = ''
            self.current_spell = ''
            self.new_weapon = ''
            self.current_shout = ''
            self.new_enemy = ''


            if self.shout_level + self.spell_level + self.weapon_level >= 143:
                print("LEVEL BREAK 1")
                self.high_level = True

            time.sleep(2.0)

            try:

                text_box = self.d(className="android.widget.EditText", resourceId="com.amazon.dee.app:id/input_text")
                if text_box.count < 1:
                    continue
                text_box[0].set_text(command)
                time.sleep(0.5)

                send_button = self.d(className="android.widget.FrameLayout", resourceId="com.amazon.dee.app:id/send_button")
                send_button.click()
            except u2.exceptions.UiObjectNotFoundError as uonfe:
                logging.error(uonfe.message)
                self._handle_alexa_home_screen()

            time.sleep(4.0)

            if (self.shout_level + self.spell_level + self.weapon_level >= 155) and \
                    'very special edition' in printable_text.lower():
                print("LEVEL BREAK 2")
                out_line = self.current_time_string + "\t" + "KILL SCREEN" + "\t" + str(command) + "\t" + \
                           str(self.shout_level) + "\t" + \
                           str(self.spell_level) + "\t" + str(self.weapon_level) + "\t" + printable_text
                self.my_outfile.write(out_line + "\n")
                self.my_outfile.flush()
                break
            a = 1

            #if self.command_count >= 50:
            #    break
            #self.command_count += 1

        self.my_outfile.close()

        end_time = datetime.now()
        print(end_time - self.start_time)
        print("Done")

        return True


if __name__ == '__main__':
    svsep = SkyrimVSEPlayer()
    ret_val = svsep.start()
    print(str(ret_val))
