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
    print(f'building {build_tuple[0]} =  {sorted(building, key=int)}')
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
    """Where the magic happens. Calls helper functions to get set difference for apartments in building_name.
    Prints diagnostics. Probably doing too much."""
    # todo: split out print statements
    apartments = get_building(build_tuple)
    address = get_address(build_tuple[1])
    print(f'Number of ADDRESSES in {build_tuple[0]} = {len(address)}')
    registered_units = eval('parse_' + build_tuple[0] + '(address)')
    # todo: need to test type before key=int sort
    unregistered_units = sorted(apartments - registered_units, key=int)
    print('worksheet_name:', build_tuple[1])
    print('All Apartments: ', sorted(apartments, key=int))
    print('registered_units: ', sorted(registered_units, key=int))
    print('unregistered_units: ', sorted(unregistered_units, key=int))
    print('\n****************************')
    output(build_tuple, unregistered_units)
    return  #unregistered_units


def output(build_tuple, unregistered_units):
    """export to excel worksheet in already opened workbook"""
    df = pd.DataFrame.from_dict({build_tuple[0]: unregistered_units})
    df.to_excel(writer, sheet_name=build_tuple[0])


if __name__ == "__main__":

    #path = r'D:\Stuff\Projects\Pol\Unregistered\Output\Unregistered Units.xlsx'
    path = r'..\io\Output\Unregistered Units.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    # df3.to_excel(writer, sheet_name = 'x3')
    # df4.to_excel(writer, sheet_name = 'x4')
    # writer.save()
    # writer.close()
    # buildings = [('bayfront', 'Bayfront Tower'), ('beacon430', 'Beacon 430'), ('beacononthird', 'BeaconOn3rd_sheet'),
    #              ('bliss', 'Bliss'), ('camden', 'Camden Pier Dist'), ('cloisters', 'Cloisters'),
    #              ('cottonwood', 'Cottonwood Bayview'), ('florencia', 'Florencia'),
    #              ('huntington', 'Huntington'), ('presbyterian', 'Presbyterian Towers'),
    #              ('rowlandplace', 'Rowland Place'), ('sage', 'Sage_sheetname')]
    #
    # ('WinstonPark', 'WinstonParklist20200612-6816659306')
    # #buildings = [('bayfront', 'Bayfront Tower')]
    buildings = [('camden', 'Camden Pier Dist'), ('presbyterian', 'Presbyterian Towers')]
    for build_tuple in buildings:
        unregistered_units = get_diff(build_tuple)
    #     output(build_tuple, unregistered_units)

    writer.save()
    writer.close()
