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

def exact_pattern_match(pat: str, str: str) -> list[int]:
    z_values = z_algorithm(pat + '$' + str)
    important_z_values = z_values[len(pat)+1:]
    occurences = []
    for idx, z_value in enumerate(important_z_values):
        if z_value == len(pat):
            occurences.append(idx)

    return occurences



print(exact_pattern_match('abc', 'aaabcddabcab'))