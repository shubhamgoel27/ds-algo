from collections import defaultdict
from typing import List

class Solution:
    def get_sequence(self, string):
        seq = ''
        if len(string)==1:
            return "-1"
        for i in range(1, len(string)):
            diff = (ord(string[i]) - ord(string[i-1]) +26)%26
            seq+=str(diff) +","
        return seq


    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        seq_dict = defaultdict(list)
        for s in strings:
            seq = self.get_sequence(s)
            seq_dict[seq].append(s)
        
        final = [] 

        for seq, str_list in seq_dict.items():
            final.append(str_list)

        return final 
