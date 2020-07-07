import pathlib
import glob
import re


class Rename:
    def __init__(self):
        self.max = 0
        self.start = 1
        self.addSpacing = True
        self.theMode = 0

    def inputs(self, path):
        # apath = input('File path')
        apath = pathlib.Path(path)
        return apath

    def getNameString (self, count, parts, path):
        if self.theMode == 0:
            epno = str(count).zfill(2)
            nameString = f"{parts} - {epno}{path.suffix}"
        elif self.theMode == 1:
            nameString = str(count)
        elif self.theMode == 2:
            nameString = str(count).zfill(4)
        elif self.theMode == 3:
            nameString = re.sub(r"([\s_]?)([\[\(]([^\]\[\(\)]|[\[\(][\]\)])*[\]\)])([\s_]?)",'',path.name)
        if self.addSpacing:
            nameString = re.sub(r'([\._])(?=.*\.[^\.]*$)'," ",nameString)
        
        return nameString

    def preview(self, directory, gui, customName=False):
        print(f'+ {directory}')
        count = self.start
        parts = directory.parts
        parts = parts[len(directory.parts) - 1]
        if customName:
            parts = customName
        for path in sorted(directory.glob('*.mkv')):
            # depth = len(path.relative_to(directory).parts)
            # spacer = '    ' * depth
            # print(f'{spacer}+ {path.name}')
            nameString = self.getNameString(count,parts,path)
            gui.insert('', 'end', path.name, text=path.name, values=(nameString,''))
            count += 1
        self.max = count -1
        print(count)
        return parts

    def renames(self, directory, name, count, maxcount):
        # count = self.start
        # maxcount = self.max
        parts = directory.parts
        parts = parts[len(directory.parts)-1]
        for path in sorted(directory.glob('*.mkv')):
            epno = str(count).zfill(2)
            nameString = self.getNameString(count,parts,path)
            nameString = f"{directory}\{nameString}"
            path.rename(nameString)
            if count == maxcount:
                exit()
            count += 1
