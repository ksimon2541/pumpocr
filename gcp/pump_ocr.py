from vision_api_helpers import *

judgements = ['PERFECT', 'GREAT', 'GOOD', 'BAD', 'MISS']
playstyles = ['SINGLE', 'DOUBLE']
judge_mods = ['HJ', 'VJ']
ranks = ['SSS', 'SS', 'S', 'A', 'B', 'C', 'D', 'F']


# Search all words and largest numerical value should always be TOTAL SCORE.
def find_total_score(document):
    largest = 0
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)

                    try:
                        candidate = int(assembled)
                        if candidate > largest:
                            largest = candidate
                    except ValueError:
                        pass
    return str(largest)


# Song title is always centered and slightly above PERFECT judgement.
def find_song_title(document):
    perfect_bounds = find_word_location(document, 'PERFECT')
    if perfect_bounds == None:
        return 'Not Found'
    expected_song_bounds = [perfect_bounds.vertices[0].x, perfect_bounds.vertices[0].y-100, perfect_bounds.vertices[1].x, perfect_bounds.vertices[0].y]
    song_title = text_within(document, expected_song_bounds[0], expected_song_bounds[1], expected_song_bounds[2], expected_song_bounds[3])
    return song_title


def find_playstyle_bounds(document):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)
                    if assembled in playstyles:
                        return word.bounding_box


def find_playstyle(document):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)
                    if assembled in playstyles:
                        return assembled
    return 'Not Found'

def find_judge_mod(document):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)
                    if assembled in judge_mods:
                        return assembled
    return 'NJ'



# Look for a number between 0 and 28 that is near find_playstyle_bounds to ensure we're not taking some other number
# coincidentally in our range.
def find_difficulty(document):
    playstyle_bounds = find_playstyle_bounds(document)
    if playstyle_bounds == None:
        return 'Not Found'
    expected_difficulty_bounds = [playstyle_bounds.vertices[0].x-50, playstyle_bounds.vertices[0].y+20,
                            playstyle_bounds.vertices[1].x+50, playstyle_bounds.vertices[0].y+20]
    difficulty = text_within(document, expected_difficulty_bounds[0], expected_difficulty_bounds[1], expected_difficulty_bounds[2],
                             expected_difficulty_bounds[3])
    return difficulty


# Rank will always be one of the entries in ranks list, so just check against those.
def find_rank(document):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)
                    if assembled in ranks:
                        return assembled
    return 'Not Found'


# find_word_location makes it easy to find specific text on image.
def find_judgements(document):
    judgement_pairs = []
    for judgement in judgements:
        judgement_bounds = find_word_location(document, judgement)

        # todo: use different method to locate judgements that is more consistent
        if judgement_bounds == None:
            judgement_pairs.append((judgement, 'Not Found'))
        else:
            judgement_count = find_judgement_count(document, judgement_bounds, judgement)
            judgement_pairs.append((judgement, judgement_count))
    return judgement_pairs


# Judgement counts will always have similar vertical positions as the text, just off left (and off right for P2 later).
def find_judgement_count(document, judgement_bounds, judgement):
    judgement_vertical_bounds = (judgement_bounds.vertices[0].y, judgement_bounds.vertices[2].y)
    closest_word = ''
    min_vertical_diff = 100000
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:

                    # Don't check judgement against itself
                    if assemble_word(word) == judgement:
                        continue

                    word_vertical_bounds = (word.bounding_box.vertices[0].y, word.bounding_box.vertices[2].y)
                    vertical_diff = abs(judgement_vertical_bounds[0] - word_vertical_bounds[0]) + abs(judgement_vertical_bounds[1] - word_vertical_bounds[1])

                    if vertical_diff < min_vertical_diff:
                        closest_word = assemble_word(word)
                        min_vertical_diff = vertical_diff
    return closest_word


# Judgement counts will always have similar vertical positions as the text, just off left (and off right for P2 later).
def find_max_combo(document):
    max_combo_bounds = find_word_location(document, 'MAX')
    if max_combo_bounds == None:
        return 'Not Found'
    max_combo_vertical_bounds = (max_combo_bounds.vertices[0].y, max_combo_bounds.vertices[2].y)
    closest_word = ''
    min_vertical_diff = 100000
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)

                    # Don't check judgement against itself
                    if assembled == 'MAX' or assembled == 'COMBO':
                        continue

                    word_vertical_bounds = (word.bounding_box.vertices[0].y, word.bounding_box.vertices[2].y)
                    vertical_diff = abs(max_combo_vertical_bounds[0] - word_vertical_bounds[0]) + abs(max_combo_vertical_bounds[1] - word_vertical_bounds[1])

                    if vertical_diff < min_vertical_diff:
                        closest_word = assemble_word(word)
                        min_vertical_diff = vertical_diff
    return closest_word