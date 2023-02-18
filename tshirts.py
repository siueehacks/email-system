from dotenv import load_dotenv

from helpers.sheets import get_sheet_info

load_dotenv()

SAMPLE_RANGE_NAME = "Form Responses 1!L:L"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    values = get_sheet_info(SAMPLE_RANGE_NAME)

    if not values:
        print("No data found.")
        return

    shirt_dict = {}
    for row in values[1:]:
        if row[0] in shirt_dict:
            shirt_dict[row[0]] += 1
        else:
            shirt_dict[row[0]] = 1
    
    print(f'Total: {len(values[1:])}')
    print(shirt_dict)


if __name__ == "__main__":
    main()
