file_path = "./Docling_sample_B.md"  # Replace with the actual path to your file

my_list = []   # For header line
my_list1 = []  # For data line

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        line_count = 0
        for line in file:
            words = [word.strip() for word in line.strip().split('|') if word.strip()]
            if line_count == 0:
                my_list = words
            elif line_count == 1:
                my_list1 = words
            line_count += 1
    
    # Convert the two lists to a dictionary
    my_dict = dict(zip(my_list, my_list1))
    # print("my_list:", my_list)
    # print("my_list1:", my_list1)
    print(my_dict)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
