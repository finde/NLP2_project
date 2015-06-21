import sys
import fileinput

if __name__ == "__main__":
    temp_str = ''
    temp_count = 0.0

    for line in fileinput.input():
        temp = line.split(' -==- ')

        if temp_str == temp[0]:
            temp_count += float(temp[1])

        else:
            if temp_str != '':
                sys.stdout.write(temp_str + " " + str(temp_count) + "\n")

            temp_str = temp[0]
            temp_count = float(temp[1])

    sys.stdout.write(temp_str + " " + str(temp_count))