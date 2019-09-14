import pathlib
import glob


class Rename:
    max = 200
    start = 1

    def inputs(self, path):
        # apath = input('File path')
        apath = pathlib.Path(path)
        return apath

    def getstartandmax(self):
        duo = input('start number and max eps').split(',')
        self.start = int(duo[0])
        self.max = int(duo[1])

    def preview(self, directory, gui=False):
        print(f'+ {directory}')
        count = self.start
        maxcount = self.max
        parts = directory.parts
        parts = parts[len(directory.parts) - 1]
        for path in sorted(directory.glob('*.mkv')):
            # depth = len(path.relative_to(directory).parts)
            # spacer = '    ' * depth
            # print(f'{spacer}+ {path.name}')
            epno = str(count).zfill(2)
            nameString = f"{parts} - {epno}{path.suffix}"
            if gui:
                gui.insert('', 'end', path.name, text=path.name, values=(nameString,''))
            if count == maxcount:
                exit()
            count += 1
        return parts

    def renames(self, directory, name, count, maxcount):
        # count = self.start
        # maxcount = self.max
        for path in sorted(directory.glob('*.mkv')):
            parts = directory.parts
            parts = parts[len(directory.parts)-1]
            epno = str(count).zfill(2)
            nameString = f"{directory}\{name} - {epno}{path.suffix}"
            path.rename(nameString)
            if count == maxcount:
                exit()
            count += 1
