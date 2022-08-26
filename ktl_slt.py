import sys, os, time, csv

file_list = []
total_result = []

def run():
    total_insert = total_delete = total_substitution = total_sentence_len = 0
    total_WER = total_infer = total_slt = 0.0

    for fname in file_list:
        # AI function
        # fname is a filename without path
        # header = ['Filename','Ref','HYP','Insert', 'Delete', 'Substitution', 'Sentence_len','WER','Total time','SLT time']
        result = ai_func(fname)
        # the end of AI function

        total_result.append(result)
        total_insert += float(result[3])
        total_delete += float(result[4])
        total_substitution += float(result[5])
        total_sentence_len += float(result[6])
        total_WER += float(result[7])
        total_infer += float(result[8])
        total_slt += float(result[9])

        print(fname, len(total_result))

    tline = len(total_result)
    last_line = [ "Result", "", "", f"{total_insert}", f"{total_delete}", f"{total_substitution}", f"{total_sentence_len}",
            f"{(total_insert+total_delete+total_substitution)/total_sentence_len}", f"{total_infer/tline}", f"{total_slt/tline}" ]

    # csv file
    if len(total_result) > 0:
        header = ['Filename','Ref','HYP','Insert', 'Delete', 'Substitution', 'Sentence_len','WER','Total time','SLT time']
        with open('result.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(total_result)
            writer.writerow(last_line)


def ai_func(filename):
    time.sleep(0.5)
    return_list = [filename, "2.5", "2.3", '1', '2', '3', '4', "4.5", "7.2", "3.2"]
    return return_list

if __name__ == "__main__":
    if len(sys.argv) == 2:
        target_dir = sys.argv[1]
        if os.path.isdir(target_dir) :
            print("Start....")
            for fname in os.listdir(target_dir):
                if fname.endswith('.mp4'):
                    file_list.append(fname)
        else:
            print(f"{target_dir} is not a directory")
        print(f"{len(file_list)} have been selected")
        run()
    else:
        print("Example:\npython ktl_slt.py <directory>")
