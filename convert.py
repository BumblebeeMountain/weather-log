import datetime

def convert(strTime):
    # 2021-01-08 12:19, 998.9
    empty = strTime.replace("-", "")
    empty = empty.replace(" ", "")
    empty = empty.replace(":", "")

    y = int(empty[0:4])
    m = int(empty[4:6])
    d = int(empty[6:8])

    h = int(empty[8:10])
    minute = int(empty[10:12])

    return int(datetime.datetime(y, m, d, h, minute).timestamp())

def main():
    f = open("pressure.csv", "r")
    text = f.read()
    f.close()
    lines = text.split("\n")
    head = lines.pop(0)
    lines.pop()

    lines = [val.split(", ") for val in lines]

    outString = head + "\n"
    for l in lines:
        l[0] = convert(l[0])
        outString += "{}, {}\n".format(l[0], l[1])

    outFile = open("p.csv", "w")
    outFile.write(outString)
    outFile.close()



if __name__ == "__main__":
    main()
