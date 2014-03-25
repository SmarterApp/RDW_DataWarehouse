import DataGeneration.src.constants.constants as constants


def derive_demographic(demo_list):
    '''
    Main function to generate the derived demographic columns.
    @param demo_list: list of boolean values for each demographic. The order is:
    1. African American,
    2. Asian,
    3. Hispanic,
    4. Native American / Alaskan Native,
    5. Pacific Islander,
    6. White
    '''
    try:
        # TODO: need to decide the value. is it true/false, or f/t, or others
        if demo_list[constants.HISPANIC_CODE - 1] is True:
            return constants.HISPANIC_CODE
        else:
            race_count = 0
            result = 0
            for i in range(len(demo_list)):
                if i == constants.HISPANIC_CODE - 1:
                    continue
                else:
                    if demo_list[i] is True:
                        race_count += 1
                        result = i + 1
            if race_count > 1:
                return constants.TWO_OR_MORE_RACES_CODE
            else:
                return result
    except:
        print("Generate derived demographic column error")
        return -1


"""
if __name__ == '__main__':
    print(derive_demographic([False, True, True, True, True, True]))
"""
