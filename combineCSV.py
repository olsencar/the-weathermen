def main():
    fw = open("weather-data-complete.csv", "w");
    fr = open("weather-data-miles.csv", "r");
    fw.write(fr.read());
    fw.write("\n");
    fr.close();
    fr = open("weather-data-shane.csv", "r");
    fw.write(fr.read());
    fw.write("\n");
    fr.close();
    fr = open("weather-data-carter.csv", "r");
    fw.write("\n")
    fw.write(fr.read());
    fr.close();

if __name__ == '__main__':
    main();