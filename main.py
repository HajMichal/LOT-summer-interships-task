import xml.etree.ElementTree as ET
import argparse

# parse and obtain the root element of the XML file
tree = ET.parse('example.xml')
root = tree.getroot()

# user data display scheme
def print_person(person):
    print("Name: ", person[0].text)
    print("Surname: ", person[1].text)
    print("Age: ", person[2].text)
    print("Gender: ", person[3].text)
    print("Rank: ", person[4].text)
    print("Salary: ", person[5].text + '\n')

# checks whether the data provided by the user is correct with the one 
# given in the arguments ( or if it is in the range of )
def filter_persons(root, args):
    for child in root:
        if args.rank and child[4].text == args.rank:
            print_person(child)
        elif args.gender and child[3].text == args.gender:
            print_person(child)
        elif (args.age_range and args.age_range[0] <= int(child[2].text) 
            <= args.age_range[1]):
            print_person(child)
        elif (args.salary_range and args.salary_range[0] <= int(child[5].text)
            <= args.salary_range[1]):
            print_person(child)

def main():
    parser = argparse.ArgumentParser(
        description="This programme filters the data and returns user depends on given arguments and values. You can choose one of the following options:")
    
    # specify argument cases
    parser.add_argument('--rank', metavar='RANK', type=str, help="Rank")
    parser.add_argument('--gender', metavar='GENDER', type=str, help="Gender")
    parser.add_argument(
        '--age-range', 
        nargs=2, 
        metavar=('MIN', 'MAX'), 
        type=float, 
        help='Age range'
        )
    parser.add_argument(
        '--salary-range', 
        nargs=2, 
        metavar=('MIN', 'MAX'), 
        type=float, 
        help='Salary range'
        )

    args = parser.parse_args()

    # checks if user provide any argument when starting programme
    if args.rank or args.gender or args.age_range or args.salary_range:
        filter_persons(root, args)
    else:
        print("You didn't provide any argument with value. For more information type: \n\n $ python3 main.py -h \n or \n $ python3 main.py --help ")


if __name__ == '__main__':
    main()