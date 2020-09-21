import json
import difflib
import base64
import os


def main():
    def add_to_clip_board(text):
        command = 'echo ' + text.strip() + '| clip'
        os.system(command)


    def get_exact_item_name(non_item_name):
        exact_items_names = []

        with open('items.txt') as json_file:
            data = json.load(json_file)

            for a in data:
                exact_items_names.append(a)
        json_file.close()

        try:
            return difflib.get_close_matches(non_item_name.upper().replace(" ", "_"), exact_items_names)[0]
        except IndexError:
            return None


    def get_item_texture(item_name):
        exact_item_name = get_exact_item_name(item_name)

        with open('items.txt') as json_file:
            data = json.load(json_file)
            pairs = data.items()

            for p, i in pairs:
                if p == exact_item_name:
                    item = i.items()

                    for j, k in item:
                        if j == "texture":
                            return k
            return None


    def get_head(item_name):
        item_texture = get_item_texture(item_name)
        if item_texture is None:
            return None
        else:
            texture_bytes = ('{"textures":{"SKIN":{"url":"http://textures.minecraft.net/texture/' + str(get_item_texture(item_name)) + '"}}}').encode('ascii')
            base64_bytes = base64.b64encode(texture_bytes)
            texture_base64 = base64_bytes.decode('ascii')

            return '/give @p minecraft:player_head{SkullOwner:{Id:[I;-903112851,1937327098,-1258035656,1495487699],Properties:{textures:[{Value:"' + str(texture_base64) + '"}]}}} 1'


    def script():
        print("Please enter the name of the item :")
        print()
        name = input()
        print("")
        if name == "":
            script()
        else:
            head = get_head(name)
            if head is None:
                print("Incorrect Name")
                print("")
                script()
            else:
                print("")
                print(head)
                print("")
                resp = input("Would you like to send the command into your clipboard ? (y or n)")
                if resp == "y":
                    add_to_clip_board(head)
                else:
                    exit()

    script()


if __name__ == '__main__':
    main()