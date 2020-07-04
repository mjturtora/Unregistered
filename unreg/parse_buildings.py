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

    for u in unit_string:
        print(f'u={u}')
        address = address[address.str.contains(u)].str.rsplit(n=1, expand=True)
        #print(type(address))

    unit_count = len(address)
    registered_units = set(address[1].values)
    unique_unit_count = len(registered_units)
    counts = (raw_address_count, street_number_count, unit_count, unique_unit_count)
    print_counts(counts)
    return registered_units

# Maybe don't need functions for each one anymore...
# could just loop through a list (of tuples?) with NAME, Street_Number, and Unit_string

def parse_camden(address):
    """Controls parsing for Camden"""
    street_number = '330'
    unit_string = ['Unit']
    return parse_addresses(address, street_number, unit_string)


def parse_presbyterian(address):
    """Controls parsing for Presbyterian"""
    street_number = '430'
    unit_string = ['Apt']
    return parse_addresses(address, street_number, unit_string)
