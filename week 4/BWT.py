def BWT(suffix_array: list[list[tuple[str, int]]]) -> list[str]:
    pass


def get_rank_arr(suffix_array: list[list[tuple[str,int]]]) -> list[int]:
    rank_arr = [0 for _ in range(26)]
    prev_letter = '$'
    for i in range(1, len(suffix_array)):
        curr_letter = suffix_array[i][0]
        if curr_letter != prev_letter:
            rank_arr[ord(curr_letter) - 97] = i 
            prev_letter = curr_letter
    
    return rank_arr

def get_nocc_arr(BWT_L_arr: list[str]) -> list[list[int]]:
    nocc_table = []
    prevcalc = [0 for _ in range(26)]
    nocc_table.append(prevcalc)
    for i in range(len(BWT_L_arr)):
        new_calc = prevcalc[:]
        observed_letter = BWT_L_arr[i]
        new_calc[ord(observed_letter) - 97] += 1
        prevcalc = new_calc


def get_char_table(letter: str, char_arr: list[int]) -> int:
    return char_arr[ord(letter) - 97]

def set_char_table(letter: str, number: int, char_arr: list[int]) -> None:
    char_arr[ord(letter) - 97] = number

def set_rank(letter: str, rank: int, rank_arr: list[int]):
    rank_arr[ord(letter) - 97] = rank

def get_nocc(letter: str, i_exclusive: int, nocc_arr: list[list[int]]) -> int:
    return nocc_arr[i_exclusive][ord(letter) - 97]