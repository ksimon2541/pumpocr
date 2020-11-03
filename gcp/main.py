import argparse
from pump_ocr import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    parser.add_argument('-img_dir', help='Optional directory to bulk process imgs', default=0)
    args = parser.parse_args()

    render_doc_text(args.detect_file, args.out_file)
    document = annotate_image(args.detect_file)
    print('SONG: {}'.format(find_song_title(document)))
    print('DIFFICULTY: {} {}'.format(find_playstyle(document), find_difficulty(document)))
    print('JUDGEMENT MODIFIER: {}'.format(find_judge_mod(document)))
    print('RANK: {}'.format(find_rank(document)))
    print('JUDGEMENTS: {}'.format(find_judgements(document)))
    print('MAX COMBO: {}'.format(find_max_combo(document)))
    print('TOTAL SCORE: {}'.format(find_total_score(document)))
