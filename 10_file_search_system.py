"""
LLD Problem: Design a File Search System.
"""

"""
Should allow users to search files like the linux Find command.
2 filters -> minimum size, and file extension.
the default method is AND if anyone mentions both of these flags, but also implement an OR filter
"""

"""
File:
- name, size, is_directory, extension, children

Filter(ABC):
- apply(file) -> applies the filter on a file

MinSizeFilter(Filter):
- size
- apply(file) -> returns if the size of the file is greater than the mentioned size

ExtensionFilter(Filter):
- extension
- apply(file) -> returns if the extension of the file is the same as mentioned extension

FileSearcher():
- apply_filter(filters, root) -> starts searching files from the root file (can be directory) and applies filters

- file search will be through BFS as we can think of a file system as a tree. 
- in the AND filter, we will check all filters, and if any of them fails, we will break out of the loop and not append the child.
- in the OR filter, we check the filters and if any of them return True, then we append the child.

"""

from abc import ABC, abstractmethod
from collections import deque # for BFS file search


class File:
    def __init__(self, name: str, size: float) -> None:
        self.name = name
        self.size = size
        
        self.is_directory = False if "." in self.name else True
        self.extension = self.name.split(".")[-1] if "." in self.name else ""
        
        self.children = [] # if it is a direcrory, then it can have children

class Filter(ABC):
    def __init__(self) -> None:
        pass
       
    @abstractmethod
    def apply(self, file: File) -> bool:
        pass

class MinSizeFilter(Filter): # returns files with size > min_size
    def __init__(self, size: float) -> None:
        self.size = size
    
    def apply(self, file: File) -> bool:
        return file.size > self.size

class ExtensionFilter(Filter):
    def __init__(self, extension: str) -> None:
        self.extension = extension
    
    def apply(self, file: File) -> bool:
        return self.extension == file.extension


class FileSearcher():
    
    def apply_filter(self, filters: list[Filter], root: File, mode: str) -> list:
        if not filters:
            raise ValueError("Please add at least one filter.")
        
        mode = mode.lower()
        if mode not in ["and", "or"]:
            raise ValueError("Mode can only be AND or OR.")
        
        res = []
        q = deque()
        q.append(root)
        
        while q:
            curr = q.popleft()
            if curr.is_directory:
                for child in curr.children:
                    q.append(child)
            else:
                if mode == "and":
                    flag = True
                    for filter in filters:
                        if not filter.apply(curr):
                            flag = False
                            break
                    if flag:
                        res.append(curr)
                
                elif mode == "or":
                    for filter in filters:
                        if filter.apply(curr):
                            res.append(curr)
                            break # either is true so we can break
                
        return res
        
        
def main():
    try:
        f1 = File("root_300", 300)
        
        f2 = File("cats_100", 100) # directory
        f3 = File("dogs_100", 100) # directory
        f4 = File("bird_100", 100) # directory
        
        f1.children = [f2, f3, f4]
        
        f5 = File("cat1.img", 5)
        f6 = File("cat2.jpg", 6)
        f7 = File("cat3.xml", 8)
        
        f2.children = [f5, f6, f7]
        
        f8 = File("dog1.jpg", 8)
        f9 = File("dog2.xml", 7)
        f10 = File("dog3.png", 6)
        
        f3.children = [f8, f9, f10]
       
        min_size_filter = MinSizeFilter(5)
        jpg_filter = ExtensionFilter("jpg")
        
        finder = FileSearcher()
        
        print("\nAND filter for min_size = 5 and extension = jpg:")
        filters=[min_size_filter, jpg_filter]
        print([f.name for f in finder.apply_filter(root=f1, filters=filters, mode="and")])
        
        print("\nOR filter for min_size = 5 and extension = jpg:")
        filters=[min_size_filter, jpg_filter]
        print([f.name for f in finder.apply_filter(root=f1, filters=filters, mode="or")])
    except ValueError as e:
        print(e)
        
if __name__ == "__main__":
    main()