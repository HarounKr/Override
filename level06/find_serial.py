import sys

def calculate_serial(s):
    serial = (ord(s[3]) ^ 0x1337) + 6221293
    for i in range(len(s)):
        if ord(s[i]) <= 31:
            return 1 
        serial += (serial ^ ord(s[i])) % 0x539
    return serial

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        target_string = sys.argv[1]
    else:
        print("No target string provided.")
        sys.exit(1) 

    result = calculate_serial(target_string)
    if result == 1:
        print("Invalid input or too short string.")
    else:
        print('Serial is:', result)
