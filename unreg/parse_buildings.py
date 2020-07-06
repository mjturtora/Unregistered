# Module to parse each building's address strings
# Began working for situation where each building needs more
# than one "Unit String" (like "Unit" or "Apt") but haven't needed it.

def print_counts(counts):
    print('pre-filtered number of addresses: ', counts[0])
    print('Number of addresses starting with street number: ', counts[1])
    print('Number of addresses containing UNIT: ', counts[2])
    print('Number of UNIQUE Units: ', counts[3])

def parse_addresses(address, street_number, unit_string):
    """Gets unique unit numbers from dataframe of addresses"""
    raw_address_count = len(address)
    address = address[address.str.startswith(street_number)]
    street_number_count = len(address)

    #create empty set to add new sets to
    #This way we are not overwriting the address variable
    #for buildings with multiple unit strings
    registered_units = set()

    for u in unit_string:
        print(f'u={u}')
        # print(type(address))
        temp_df = address[address.str.contains(u)].str.rsplit(n=1, expand=True)
        registered_units |= set(temp_df[1].values)

    #run through apts and replace any O with 0 (because yes someone typed an O instead of a 0)
    for apt in registered_units:
        if 'O' in apt:
            index = apt.find('O')
            newAptNumber = apt[:index] + '0' + apt[index+1:]
            registered_units.remove(apt)
            registered_units.add(newAptNumber)


    unit_count = len(address)
    # registered_units = set(address[1].values)
    unique_unit_count = len(registered_units)
    counts = (raw_address_count, street_number_count, unit_count, unique_unit_count)
    print_counts(counts)
    return registered_units

# Maybe don't need functions for each one anymore...
# could just loop through a list (of tuples?) with NAME, Street_Number, and Unit_string

