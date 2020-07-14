# unreg.py is the "main" program. It imports a module for "building"
# the structure of each building and another module for
# parsing addresses.

# still need 400 beach or whatever it was... the complicated one

# file input path in function get_address
# reads data for each building from a worksheet with all
# buildings in one workbook (usually)

# file output path in __main__
# setup to write each building to separate worksheets in a single workbook

# Using tuples of (function_named_for_building, worksheet_name_of_building):
# designed to run through all at once when everything is working but
# each one must be tested one at a time

# eventually, this should make it easy to run updates.

import os
import pandas as pd

# frowned upon syntax but works:
from buildings import *
from parse_buildings import *

# pandas display options
pd.options.display.precision = 2
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#####################################

path = os.getcwd()
print(f"The current working directory is {path}")


def get_building(build_tuple):
    """Wrapper to call each building structure. Returns list of valid unit numbers"""
    building = eval(build_tuple[0] + '()')
    try:
        print(f'building {build_tuple[0]} =  {sorted(building, key=int)}')
    except ValueError:
        print(f'building {build_tuple[0]} =  {building}')
    print(f'Number of apartments in {build_tuple[0]} =  {len(building)}')
    return building


def get_address(building_sheetname):
    """Read raw data and return all addresses as dataframe. Bad separation of concerns"""
    #todo: split into separate read and clean functions
    fname = r"..\io\input\Primary Building Captain contact information and VBM target postcard number 1 May 2020.xlsx"
    #fname = r"D:\Stuff\Projects\Pol\Unregistered\data\WinstonParklist20200612-6816659306"
    print('Reading data file: "{}"'.format(fname))
    print(f'building_sheetname: {building_sheetname}')
    df = pd.read_excel(fname, sheet_name=building_sheetname)
    #print(f'dataframe from file: {df}')
    df['Address'].str.strip
    address = df['Address'].sort_values()
    return address


def get_diff(build_tuple):
    """Where the magic happens. Calls helper functions to get data needed
     for set difference of units in building by name.
    Prints diagnostics. Probably doing too much."""
    # todo: split out print statements
    apartments = get_building(build_tuple)
    address = get_address(build_tuple[1])
    registered_units = parse_addresses(address, build_tuple[2], build_tuple[3])
    # todo: need to test type before key=int sort
    try:
        unregistered_units = sorted(apartments - registered_units, key=int)
    except ValueError:
        unregistered_units = apartments - registered_units
    output(build_tuple, unregistered_units)

    print('worksheet_name:', build_tuple[1])
    print(f'Number of ADDRESSES in {build_tuple[0]} = {len(address)}')
    #try catch to account for apartments with alpha characters
    #Doesn't sort if an exception is thrown
    try:
        print('All Apartments: ', sorted(apartments, key=int))
        # print(len(apartments))
        print('registered_units: ', sorted(registered_units, key=int))
        # print(len(registered_units))
        print('unregistered_units: ', sorted(unregistered_units, key=int))
        # print(len(unregistered_units))
    except ValueError:
        print('All Apartments: ', apartments)
        print('registered_units: ', registered_units)
        print('unregistered_units: ', unregistered_units)
    print('\n****************************')
    return


def output(build_tuple, unregistered_units):
    """export to excel worksheet in already opened workbook"""
    df = pd.DataFrame.from_dict({build_tuple[0]: unregistered_units})
    df.to_excel(writer, sheet_name=build_tuple[0])


if __name__ == "__main__":

    path = r'..\io\Output\Unregistered Units.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    # new format for tuples: (function name, sheet name, street number, unit string list)
    # removes need for multiple parse functions
    # buildings = [
    #               ('fourHundredBeach', '400 Beach', '400', ['Unit']),
    #               ('bayfront', 'Bayfront Tower', '1', ['Unit', 'Ste', '#']),
    #               ('beacon430', 'Beacon 430', '430', ['Apt']),
    #               ('beacononthird', 'BeaconOn3rd_sheet'),                <-- didn't see sheet for this one
    #               ('bliss', 'Bliss', '176', ['Unit']),
    #               ('camden', 'Camden Pier Dist', '330', ['Unit']),
    #               ('cloisters', 'Cloisters', '288', ['Apt', 'Ph', '#']),  <-- funky one
    #               ('cottonwood', 'Cottonwood Bayview', '235', ['Unit']),
    #               ('florencia', 'Florencia', '100', ['Unit']),
    #               ('hermitage', 'Hermitage', '151', ['Unit']),  <-- Also missing sheet, Harbor's Edge exists twice
    #               ('huntington', 'Huntington', '350', ['Apt']),
    #               ('presbyterian', 'Presbyterian Towers', '430', ['Apt']),
    #               ('rowlandplace', 'Rowland Place', '146', ['Unit']),
    #               ('sage', 'Sage_sheetname'),                             <-- also didn't see sheet for this one
    #               ('salvador', 'Salvador', '199', ['Unit', '#']),
    #               ('signature', 'Signature', '175', ['Apt']),
    #               ('winstonPark', ???, '5095', [])      <-- Also missing sheet
    #            ]
    #
    # ('WinstonPark', 'WinstonParklist20200612-6816659306')
    # #buildings = [('bayfront', 'Bayfront Tower')]
    buildings = [
        ('fourHundredBeach', '400 Beach', '400', ['Unit'])
    ]
    for build_tuple in buildings:
        unregistered_units = get_diff(build_tuple)

    writer.save()
    writer.close()
