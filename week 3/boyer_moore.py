def reverse_indices(arr: list[int]) -> list[int]:
    size = len(arr) - 1
    return [arr[-(x+1)] for x in range(len(arr))]


def reverse_z_algorithm(str: str) -> list[int]:
    reversed_str = str[::-1]
    reversed_indices = z_algorithm(reversed_str)
    return reverse_indices(reversed_indices)

def z_algorithm(str: str) -> list[int]:
    z_values=[len(str)]
    l=0
    r=0

    for i in range(1, len(str)):
        if i > r:
            new_z_value = find_new_z_box(str, i, 0)
            z_values.append(new_z_value)
            if i + new_z_value > r:
                l = i
                r = i + new_z_value
        
        else:
            #i within z_box
            corr_z_value = z_values[i-l]

            # case 2a: corresponding z-value is within z-box
            if corr_z_value < r - i:
                z_values.append(corr_z_value)
            
            # case 2b: corresponding z-value is remainder of length of z-box
            elif corr_z_value == r - i:
                known = corr_z_value
                new_z_value = find_new_z_box(str, i, corr_z_value)
                z_values.append(new_z_value)
                if i + new_z_value > r:
                    l = i
                    r = i + new_z_value
            
            # case 2bb: corresponding z-value is larger than box
            else:
                new_z_value = r - i
                z_values.append(new_z_value)
            
        i += 1
    
    return z_values

def find_new_z_box(str: str, i: int, known: int) -> int:
    new_z_value = 0 + known
    prefix_curr = known
    idx = i + known
    
    if idx > len(str) - 1:
        return new_z_value
    while str[idx] == str[prefix_curr]:
        prefix_curr += 1
        new_z_value += 1

        if idx == len(str) - 1:
            break
        idx += 1
        
    
    return new_z_value

def good_suffix(z_suffix_array: list[int]) -> list[int]:
    good_suffix_array = [0 for _ in range(len(z_suffix_array))]
    num_char = len(z_suffix_array)

    for index, value in enumerate(z_suffix_array[:-1]):
        if value > 0:
            good_suffix_array[num_char - value] = index

    return good_suffix_array
    
def bad_character_1d(pat:str) -> dict[str, int]:
    dict = {}
    for index, char in enumerate(pat):
        dict[char] = index
    return dict

def bad_character_2d(pat:str) -> list[dict[str, int]]:
    arr = []
    for length in range(1, len(pat) + 1):
        arr.append(bad_character_1d(pat[:length]))
    
    return arr

def matched_prefix(z_suffix_array: list[int]) -> list[int]:
    arr = []
    map(lambda index, value: value if (index-value==0) else 0, enumerate(z_suffix_array))
    curr_max = z_suffix_array[0]
    for index, value in enumerate(z_suffix_array):
        curr_max = max(curr_max, value)
        arr.append(curr_max)
    
    return arr[::-1]

def boyer_moore(pat: str, txt: str)-> tuple[list[int], int]:
    z_suffix_array = reverse_z_algorithm(pat)
    good_suffix_array = good_suffix(z_suffix_array)
    bad_char_k_array = bad_character_2d(pat)
    matched_prefixes_array = matched_prefix(z_suffix_array)
    matches = []
    curr_txt_boundary = len(pat) - 1
    pat_length = len(pat)
    comparisons = 0

    if pat == "":
        return []
    
    while curr_txt_boundary <= len(txt) - 1:
        curr_observed_txt_index = curr_txt_boundary
        is_match = False
        for curr_observed_pat_index in range(len(pat) - 1, -1, -1):
            
            comparisons += 1
            if txt[curr_observed_txt_index] != pat[curr_observed_pat_index]:
                bad_char_val = bad_char_k_array[curr_observed_pat_index].get(txt[curr_observed_txt_index])
                good_suffix_val = good_suffix_array[min(curr_observed_pat_index + 1, len(pat) - 1)]
                if bad_char_val is None:
                    bad_char_val = 0
                
                n_bad_char = pat_length - bad_char_val - 1
                n_good_suffix = pat_length - good_suffix_val - 1
                shift_amt = min(n_bad_char, n_good_suffix)
                
                if shift_amt == 0:
                    shift_amt = pat_length - matched_prefixes_array[curr_observed_pat_index]

                is_match = False
                break

            is_match = True
            curr_observed_txt_index -= 1

        if is_match:
            matches.append(curr_txt_boundary)
            if len(pat) > 1:
                curr_txt_boundary += len(pat) - 1 - matched_prefixes_array[1] 
            else:
                curr_txt_boundary += 1
        else:
            curr_txt_boundary += shift_amt
    
    return matches, comparisons

def boyer_moore_binary_optimised(pat: str, txt: str)-> tuple[list[int], int]:
    z_suffix_array = reverse_z_algorithm(pat)
    good_suffix_array = good_suffix(z_suffix_array)
    bad_char_k_array = bad_character_2d(pat)
    matched_prefixes_array = matched_prefix(z_suffix_array)
    matches = []
    curr_txt_boundary = len(pat) - 1
    pat_length = len(pat)
    comparisons = 0

    if pat == "":
        return []
    
    while curr_txt_boundary <= len(txt) - 1:
        curr_observed_txt_index = curr_txt_boundary
        is_match = False
        for curr_observed_pat_index in range(len(pat) - 1, -1, -1):
            
            comparisons += 1
            if txt[curr_observed_txt_index] != pat[curr_observed_pat_index]:
                bad_char_val = bad_char_k_array[curr_observed_pat_index].get(txt[curr_observed_txt_index])
                good_suffix_val = good_suffix_array[min(curr_observed_pat_index + 1, len(pat) - 1)]
                if bad_char_val is None:
                    bad_char_val = 0
                
                n_bad_char = pat_length - bad_char_val - 1
                n_good_suffix = pat_length - good_suffix_val - 1
                shift_amt = min(n_bad_char, n_good_suffix)
                
                if shift_amt == 0:
                    shift_amt = pat_length - matched_prefixes_array[curr_observed_pat_index]

                is_match = False
                break

            is_match = True
            curr_observed_txt_index -= 1

        if is_match:
            matches.append(curr_txt_boundary)
            if len(pat) > 1:
                curr_txt_boundary += len(pat) - 1 - matched_prefixes_array[1] 
            else:
                curr_txt_boundary += 1
        else:
            curr_txt_boundary += shift_amt
    
    return matches, comparisons

def naive_pat_match(pat: str, txt: str) -> tuple[list[int],int]:
    matches = []
    comparisons = 0
    for i in range(len(txt)-len(pat)+1):
        for j in range(len(pat)):
            comparisons += 1
            if txt[i+j] != pat[j]:
                break
            if j == len(pat)-1:
                matches.append(i)
            
    
    return (matches, comparisons)

from timeit import default_timer as timer

start1 = timer()
print(naive_pat_match('abbcbcbcb', 'aaacbbabasccbcbacbabcbbcccbsacbhscxsdbabababbabbbaaacbbabasccbcbacbabcbbcccbsacbhscxsdbabababbabbbaaacbbabasccbcbacbabcbbcccbsacbhscxsdbabababbabbbaaacbbabasccbcbacbabcbbcccbsacbhscxsdbabababbabbb'))
end1 = timer()
print(start1-end1)

start2=timer()
print(boyer_moore('abbcbcbcb', 'aaacbbabasccbcbacbabcbbcccbsacbhscxsdbabababbabbbaaacbbabasccbcbacbabcbbcccbsacbhscxsdbabababbabbbaaacbbabasccbcbacbabcbbcccbsacbhscxsdbabababbabbbaaacbbabasccbcbacbabcbbcccbsacbhscxsdbabababbabbb'))
end2=timer()
print(start2-end2)
