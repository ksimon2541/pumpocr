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

    closest = 'Not Found'
    closest_dist = 100000
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)

                    # Ensure what we're considering is a number
                    if try_parse_number(assembled) == None:
                        continue

                    num = int(assembled)
                    if num > 28:
                        continue

                    (x_dist, y_dist) = dist_between_top_left(playstyle_bounds, word.bounding_box)
                    if y_dist < closest_dist:
                        closest_dist = y_dist
                        closest = assembled

    return closest


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
        judgement_count = 'Not Found'

        # todo: use different method to locate judgements that is more consistent
        if judgement_bounds != None:
            judgement_count = find_judgement_count(document, judgement_bounds)

        judgement_pairs.append((judgement, judgement_count))
    return judgement_pairs


# Judgement counts will always have similar vertical positions as the text, just off left (and off right for P2 later).
def find_judgement_count(document, judgement_bounds):
    closest_word = 'Not Found'
    closest_x_dist = 100000
    closest_y_dist = 100000
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)

                    # Ensure what we're considering is a number
                    if try_parse_number(assembled) == None:
                        continue

                    (x_dist, y_dist) = dist_between_top_left(judgement_bounds, word.bounding_box)

                    # Skip anything not in the same row
                    if y_dist > 20:
                        continue

                    if x_dist < closest_x_dist:
                        closest_x_dist = x_dist
                        closest_word = assembled

    return closest_word


# Judgement counts will always have similar vertical positions as the text, just off left (and off right for P2 later).
def find_max_combo(document):
    max_combo_bounds = find_word_location(document, 'MAX')
    if max_combo_bounds == None:
        return 'Not Found'

    closest_word = 'Not Found'
    closest_dist = 100000
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled = assemble_word(word)

                    # Ensure we're dealing with a number
                    if try_parse_number(assembled) == None:
                        continue

                    (x_dist, y_dist) = dist_between_top_left(max_combo_bounds, word.bounding_box)
                    if y_dist < closest_dist:
                        closest_dist = y_dist
                        closest_word = assemble_word(word)
    return closest_word

def try_parse_number(str):
    try:
        num = int(str)
        return num
    except ValueError:
        return None

def dist_between_top_left(poly1, poly2):
    x_dist = abs(poly1.vertices[0].x - poly2.vertices[0].x)
    y_dist = abs(poly1.vertices[0].y - poly2.vertices[0].y)
    return (x_dist, y_dist)