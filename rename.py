import pathlib
import glob
import re


class Rename:
    def __init__(self):
        self.max = 0
        self.start = 1
        self.addSpacing = True
        self.theMode = 0
        self.extensions = ["ANY"]
        self.theExtension = 0

    def inputs(self, path):
        # apath = input('File path')
        apath = pathlib.Path(path)
        return apath

    def getNameString (self, count, parts, path):
        if self.theMode == 0:
            epno = str(count).zfill(2)
            nameString = f"{parts} - {epno}{path.suffix}"
        elif self.theMode == 1:
            nameString = f'{str(count)}{path.suffix}'
        elif self.theMode == 2:
            nameString = f'{str(count).zfill(4)}{path.suffix}'
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
        for path in sorted(directory.glob('*.*')):
            # depth = len(path.relative_to(directory).parts)
            # spacer = '    ' * depth
            # print(f'{spacer}+ {path.name}')
            if path.suffix not in self.extensions:
                self.extensions.append(path.suffix)
            nameString = self.getNameString(count,parts,path)
            gui.insert('', 'end', path.name, text=path.name, values=(nameString,''))
            count += 1
        self.max = count -1
        print(self.extensions)
        return parts

    def renames(self, directory, name, count, maxcount):
        # count = self.start
        # maxcount = self.max
        parts = directory.parts
        parts = parts[len(directory.parts)-1]
        if self.theExtension != 0:
            theExtension = '*'+ self.extensions[self.theExtension]
        else:
            theExtension = '*.*'
        for path in sorted(directory.glob(theExtension)):
            epno = str(count).zfill(2)
            nameString = self.getNameString(count,parts,path)
            nameString = f"{directory}\{nameString}"
            path.rename(nameString)
            if count == maxcount:
                exit()
            count += 1
