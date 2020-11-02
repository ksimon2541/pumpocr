import argparse
from pump_ocr import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()

    document = annotate_image(args.detect_file)
    print('SONG: {}'.format(find_song_title(document)))
    print('DIFFICULTY: {} {}'.format(find_playstyle(document), find_difficulty(document)))
    print('RANK: {}'.format(find_rank(document)))
    print('JUDGEMENTS: {}'.format(find_judgements(document)))
    print('MAX COMBO: {}'.format(find_max_combo(document)))
    print('TOTAL SCORE: {}'.format(find_total_score(document)))
