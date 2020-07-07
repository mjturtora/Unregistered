# Module to generate list of all unit numbers in each building
import pandas as pd

def block(floor_min=1, floor_max=1, unit_min=1, unit_max=1):
    # Creates blocks of unit numbers
    units = set([(str(f) + str(u).zfill(2))
                        for f in range(floor_min, floor_max+1)
                            for u in range(unit_min, unit_max+1)])
    return units


def bayfront():
    # floors 8 -27
    # units 01-14 w/o 13
    # floors 23-27 units 03-04 paired (so no 04)

    # Address data like: Unit, Ste, and #
    # 1 Beach Dr SE # 4
    # 1 Beach Dr SE Unit 914
    # 1 Beach Dr SE Ste 1014
    complete_set = block(floor_min=8, floor_max=27, unit_min=1, unit_max=14)
    # create exclusions ("empty set" - No unit xx13 and paired units 03 & 04 for floors 23-27)
    empty_set = block(floor_min=8, floor_max=27, unit_min=13, unit_max=13) | \
                    block(floor_min=23, floor_max=27, unit_min=4, unit_max=4)
    apartments = complete_set - empty_set
    return apartments


def beacon430():
    # 430 3rd Avenue South
    # 4 floors each with 87 units, numbered 101-187, 201-287, 301-387, and 401-487
    apartments = block(floor_min=1, floor_max=4, unit_min=1, unit_max=87)
    return apartments


def beacononthird():
    # Beacon on Third has 8 floors 2-9, and 14 units per floor (112) within the rectangular part of the building.
    # The West end, the "Y", is 9 floors (2-10)  and 8 units per floor (72). A total of 184 units
    complete_set = block(floor_min=2, floor_max=10, unit_min=1, unit_max=22)
    # create exclusions ("empty set" - no units 1-14 on 10)
    empty_set = block(floor_min=10, floor_max=10, unit_min=1, unit_max=14)
    apartments = complete_set - empty_set
    return apartments


def bliss():

    # Bliss Tower is at 176 4th Ave NE, 33701.
    s = \
"""201, 301, 401, 501, 502, 601, 602, 701, 702, 801, 802, 901, 902, 1001, 1002, 1101, 1102, 1201, 1202, 1401, 1402, 
1501, 1502, 1601, 1602, 1701, 1702, 1801, 1802"""
    apartments = set(s.replace('\n', '').replace(' ', '').split(','))
    return apartments


def camden():
    # Create apartment structure as set
    # 22 units / floor except first floor with 6
    # first create complete set
    complete_set = block(floor_min=1, floor_max=18, unit_min=1, unit_max=22)
    # create exclusions ("empty set" - union of first floor extras and thirteenth floor)
    empty_set = block(floor_min=1, floor_max=1, unit_min=7, unit_max=22) | \
                    block(floor_min=13, floor_max=13, unit_min=1, unit_max=22)
    apartments = complete_set - empty_set
    return apartments


def cloisters():
    # 288 Beach Drive, N. E.
    # According to Nona Peebles, the building captain, the unit numbers below are
    # either Republican or unregistered in Florida.
    s = "3A, 3C, 4A, 4C, 5A, 5B, 5C, 6A, 8B, 9A, 9B, 10B, 10C, 11A, 11B, 11C, 12B, PH1, PH2"
    apartments = set(s.replace('\n', '').replace(' ', '').split(','))
    return apartments


def cottonwood():
    # 235 3rd Avenue North
    s = \
"""100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 114, 116, 131, 135, 137, 139, 141, 143, 145, 147, 149, 151,
165, 167, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 214, 216, 217, 219, 231, 233, 235, 237,
239, 241, 243, 245, 247, 249, 251, 253, 255, 257, 259, 261, 263, 265, 267, 702, 703, 704, 705, 706, 707, 708, 709,
710, 711, 712, 713, 714, 715, 716, 717, 719, 721, 723, 731, 733, 735, 737, 739, 741, 743, 745, 747, 749, 751, 753,
755, 757, 761, 763, 765, 767"""
    apartments = set(s.replace('\n', '').replace(' ', '').split(','))
    t = """600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 619, 621, 623, 
           625, 627, 629, 631, 633, 635, 637, 639, 641, 643, 645, 647, 649, 651, 653, 655, 657, 659, 661, 665, 667"""
    t = t.replace('\n', '').replace(' ', '').split(',')
    v = [u[1:] for u in t]
    block = set([(str(f) + str(u).zfill(2))
                        for f in range(3, 7)
                            for u in v])
    apartments = apartments | block
    return apartments


def florencia():
    # 100 Beach Dr NE, St. Petersburg, FL 33701 ??
    # Create apartment structure as set
    # The Florencia living floors begin with one unit on the 3rd floor (301),
    # on floors 4-18 there are 3 units per floor (401, 402, 403, etc.),
    # then things change: 1900, 1901, 1902, 2001, 2002,
    # finally, there are the penthouses (2100, 2200).

    # todo: double check that there is a 13th floor!!!

    # first create complete set
    apartments = {'301', '1900', '1901', '1902', '2001', '2002', '2100', '2200'}
    fblock = block(floor_min=4, floor_max=18, unit_min=1, unit_max=3)
    apartments = apartments | fblock
    return apartments


def huntington():
    # 350 2nd Street North
    apartments = set([str(s) for s in range(1, 28)])
    return apartments


def presbyterian():
    # 4320 Bay Street, N.E.
    # 2-15 floors 01-15 units
    apartments = block(floor_min=2, floor_max=15, unit_min=1, unit_max=15)
    return apartments


def rowlandplace():
    # 146th 4th Ave
    s = \
"""201, 202, 203, 204, 301, 302, 303, 304, 401, 402, 403, 404, 501, 502, 503, 504, 600"""
    apartments = set(s.replace('\n', '').replace(' ', '').split(','))
    return apartments


def sage():
    # 400 4th Avenue South
    complete_set = block(floor_min=1, floor_max=12, unit_min=1, unit_max=10)
    # create exclusions ("empty set")
    s = "109, 110, 209, 210, 310, 409, 410, 510"
    empty_set = set(s.replace('\n', '').replace(' ', '').split(','))
    apartments = complete_set - empty_set
    return apartments

def salvador():
    #199 Dali Blvd
    #Unit and # for PH
    # Floors 3-12 + PH
    # 1-6 for 3rd floor, 1-7 for 4-12, 1-5 PH
    complete_set = {'PH1', 'PH2', 'PH3', 'PH4', 'PH5'}
    complete_set |= block(floor_min=3, floor_max=12, unit_min=1, unit_max=7)
    complete_set -= {'307'}
    return complete_set

def signature():
    #175 1st St S
    #Apt
    #Saved in Excel File "Signature Unit Numbers" with sheetname "Signature"
    fname = r"..\io\input\Signature Unit Numbers.xlsx"
    print('Reading data file: "{}"'.format(fname))
    df = pd.read_excel(fname, sheet_name='Signature')
    df['Unit'].str.strip
    apartments = set(df['Unit'].str.replace('#', ''))
    return apartments

